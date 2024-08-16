import math
import os
import datetime
import time
import json
import torch
import h5py
import argparse
import zarr
import numpy as np
from tqdm import tqdm
from abc import ABCMeta, abstractmethod
from sklearn.model_selection import StratifiedKFold
import torch.multiprocessing as mp
import torch.distributed as dist
from scipy.ndimage import zoom

from bioimageio.core import create_prediction_pipeline
from bioimageio.spec import load_description, InvalidDescr
from bioimageio.spec.model.v0_5 import ModelDescr
from bioimageio.core.digest_spec import get_test_inputs

from biapy.config.config import Config
from biapy.models import (
    build_model,
    build_torchvision_model,
    build_bmz_model,
    check_bmz_args,
)
from biapy.engine import prepare_optimizer, build_callbacks
from biapy.data.generators import (
    create_train_val_augmentors,
    create_test_augmentor,
    check_generator_consistence,
)
from biapy.utils.misc import (
    get_world_size,
    get_rank,
    is_main_process,
    save_model,
    time_text,
    load_model_checkpoint,
    TensorboardLogger,
    to_pytorch_format,
    to_numpy_format,
    is_dist_avail_and_initialized,
    setup_for_distributed,
)
from biapy.utils.util import (
    load_data_from_dir,
    load_3d_images_from_dir,
    create_plots,
    pad_and_reflect,
    save_tif,
    check_downsample_division,
    read_chunked_data,
    order_dimensions,
    read_img,
)
from biapy.engine.train_engine import train_one_epoch, evaluate
from biapy.data.data_2D_manipulation import (
    crop_data_with_overlap,
    merge_data_with_overlap,
    load_and_prepare_2D_train_data,
)
from biapy.data.data_3D_manipulation import (
    crop_3D_data_with_overlap,
    merge_3D_data_with_overlap,
    load_and_prepare_3D_data,
    load_and_prepare_3D_efficient_format_data,
    load_3D_efficient_files,
    extract_3D_patch_with_overlap_yield,
)
from biapy.data.post_processing.post_processing import (
    ensemble8_2d_predictions,
    ensemble16_3d_predictions,
    apply_binary_mask,
)
from biapy.data.post_processing import apply_post_processing
from biapy.data.pre_processing import preprocess_data


class Base_Workflow(metaclass=ABCMeta):
    """
    Base workflow class. A new workflow should extend this class.

    Parameters
    ----------
    cfg : YACS configuration
        Running configuration.

    Job_identifier : str
        Complete name of the running job.

    device : Torch device
        Device used.

    args : argpase class
        Arguments used in BiaPy's call.
    """

    def __init__(
        self,
        cfg: type[Config],
        job_identifier: str,
        device: type[torch.device],
        args: type[argparse.Namespace],
    ):
        self.cfg = cfg
        self.args = args
        self.job_identifier = job_identifier
        self.device = device
        self.original_test_path = None
        self.original_test_mask_path = None
        self.test_mask_filenames = None
        self.cross_val_samples_ids = None
        self.post_processing = {}
        self.post_processing["per_image"] = False
        self.post_processing["as_3D_stack"] = False
        self.test_filenames = None
        self.data_norm = None
        self.model = None
        self.checkpoint_path = None
        self.optimizer = None
        self.loss_scaler = None
        self.model_prepared = False
        self.dtype = np.float32 if not self.cfg.TEST.REDUCE_MEMORY else np.float16
        self.dtype_str = "float32" if not self.cfg.TEST.REDUCE_MEMORY else "float16"
        self.loss_dtype = torch.float32

        self.use_gt = False
        if self.cfg.DATA.TEST.LOAD_GT or self.cfg.DATA.TEST.USE_VAL_AS_TEST:
            self.use_gt = True

        # Save paths in case we need them in a future
        self.orig_train_path = self.cfg.DATA.TRAIN.PATH
        self.orig_train_mask_path = self.cfg.DATA.TRAIN.GT_PATH
        self.orig_val_path = self.cfg.DATA.VAL.PATH
        self.orig_val_mask_path = self.cfg.DATA.VAL.GT_PATH

        self.all_pred = []
        self.all_gt = []

        self.stats = {}

        # Per crop
        self.stats["per_crop"] = {}
        self.stats["patch_by_batch_counter"] = 0

        # Merging the image
        self.stats["merge_patches"] = {}
        self.stats["merge_patches_post"] = {}

        # As 3D stack
        self.stats["as_3D_stack"] = {}
        self.stats["as_3D_stack_post"] = {}

        # Full image
        self.stats["full_image"] = {}
        self.stats["full_image_post"] = {}

        # By chunks
        self.stats["by_chunks"] = {}

        self.by_chunks = False
        if (
            self.cfg.TEST.BY_CHUNKS.ENABLE
            and self.cfg.TEST.BY_CHUNKS.WORKFLOW_PROCESS.ENABLE
            and self.cfg.TEST.BY_CHUNKS.WORKFLOW_PROCESS.TYPE == "chunk_by_chunk"
        ):
            self.by_chunks = True

        self.world_size = get_world_size()
        self.global_rank = get_rank()
        if self.cfg.TEST.BY_CHUNKS.ENABLE and self.cfg.PROBLEM.NDIM == "3D":
            maxsize = min(10, self.cfg.SYSTEM.NUM_GPUS * 10)
            self.output_queue = mp.Queue(maxsize=maxsize)
            self.input_queue = mp.Queue(maxsize=maxsize)
            self.extract_info_queue = mp.Queue()

        # Test variables
        if self.cfg.TEST.POST_PROCESSING.MEDIAN_FILTER:
            if self.cfg.PROBLEM.NDIM == "2D":
                if self.cfg.TEST.ANALIZE_2D_IMGS_AS_3D_STACK:
                    self.post_processing["as_3D_stack"] = True
                else:
                    self.post_processing["per_image"] = True
            else:
                self.post_processing["per_image"] = True

        # Define permute shapes to pass from Numpy axis order (Y,X,C) to Pytorch's (C,Y,X)
        self.axis_order = (0, 3, 1, 2) if self.cfg.PROBLEM.NDIM == "2D" else (0, 4, 1, 2, 3)
        self.axis_order_back = (0, 2, 3, 1) if self.cfg.PROBLEM.NDIM == "2D" else (0, 2, 3, 4, 1)

        # Define metrics
        self.define_metrics()

        # Tochvision variables
        self.torchvision_preprocessing = None

        # Load BioImage Model Zoo pretrained model information
        self.bmz_config = {}
        self.bmz_pipeline = None
        if self.cfg.MODEL.SOURCE == "bmz":
            self.bmz_config["preprocessing"] = check_bmz_args(self.cfg.MODEL.BMZ.SOURCE_MODEL_ID, self.cfg)

            print("Loading BioImage Model Zoo pretrained model . . .")
            self.bmz_config["original_bmz_config"] = load_description(self.cfg.MODEL.BMZ.SOURCE_MODEL_ID)

            # let's make sure we have a valid model...
            if isinstance(self.bmz_config["original_bmz_config"], InvalidDescr):
                raise ValueError(f"Failed to load {self.cfg.MODEL.SOURCE}")

            self.bmz_config["original_model_spec_version"] = "v0_4"
            if isinstance(self.bmz_config["original_bmz_config"], ModelDescr):
                self.bmz_config["original_model_spec_version"] = "v0_5"

            # 1) Change PATCH_SIZE with the one stored in the RDF
            inputs = get_test_inputs(self.bmz_config["original_bmz_config"])
            if "input0" in inputs.members:
                input_image_shape = inputs.members["input0"]._data.shape
            elif "raw" in inputs.members:
                input_image_shape = inputs.members["raw"]._data.shape
            else:
                raise ValueError(f"Couldn't load input info from BMZ model's RDF: {inputs}")
            # if not self.bmz_config['original_model_spec_version']:
            #     input_image = np.load(download(self.bmz_config['original_bmz_config'].test_inputs[0]).path)
            # else:
            #     input_image = np.load(download(self.bmz_config['original_bmz_config'].inputs[0].test_tensor.source.absolute()).path)

            opts = []
            if self.cfg.DATA.PATCH_SIZE != input_image_shape[2:] + (input_image_shape[1],):
                opts += [
                    "DATA.PATCH_SIZE",
                    input_image_shape[2:] + (input_image_shape[1],),
                ]
                print(
                    "[BMZ] Changed 'DATA.PATCH_SIZE' from {} to {} as defined in the RDF".format(
                        self.cfg.DATA.PATCH_SIZE, opts[1]
                    )
                )

            # 2) Change preprocessing to the one stablished by BMZ
            print(
                f"[BMZ] Overriding preprocessing steps to the ones fixed in BMZ model: {self.bmz_config['preprocessing']}"
            )
            if isinstance(self.bmz_config["preprocessing"], list) and len(self.bmz_config["preprocessing"]) > 1:
                raise ValueError("More than one preprocessing from BMZ not implemented yet")

            # Translate BMZ keywords into BiaPy's
            if len(self.bmz_config["preprocessing"]) > 0:
                app_mode = "dataset" if self.bmz_config["preprocessing"]["kwargs"]["mode"] == "per_dataset" else "image"
                if app_mode != self.cfg.DATA.NORMALIZATION.APPLICATION_MODE:
                    opts += ["DATA.NORMALIZATION.APPLICATION_MODE", app_mode]
                    print(
                        "[BMZ] Changed 'DATA.NORMALIZATION.APPLICATION_MODE' from {} to {} as defined in the RDF".format(
                            self.cfg.DATA.NORMALIZATION.APPLICATION_MODE, app_mode
                        )
                    )

                if self.cfg.TRAIN.ENABLE and not self.cfg.DATA.TRAIN.IN_MEMORY and app_mode == "dataset":
                    raise ValueError(
                        "The BioImage Model Zoo model selected changed your normalization settings. Due to that the following error "
                        "appeared:\n'DATA.NORMALIZATION.APPLICATION_MODE' == 'dataset' can only be applied if 'DATA.TRAIN.IN_MEMORY' == True"
                    )
                if self.cfg.TEST.ENABLE and not self.cfg.DATA.TEST.IN_MEMORY and app_mode == "dataset":
                    raise ValueError(
                        "The BioImage Model Zoo model selected changed your normalization settings. Due to that the following error "
                        "appeared:\n'DATA.NORMALIZATION.APPLICATION_MODE' == 'dataset' can only be applied if 'DATA.TEST.IN_MEMORY' == True"
                    )

                # 'zero_mean_unit_variance' norm of BMZ is as our 'custom' norm without providing mean/std
                if self.bmz_config["preprocessing"]["name"] == "zero_mean_unit_variance":
                    opts += [
                        "DATA.NORMALIZATION.TYPE",
                        "custom",
                        "DATA.NORMALIZATION.CUSTOM_MEAN",
                        -1.0,
                        "DATA.NORMALIZATION.CUSTOM_STD",
                        -1.0,
                    ]
                    if self.cfg.DATA.NORMALIZATION.TYPE != "custom":
                        print(
                            "[BMZ] Changed 'DATA.NORMALIZATION.TYPE' from {} to {} as defined in the RDF".format(
                                self.cfg.DATA.NORMALIZATION.TYPE, "custom"
                            )
                        )
                    if self.cfg.DATA.NORMALIZATION.CUSTOM_MEAN != -1:
                        print(
                            "[BMZ] Changed 'DATA.NORMALIZATION.CUSTOM_MEAN' from {} to {} as defined in the RDF".format(
                                self.cfg.DATA.NORMALIZATION.CUSTOM_MEAN, -1
                            )
                        )
                    if self.cfg.DATA.NORMALIZATION.CUSTOM_STD != -1:
                        print(
                            "[BMZ] Changed 'DATA.NORMALIZATION.CUSTOM_STD' from {} to {} as defined in the RDF".format(
                                self.cfg.DATA.NORMALIZATION.CUSTOM_STD, -1
                            )
                        )
                elif self.bmz_config["preprocessing"]["name"] == "fixed_zero_mean_unit_variance":
                    mean = -1
                    std = -1
                    if "kwargs" in self.bmz_config["preprocessing"] and "mean" in self.bmz_config["preprocessing"]["kwargs"]:
                        mean = self.bmz_config["preprocessing"]["kwargs"]["mean"]
                        std = self.bmz_config["preprocessing"]["kwargs"]["std"]
                    elif "mean" in self.bmz_config["preprocessing"]:
                        mean = self.bmz_config["preprocessing"]["mean"]
                        std = self.bmz_config["preprocessing"]["std"]
                    opts += [
                        "DATA.NORMALIZATION.TYPE",
                        "custom",
                        "DATA.NORMALIZATION.CUSTOM_MEAN",
                        mean,
                        "DATA.NORMALIZATION.CUSTOM_STD",
                        std,
                    ]
                    if self.cfg.DATA.NORMALIZATION.TYPE != "custom":
                        print(
                            "[BMZ] Changed 'DATA.NORMALIZATION.TYPE' from {} to {} as defined in the RDF".format(
                                self.cfg.DATA.NORMALIZATION.TYPE, "custom"
                            )
                        )
                    if self.cfg.DATA.NORMALIZATION.CUSTOM_MEAN != mean:
                        print(
                            "[BMZ] Changed 'DATA.NORMALIZATION.CUSTOM_MEAN' from {} to {} as defined in the RDF".format(
                                self.cfg.DATA.NORMALIZATION.CUSTOM_MEAN, mean
                            )
                        )
                    if self.cfg.DATA.NORMALIZATION.CUSTOM_STD != std:
                        print(
                            "[BMZ] Changed 'DATA.NORMALIZATION.CUSTOM_STD' from {} to {} as defined in the RDF".format(
                                self.cfg.DATA.NORMALIZATION.CUSTOM_STD, std
                            )
                        )
                # 'scale_linear' norm of BMZ is close to our 'div' norm (TODO: we need to control the "gain" arg)
                elif self.bmz_config["preprocessing"]["name"] == "scale_linear":
                    opts += ["DATA.NORMALIZATION.TYPE", "div"]
                    if self.cfg.DATA.NORMALIZATION.TYPE != "div":
                        print(
                            "[BMZ] Changed 'DATA.NORMALIZATION.TYPE' from {} to {} as defined in the RDF".format(
                                self.cfg.DATA.NORMALIZATION.TYPE, "div"
                            )
                        )
                # 'scale_range' norm of BMZ is as our PERC_CLIP + 'scale_range' norm
                elif self.bmz_config["preprocessing"]["name"] == "scale_range":
                    opts += ["DATA.NORMALIZATION.TYPE", "scale_range"]
                    if self.cfg.DATA.NORMALIZATION.TYPE != "scale_range":
                        print(
                            "[BMZ] Changed 'DATA.NORMALIZATION.TYPE' from {} to {} as defined in the RDF".format(
                                self.cfg.DATA.NORMALIZATION.TYPE, "scale_range"
                            )
                        )
                    if (
                        float(self.bmz_config["preprocessing"]["kwargs"]["min_percentile"]) != 0
                        or float(self.bmz_config["preprocessing"]["kwargs"]["max_percentile"]) != 100
                    ):
                        opts += [
                            "DATA.NORMALIZATION.PERC_CLIP",
                            True,
                            "DATA.NORMALIZATION.PERC_LOWER",
                            float(self.bmz_config["preprocessing"]["kwargs"]["min_percentile"]),
                            "DATA.NORMALIZATION.PERC_UPPER",
                            float(self.bmz_config["preprocessing"]["kwargs"]["max_percentile"]),
                        ]
                        if not self.cfg.DATA.NORMALIZATION.PERC_CLIP:
                            print(
                                "[BMZ] Changed 'DATA.NORMALIZATION.PERC_CLIP' from {} to {} as defined in the RDF".format(
                                    self.cfg.DATA.NORMALIZATION.PERC_CLIP, True
                                )
                            )
                        if (
                            self.cfg.DATA.NORMALIZATION.PERC_LOWER
                            != self.bmz_config["preprocessing"]["kwargs"]["min_percentile"]
                        ):
                            print(
                                "[BMZ] Changed 'DATA.NORMALIZATION.PERC_LOWER' from {} to {} as defined in the RDF".format(
                                    self.cfg.DATA.NORMALIZATION.PERC_LOWER,
                                    self.bmz_config["preprocessing"]["kwargs"]["min_percentile"],
                                )
                            )
                        if (
                            self.cfg.DATA.NORMALIZATION.PERC_UPPER
                            != self.bmz_config["preprocessing"]["kwargs"]["max_percentile"]
                        ):
                            print(
                                "[BMZ] Changed 'DATA.NORMALIZATION.PERC_UPPER' from {} to {} as defined in the RDF".format(
                                    self.cfg.DATA.NORMALIZATION.PERC_UPPER,
                                    self.bmz_config["preprocessing"]["kwargs"]["max_percentile"],
                                )
                            )

            self.cfg.merge_from_list(opts)

    def define_metrics(self):
        """
        This function must define the following variables:

        self.train_metrics : List of functions
            Metrics to be calculated during model's training.

        self.train_metric_names : List of str
            Names of the metrics calculated during training.

        self.train_metric_best : List of str
            To know which value should be considered as the best one. Options must be: "max" or "min".

        self.test_metrics : List of functions
            Metrics to be calculated during model's test/inference.

        self.test_metric_names : List of str
            Names of the metrics calculated during test/inference.

        self.loss : Function
            Loss function used during training and test.
        """
        if not hasattr(self, "train_metrics"):
            raise ValueError("'train_metrics' is not defined. Correct define_metrics() function")
        if not hasattr(self, "train_metric_names"):
            raise ValueError("'train_metric_names' is not defined. Correct define_metrics() function")
        if not hasattr(self, "train_metric_best"):
            raise ValueError("'train_metric_best' is not defined. Correct define_metrics() function")
        else:
            assert all(
                [True if x in ["max", "min"] else False for x in self.train_metric_best]
            ), "'train_metric_best' needs to be one between ['max', 'min']"
        if not hasattr(self, "test_metrics"):
            raise ValueError("'test_metrics' is not defined. Correct define_metrics() function")
        if not hasattr(self, "test_metric_names"):
            raise ValueError("'test_metric_names' is not defined. Correct define_metrics() function")
        if not hasattr(self, "loss"):
            raise ValueError("'loss' is not defined. Correct define_metrics() function")

    @abstractmethod
    def metric_calculation(self, output, targets, train=True, metric_logger=None):
        """
        Execution of the metrics defined in :func:`~define_metrics` function.

        Parameters
        ----------
        output : Torch Tensor
            Prediction of the model.

        targets : Torch Tensor
            Ground truth to compare the prediction with.

        train : bool, optional
            Whether to calculate train or test metrics.

        metric_logger : MetricLogger, optional
            Class to be updated with the new metric(s) value(s) calculated.

        Returns
        -------
        value : float
            Value of the metric for the given prediction.
        """
        raise NotImplementedError

    def prepare_targets(self, targets, batch):
        """
        Location to perform any necessary data transformations to ``targets``
        before calculating the loss.

        Parameters
        ----------
        targets : Torch Tensor
            Ground truth to compare the prediction with.

        batch : Torch Tensor
            Prediction of the model. Only used in SSL workflow.

        Returns
        -------
        targets : Torch tensor
            Resulting targets.
        """
        # We do not use 'batch' input but in SSL workflow
        return to_pytorch_format(targets, self.axis_order, self.device)

    def load_train_data(self):
        """
        Load training and validation data.
        """
        if self.cfg.TRAIN.ENABLE:
            print("##########################")
            print("#   LOAD TRAINING DATA   #")
            print("##########################")
            self.X_val, self.Y_val = None, None
            if self.cfg.DATA.TRAIN.IN_MEMORY:
                val_split = self.cfg.DATA.VAL.SPLIT_TRAIN if self.cfg.DATA.VAL.FROM_TRAIN else 0.0
                f_name = load_and_prepare_2D_train_data if self.cfg.PROBLEM.NDIM == "2D" else load_and_prepare_3D_data
                preprocess_cfg = self.cfg.DATA.PREPROCESS if self.cfg.DATA.PREPROCESS.TRAIN else None
                preprocess_fn = preprocess_data if self.cfg.DATA.PREPROCESS.TRAIN else None
                is_y_mask = self.cfg.PROBLEM.TYPE in ["SEMANTIC_SEG", "INSTANCE_SEG"]
                objs = f_name(
                    self.cfg.DATA.TRAIN.PATH,
                    self.mask_path,
                    cross_val=self.cfg.DATA.VAL.CROSS_VAL,
                    cross_val_nsplits=self.cfg.DATA.VAL.CROSS_VAL_NFOLD,
                    cross_val_fold=self.cfg.DATA.VAL.CROSS_VAL_FOLD,
                    val_split=val_split,
                    seed=self.cfg.SYSTEM.SEED,
                    shuffle_val=self.cfg.DATA.VAL.RANDOM,
                    random_crops_in_DA=self.cfg.DATA.EXTRACT_RANDOM_PATCH,
                    crop_shape=self.cfg.DATA.PATCH_SIZE,
                    y_upscaling=self.cfg.PROBLEM.SUPER_RESOLUTION.UPSCALING,
                    ov=self.cfg.DATA.TRAIN.OVERLAP,
                    padding=self.cfg.DATA.TRAIN.PADDING,
                    minimum_foreground_perc=self.cfg.DATA.TRAIN.MINIMUM_FOREGROUND_PER,
                    reflect_to_complete_shape=self.cfg.DATA.REFLECT_TO_COMPLETE_SHAPE,
                    convert_to_rgb=self.cfg.DATA.FORCE_RGB,
                    preprocess_cfg=preprocess_cfg,
                    is_y_mask=is_y_mask,
                    preprocess_f=preprocess_fn,
                )

                if self.cfg.DATA.VAL.FROM_TRAIN:
                    if self.cfg.DATA.VAL.CROSS_VAL:
                        (
                            self.X_train,
                            self.Y_train,
                            self.X_val,
                            self.Y_val,
                            self.train_filenames,
                            self.cross_val_samples_ids,
                        ) = objs
                    else:
                        (
                            self.X_train,
                            self.Y_train,
                            self.X_val,
                            self.Y_val,
                            self.train_filenames,
                        ) = objs
                else:
                    self.X_train, self.Y_train, self.train_filenames = objs
                del objs
            else:
                # Checking if the user inputted Zarr/H5 files
                zarr_files = sorted(next(os.walk(self.cfg.DATA.TRAIN.PATH))[1])
                h5_files = sorted(next(os.walk(self.cfg.DATA.TRAIN.PATH))[2])
                if (
                    self.cfg.PROBLEM.NDIM == "3D"
                    and (len(zarr_files) > 0 and ".zarr" in zarr_files[0])
                    or (len(h5_files) > 0 and ".h5" in h5_files[0])
                ):
                    val_split = self.cfg.DATA.VAL.SPLIT_TRAIN if self.cfg.DATA.VAL.FROM_TRAIN else 0.0

                    if len(zarr_files) > 0 and ".zarr" in zarr_files[0]:
                        print("Working with Zarr files . . .")
                        img_files = [os.path.join(self.cfg.DATA.TRAIN.PATH, x) for x in zarr_files]
                        mask_files = [os.path.join(self.mask_path, x) for x in sorted(next(os.walk(self.mask_path))[1])]
                    elif len(h5_files) > 0 and ".h5" in h5_files[0]:
                        print("Working with H5 files . . .")
                        img_files = [os.path.join(self.cfg.DATA.TRAIN.PATH, x) for x in h5_files]
                        mask_files = [os.path.join(self.mask_path, x) for x in sorted(next(os.walk(self.mask_path))[2])]
                    del zarr_files, h5_files

                    if self.cfg.DATA.EXTRACT_RANDOM_PATCH:
                        print(
                            "WARNING: 'DATA.EXTRACT_RANDOM_PATCH' not taken into account when working with Zarr/H5 images"
                        )
                    if self.cfg.DATA.FORCE_RGB:
                        print("WARNING: 'DATA.FORCE_RGB' not taken into account when working with Zarr/H5 images")

                    # When the labels and raw images are within the same Zarr file
                    mult_dat = None
                    if self.cfg.DATA.TRAIN.INPUT_ZARR_MULTIPLE_DATA:
                        mult_dat = {
                            "raw_path": self.cfg.DATA.TRAIN.INPUT_ZARR_MULTIPLE_DATA_RAW_PATH,
                            "gt_path": self.cfg.DATA.TRAIN.INPUT_ZARR_MULTIPLE_DATA_GT_PATH,
                            "use_gt_path": self.cfg.PROBLEM.TYPE != "INSTANCE_SEG",
                        }

                    objs = load_and_prepare_3D_efficient_format_data(
                        img_files,
                        mask_files,
                        input_img_axes=self.cfg.DATA.TRAIN.INPUT_IMG_AXES_ORDER,
                        input_mask_axes=self.cfg.DATA.TRAIN.INPUT_MASK_AXES_ORDER,
                        cross_val=self.cfg.DATA.VAL.CROSS_VAL,
                        cross_val_nsplits=self.cfg.DATA.VAL.CROSS_VAL_NFOLD,
                        cross_val_fold=self.cfg.DATA.VAL.CROSS_VAL_FOLD,
                        val_split=val_split,
                        seed=self.cfg.SYSTEM.SEED,
                        shuffle_val=self.cfg.DATA.VAL.RANDOM,
                        crop_shape=self.cfg.DATA.PATCH_SIZE,
                        y_upscaling=self.cfg.PROBLEM.SUPER_RESOLUTION.UPSCALING,
                        ov=self.cfg.DATA.TRAIN.OVERLAP,
                        padding=self.cfg.DATA.TRAIN.PADDING,
                        minimum_foreground_perc=self.cfg.DATA.TRAIN.MINIMUM_FOREGROUND_PER,
                        multiple_data_within_zarr=mult_dat,
                    )

                    if self.cfg.DATA.VAL.FROM_TRAIN:
                        if self.cfg.DATA.VAL.CROSS_VAL:
                            (
                                self.X_train,
                                self.Y_train,
                                self.X_val,
                                self.Y_val,
                                self.cross_val_samples_ids,
                            ) = objs
                        else:
                            self.X_train, self.Y_train, self.X_val, self.Y_val = objs
                    else:
                        self.X_train, self.Y_train = objs
                    del objs

                else:
                    self.X_train, self.Y_train = None, None

            ##################
            ### VALIDATION ###
            ##################
            if not self.cfg.DATA.VAL.FROM_TRAIN:
                if self.cfg.DATA.VAL.IN_MEMORY:
                    print("1) Loading validation images . . .")
                    f_name = load_data_from_dir if self.cfg.PROBLEM.NDIM == "2D" else load_3d_images_from_dir
                    preprocess_cfg = self.cfg.DATA.PREPROCESS if self.cfg.DATA.PREPROCESS.VAL else None
                    preprocess_fn = preprocess_data if self.cfg.DATA.PREPROCESS.VAL else None
                    is_y_mask = self.cfg.PROBLEM.TYPE in [
                        "SEMANTIC_SEG",
                        "INSTANCE_SEG",
                    ]
                    self.X_val, _, _ = f_name(
                        self.cfg.DATA.VAL.PATH,
                        crop=True,
                        crop_shape=self.cfg.DATA.PATCH_SIZE,
                        overlap=self.cfg.DATA.VAL.OVERLAP,
                        padding=self.cfg.DATA.VAL.PADDING,
                        reflect_to_complete_shape=self.cfg.DATA.REFLECT_TO_COMPLETE_SHAPE,
                        convert_to_rgb=self.cfg.DATA.FORCE_RGB,
                        preprocess_cfg=preprocess_cfg,
                        is_mask=False,
                        preprocess_f=preprocess_fn,
                    )

                    if self.cfg.PROBLEM.NDIM == "2D":
                        crop_shape = (
                            self.cfg.DATA.PATCH_SIZE[0] * self.cfg.PROBLEM.SUPER_RESOLUTION.UPSCALING[0],
                            self.cfg.DATA.PATCH_SIZE[1] * self.cfg.PROBLEM.SUPER_RESOLUTION.UPSCALING[1],
                            self.cfg.DATA.PATCH_SIZE[2],
                        )
                    else:
                        crop_shape = (
                            self.cfg.DATA.PATCH_SIZE[0],
                            self.cfg.DATA.PATCH_SIZE[1] * self.cfg.PROBLEM.SUPER_RESOLUTION.UPSCALING[0],
                            self.cfg.DATA.PATCH_SIZE[2] * self.cfg.PROBLEM.SUPER_RESOLUTION.UPSCALING[1],
                            self.cfg.DATA.PATCH_SIZE[3] * self.cfg.PROBLEM.SUPER_RESOLUTION.UPSCALING[2],
                        )
                    if self.load_Y_val:
                        self.Y_val, _, _ = f_name(
                            self.cfg.DATA.VAL.GT_PATH,
                            crop=True,
                            crop_shape=crop_shape,
                            overlap=self.cfg.DATA.VAL.OVERLAP,
                            padding=self.cfg.DATA.VAL.PADDING,
                            reflect_to_complete_shape=self.cfg.DATA.REFLECT_TO_COMPLETE_SHAPE,
                            check_channel=False,
                            check_drange=False,
                            convert_to_rgb=self.cfg.DATA.FORCE_RGB,
                            preprocess_cfg=preprocess_cfg,
                            is_mask=is_y_mask,
                            preprocess_f=preprocess_fn,
                        )
                    if self.Y_val is not None and len(self.X_val) != len(self.Y_val):
                        raise ValueError(
                            "Different number of raw and ground truth items ({} vs {}). "
                            "Please check the data!".format(len(self.X_val), len(self.Y_val))
                        )
                else:
                    # Checking if the user inputted Zarr/H5 files
                    zarr_files = sorted(next(os.walk(self.cfg.DATA.VAL.PATH))[1])
                    h5_files = sorted(next(os.walk(self.cfg.DATA.VAL.PATH))[2])
                    if (
                        self.cfg.PROBLEM.NDIM == "3D"
                        and (len(zarr_files) > 0 and ".zarr" in zarr_files[0])
                        or (len(h5_files) > 0 and ".h5" in h5_files[0])
                    ):
                        print("1) Loading validation image information . . .")
                        if len(zarr_files) > 0 and ".zarr" in zarr_files[0]:
                            print("Working with Zarr files . . .")
                            img_files = [os.path.join(self.cfg.DATA.VAL.PATH, x) for x in zarr_files]
                            mask_files = [
                                os.path.join(self.mask_path, x) for x in sorted(next(os.walk(self.mask_path))[1])
                            ]
                        elif len(h5_files) > 0 and ".h5" in h5_files[0]:
                            print("Working with H5 files . . .")
                            img_files = [os.path.join(self.cfg.DATA.VAL.PATH, x) for x in h5_files]
                            mask_files = [
                                os.path.join(self.mask_path, x) for x in sorted(next(os.walk(self.mask_path))[2])
                            ]
                        del zarr_files, h5_files

                        if self.cfg.DATA.FORCE_RGB:
                            print("WARNING: 'DATA.FORCE_RGB' not taken into account when working with Zarr/H5 images")

                        data_within_zarr_path, data_within_zarr_mask_path = None, None
                        if self.cfg.DATA.TRAIN.INPUT_ZARR_MULTIPLE_DATA:
                            data_within_zarr_path = self.cfg.DATA.TRAIN.INPUT_ZARR_MULTIPLE_DATA_RAW_PATH
                            if self.cfg.PROBLEM.TYPE != "INSTANCE_SEG":
                                data_within_zarr_mask_path = self.cfg.DATA.TRAIN.INPUT_ZARR_MULTIPLE_DATA_RAW_PATH

                        self.X_val, _ = load_3D_efficient_files(
                            data_path=img_files,
                            input_axes=self.cfg.DATA.VAL.INPUT_IMG_AXES_ORDER,
                            crop_shape=self.cfg.DATA.PATCH_SIZE,
                            overlap=self.cfg.DATA.VAL.OVERLAP,
                            padding=self.cfg.DATA.VAL.PADDING,
                            data_within_zarr_path=data_within_zarr_path,
                        )

                        if self.cfg.PROBLEM.NDIM == "2D":
                            crop_shape = (
                                self.cfg.DATA.PATCH_SIZE[0] * self.cfg.PROBLEM.SUPER_RESOLUTION.UPSCALING[0],
                                self.cfg.DATA.PATCH_SIZE[1] * self.cfg.PROBLEM.SUPER_RESOLUTION.UPSCALING[1],
                                self.cfg.DATA.PATCH_SIZE[2],
                            )
                        else:
                            crop_shape = (
                                self.cfg.DATA.PATCH_SIZE[0],
                                self.cfg.DATA.PATCH_SIZE[1] * self.cfg.PROBLEM.SUPER_RESOLUTION.UPSCALING[0],
                                self.cfg.DATA.PATCH_SIZE[2] * self.cfg.PROBLEM.SUPER_RESOLUTION.UPSCALING[1],
                                self.cfg.DATA.PATCH_SIZE[3] * self.cfg.PROBLEM.SUPER_RESOLUTION.UPSCALING[2],
                            )

                        if self.load_Y_val:
                            print("1) Loading validation GT information . . .")
                            self.Y_val, _ = load_3D_efficient_files(
                                data_path=mask_files,
                                input_axes=self.cfg.DATA.VAL.INPUT_MASK_AXES_ORDER,
                                crop_shape=crop_shape,
                                overlap=self.cfg.DATA.VAL.OVERLAP,
                                padding=self.cfg.DATA.VAL.PADDING,
                                check_channel=False,
                                data_within_zarr_path=data_within_zarr_mask_path,
                            )
                        else:
                            self.Y_val = None
                        if self.Y_val is not None and len(self.X_val) != len(self.Y_val):
                            raise ValueError(
                                "Different number of raw and ground truth items ({} vs {}). "
                                "Please check the data!".format(len(self.X_val), len(self.Y_val))
                            )

                    else:
                        self.X_val, self.Y_val = None, None

        # Ensure all the processes have read the data
        if is_dist_avail_and_initialized():
            print("Waiting until all processes have read the data . . .")
            dist.barrier()

    def destroy_train_data(self):
        """
        Delete training variable to release memory.
        """
        print("Releasing memory . . .")
        if "X_train" in locals() or "X_train" in globals():
            del self.X_train
        if "Y_train" in locals() or "Y_train" in globals():
            del self.Y_train
        if "X_val" in locals() or "X_val" in globals():
            del self.X_val
        if "Y_val" in locals() or "Y_val" in globals():
            del self.Y_val
        if "train_generator" in locals() or "train_generator" in globals():
            del self.train_generator
        if "val_generator" in locals() or "val_generator" in globals():
            del self.val_generator

    def prepare_train_generators(self):
        """
        Build train and val generators.
        """
        if self.cfg.TRAIN.ENABLE:
            print("##############################")
            print("#  PREPARE TRAIN GENERATORS  #")
            print("##############################")
            (
                self.train_generator,
                self.val_generator,
                self.data_norm,
                self.num_training_steps_per_epoch,
            ) = create_train_val_augmentors(
                self.cfg,
                self.X_train,
                self.Y_train,
                self.X_val,
                self.Y_val,
                self.world_size,
                self.global_rank,
            )
            if self.cfg.DATA.CHECK_GENERATORS and self.cfg.PROBLEM.TYPE != "CLASSIFICATION":
                check_generator_consistence(
                    self.train_generator,
                    self.cfg.PATHS.GEN_CHECKS + "_train",
                    self.cfg.PATHS.GEN_MASK_CHECKS + "_train",
                )
                check_generator_consistence(
                    self.val_generator,
                    self.cfg.PATHS.GEN_CHECKS + "_val",
                    self.cfg.PATHS.GEN_MASK_CHECKS + "_val",
                )

    def bmz_model_call(self, in_img, is_train=False):
        """
        Call BioImage Model Zoo model.

        Parameters
        ----------
        in_img : Tensor
            Input image to pass through the model.

        is_train : bool, optional
            Whether if the call is during training or inference.

        Returns
        -------
        prediction : Tensor
            Image prediction.
        """
        # ##### OPTION 1: we need batch size information as apply_preprocessing fails if the batch is not the same as the
        # ##### one fixed for the model. Last batch of the epoch can have less samples than batch size.
        # ##### Check torch.utils.data.DataLoader() drop last arg.
        # # Convert from Numpy to xarray.DataArray
        # self.bmz_axes = self.bmz_config['original_bmz_config'].inputs[0].axes
        # in_img = xr.DataArray(in_img.cpu().numpy(), dims=tuple(self.bmz_axes))

        # # Apply pre-processing
        # in_img = dict(zip([ipt.name for ipt in self.bmz_pipeline.input_specs], (in_img,)))
        # self.bmz_computed_measures = {}
        # self.bmz_pipeline.apply_preprocessing(in_img, self.bmz_computed_measures)
        # # print(f"in_img: {in_img['input0'].shape} {in_img['input0'].min()} {in_img['input0'].max()}")
        # # Predict
        # prediction = self.model(torch.from_numpy(np.array(in_img['input0'])).to(self.device))

        # # Apply post-processing (if any)
        # if bool(self.bmz_pipeline.output_specs[0].postprocessing):
        #     prediction = xr.DataArray(prediction.cpu().numpy(), dims=tuple(self.bmz_axes))
        #     prediction = dict(zip([out.name for out in self.bmz_pipeline.output_specs], prediction))
        #     self.bmz_pipeline.apply_postprocessing(prediction, self.bmz_computed_measures)

        #     # Convert back to Tensor
        #     prediction = torch.from_numpy(np.array(prediction)).to(self.device)

        ##### OPTION 2: Just a normal model call, but the pre and post need to be done in BiaPy
        prediction = self.model(in_img)

        return prediction

    @abstractmethod
    def torchvision_model_call(self, in_img, is_train=False):
        """
        Call a regular Pytorch model.

        Parameters
        ----------
        in_img : Tensor
            Input image to pass through the model.

        is_train : bool, optional
            Whether if the call is during training or inference.

        Returns
        -------
        prediction : Tensor
            Image prediction.
        """
        raise NotImplementedError

    def model_call_func(self, in_img, to_pytorch=True, is_train=False):
        """
        Call a regular Pytorch model.

        Parameters
        ----------
        in_img : Tensor
            Input image to pass through the model.

        to_pytorch : bool, optional
            Whether if the input image needs to be converted into pytorch format or not.

        is_train : bool, optional
            Whether if the call is during training or inference.

        Returns
        -------
        prediction : Tensor
            Image prediction.
        """
        if to_pytorch:
            in_img = to_pytorch_format(in_img, self.axis_order, self.device)
        if self.cfg.MODEL.SOURCE == "biapy":
            p = self.model(in_img)
        elif self.cfg.MODEL.SOURCE == "bmz":
            p = self.bmz_model_call(in_img, is_train)
        elif self.cfg.MODEL.SOURCE == "torchvision":
            p = self.torchvision_model_call(in_img, is_train)
        return p

    def prepare_model(self):
        """
        Build the model.
        """
        if self.model_prepared:
            print("Model already prepared!")
            return

        print("###############")
        print("# Build model #")
        print("###############")
        if self.cfg.MODEL.SOURCE == "biapy":
            (
                self.model,
                self.bmz_config["model_file"],
                self.bmz_config["model_name"],
                self.bmz_config["model_build_kwargs"],
            ) = build_model(self.cfg, self.job_identifier, self.device)
        elif self.cfg.MODEL.SOURCE == "torchvision":
            self.model, self.torchvision_preprocessing = build_torchvision_model(self.cfg, self.device)
        # BioImage Model Zoo pretrained models
        elif self.cfg.MODEL.SOURCE == "bmz":
            # Create a bioimage pipeline to create predictions
            try:
                self.bmz_pipeline = create_prediction_pipeline(
                    self.bmz_config["original_bmz_config"],
                    devices=None,
                    weight_format="torchscript",
                )
            except Exception as e:
                print(f"The error thrown during the BMZ model load was:\n{e}")
                raise ValueError(
                    "An error ocurred when creating the BMZ model (see above). "
                    "BiaPy only supports models prepared with Torchscript."
                )

            if self.args.distributed:
                raise ValueError("DDP can not be activated when loading a BMZ pretrained model")

            self.model = build_bmz_model(self.cfg, self.bmz_config["original_bmz_config"], self.device)

        self.model_without_ddp = self.model
        if self.args.distributed:
            find_unused_parameters = True if self.cfg.MODEL.ARCHITECTURE.lower() == "unetr" else False
            self.model = torch.nn.parallel.DistributedDataParallel(
                self.model,
                device_ids=[self.args.gpu],
                find_unused_parameters=find_unused_parameters,
            )
            self.model_without_ddp = self.model.module
        self.model_prepared = True

        # Load checkpoint if necessary
        if self.cfg.MODEL.SOURCE == "biapy" and self.cfg.MODEL.LOAD_CHECKPOINT:
            self.start_epoch, self.checkpoint_path = load_model_checkpoint(
                cfg=self.cfg,
                jobname=self.job_identifier,
                model_without_ddp=self.model_without_ddp,
                device=self.device,
                optimizer=self.optimizer,
                loss_scaler=self.loss_scaler,
            )
        else:
            self.start_epoch = 0

    def prepare_logging_tool(self):
        """
        Prepare looging tool.
        """
        print("#######################")
        print("# Prepare logging tool #")
        print("#######################")
        # To start the logging
        now = datetime.datetime.now()
        now = now.strftime("%Y_%m_%d_%H_%M_%S")
        self.log_file = os.path.join(
            self.cfg.LOG.LOG_DIR,
            self.cfg.LOG.LOG_FILE_PREFIX + "_log_" + str(now) + ".txt",
        )
        if self.global_rank == 0:
            os.makedirs(self.cfg.LOG.LOG_DIR, exist_ok=True)
            os.makedirs(self.cfg.PATHS.CHECKPOINT, exist_ok=True)
            self.log_writer = TensorboardLogger(log_dir=self.cfg.LOG.TENSORBOARD_LOG_DIR)
        else:
            self.log_writer = None

        self.plot_values = {}
        self.plot_values["loss"] = []
        self.plot_values["val_loss"] = []
        for i in range(len(self.train_metric_names)):
            self.plot_values[self.train_metric_names[i]] = []
            self.plot_values["val_" + self.train_metric_names[i]] = []

    def train(self):
        """
        Training phase.
        """
        self.load_train_data()
        if not self.model_prepared:
            self.prepare_model()
        self.prepare_train_generators()
        self.prepare_logging_tool()
        self.early_stopping = build_callbacks(self.cfg)

        self.optimizer, self.lr_scheduler, self.loss_scaler = prepare_optimizer(
            self.cfg, self.model_without_ddp, len(self.train_generator)
        )

        print("#####################")
        print("#  TRAIN THE MODEL  #")
        print("#####################")

        print(f"Start training in epoch {self.start_epoch+1} - Total: {self.cfg.TRAIN.EPOCHS}")
        start_time = time.time()
        self.val_best_metric = np.zeros(len(self.train_metric_names), dtype=np.float32)
        self.val_best_loss = np.Inf
        for epoch in range(self.start_epoch, self.cfg.TRAIN.EPOCHS):
            print("~~~ Epoch {}/{} ~~~\n".format(epoch + 1, self.cfg.TRAIN.EPOCHS))
            e_start = time.time()

            if self.args.distributed:
                self.train_generator.sampler.set_epoch(epoch)
            if self.log_writer is not None:
                self.log_writer.set_step(epoch * self.num_training_steps_per_epoch)

            # Train
            train_stats = train_one_epoch(
                self.cfg,
                model=self.model,
                model_call_func=self.model_call_func,
                loss_function=self.loss,
                activations=self.apply_model_activations,
                metric_function=self.metric_calculation,
                prepare_targets=self.prepare_targets,
                data_loader=self.train_generator,
                optimizer=self.optimizer,
                device=self.device,
                loss_scaler=self.loss_scaler,
                epoch=epoch,
                log_writer=self.log_writer,
                lr_scheduler=self.lr_scheduler,
                start_steps=epoch * self.num_training_steps_per_epoch,
                verbose=self.cfg.TRAIN.VERBOSE,
            )

            # Save checkpoint
            if self.cfg.MODEL.SAVE_CKPT_FREQ != -1:
                if (
                    (epoch + 1) % self.cfg.MODEL.SAVE_CKPT_FREQ == 0
                    or epoch + 1 == self.cfg.TRAIN.EPOCHS
                    and is_main_process()
                ):
                    save_model(
                        cfg=self.cfg,
                        jobname=self.job_identifier,
                        model=self.model,
                        model_without_ddp=self.model_without_ddp,
                        optimizer=self.optimizer,
                        loss_scaler=self.loss_scaler,
                        epoch=epoch + 1,
                    )

            # Validation
            if self.val_generator is not None:
                test_stats = evaluate(
                    self.cfg,
                    model=self.model,
                    model_call_func=self.model_call_func,
                    loss_function=self.loss,
                    activations=self.apply_model_activations,
                    metric_function=self.metric_calculation,
                    prepare_targets=self.prepare_targets,
                    epoch=epoch,
                    data_loader=self.val_generator,
                    lr_scheduler=self.lr_scheduler,
                )

                # Save checkpoint is val loss improved
                if test_stats["loss"] < self.val_best_loss:
                    f = os.path.join(
                        self.cfg.PATHS.CHECKPOINT,
                        "{}-checkpoint-best.pth".format(self.job_identifier),
                    )
                    print(
                        "Val loss improved from {} to {}, saving model to {}".format(
                            self.val_best_loss, test_stats["loss"], f
                        )
                    )
                    m = " "
                    for i in range(len(self.val_best_metric)):
                        self.val_best_metric[i] = test_stats[self.train_metric_names[i]]
                        m += f"{self.train_metric_names[i]}: {self.val_best_metric[i]:.4f} "
                    self.val_best_loss = test_stats["loss"]

                    if is_main_process():
                        self.checkpoint_path = save_model(
                            cfg=self.cfg,
                            jobname=self.job_identifier,
                            model=self.model,
                            model_without_ddp=self.model_without_ddp,
                            optimizer=self.optimizer,
                            loss_scaler=self.loss_scaler,
                            epoch="best",
                        )
                print(f"[Val] best loss: {self.val_best_loss:.4f} best " + m)

                # Store validation stats
                if self.log_writer is not None:
                    self.log_writer.update(test_loss=test_stats["loss"], head="perf", step=epoch)
                    for i in range(len(self.train_metric_names)):
                        self.log_writer.update(
                            test_iou=test_stats[self.train_metric_names[i]],
                            head="perf",
                            step=epoch,
                        )

                log_stats = {
                    **{f"train_{k}": v for k, v in train_stats.items()},
                    **{f"test_{k}": v for k, v in test_stats.items()},
                    "epoch": epoch,
                }
            else:
                log_stats = {
                    **{f"train_{k}": v for k, v in train_stats.items()},
                    "epoch": epoch,
                }

            # Write statistics in the logging file
            if is_main_process():
                # Log epoch stats
                if self.log_writer is not None:
                    self.log_writer.flush()
                with open(self.log_file, mode="a", encoding="utf-8") as f:
                    f.write(json.dumps(log_stats) + "\n")

                # Create training plot
                self.plot_values["loss"].append(train_stats["loss"])
                if self.val_generator is not None:
                    self.plot_values["val_loss"].append(test_stats["loss"])
                for i in range(len(self.train_metric_names)):
                    self.plot_values[self.train_metric_names[i]].append(train_stats[self.train_metric_names[i]])
                    if self.val_generator is not None:
                        self.plot_values["val_" + self.train_metric_names[i]].append(
                            test_stats[self.train_metric_names[i]]
                        )
                if (epoch + 1) % self.cfg.LOG.CHART_CREATION_FREQ == 0:
                    create_plots(
                        self.plot_values,
                        self.train_metric_names,
                        self.job_identifier,
                        self.cfg.PATHS.CHARTS,
                    )

            if self.val_generator is not None and self.early_stopping is not None:
                self.early_stopping(test_stats["loss"])
                if self.early_stopping.early_stop:
                    print("Early stopping")
                    break

            e_end = time.time()
            t_epoch = e_end - e_start
            print(
                "[Time] {} {}/{}\n".format(
                    time_text(t_epoch),
                    time_text(e_end - start_time),
                    time_text((e_end - start_time) + (t_epoch * (self.cfg.TRAIN.EPOCHS - epoch))),
                )
            )

        total_time = time.time() - start_time
        self.total_training_time_str = str(datetime.timedelta(seconds=int(total_time)))
        print("Training time: {}".format(self.total_training_time_str))

        print("Train loss: {}".format(train_stats["loss"]))
        for i in range(len(self.train_metric_names)):
            print("Train {}: {}".format(self.train_metric_names[i], train_stats[self.train_metric_names[i]]))
        if self.val_generator is not None:
            print("Validation loss: {}".format(self.val_best_loss))
            for i in range(len(self.train_metric_names)):
                print("Validation {}: {}".format(self.train_metric_names[i], self.val_best_metric[i]))

        print("Finished Training")

        # Save two samples to export the model to BMZ
        if "test_input" not in self.bmz_config:
            sample = next(enumerate(self.train_generator))
            self.bmz_config["test_input"] = sample[1][0][0]
            self.bmz_config["test_output"] = sample[1][1]
            if not isinstance(self.bmz_config["test_output"], int):
                self.bmz_config["test_output"] = self.bmz_config["test_output"][0]

        self.destroy_train_data()

    def load_test_data(self):
        """
        Load test data.
        """
        if self.cfg.TEST.ENABLE:
            print("######################")
            print("#   LOAD TEST DATA   #")
            print("######################")
            if not self.cfg.DATA.TEST.USE_VAL_AS_TEST:
                if self.cfg.DATA.TEST.IN_MEMORY:
                    print("2) Loading test images . . .")
                    f_name = load_data_from_dir if self.cfg.PROBLEM.NDIM == "2D" else load_3d_images_from_dir
                    preprocess_cfg = self.cfg.DATA.PREPROCESS if self.cfg.DATA.PREPROCESS.TEST else None
                    preprocess_fn = preprocess_data if self.cfg.DATA.PREPROCESS.TEST else None
                    is_y_mask = self.cfg.PROBLEM.TYPE in [
                        "SEMANTIC_SEG",
                        "INSTANCE_SEG",
                    ]
                    self.X_test, _, _ = f_name(
                        self.cfg.DATA.TEST.PATH,
                        convert_to_rgb=self.cfg.DATA.FORCE_RGB,
                        preprocess_cfg=preprocess_cfg,
                        is_mask=False,
                        preprocess_f=preprocess_fn,
                    )
                    if self.cfg.DATA.TEST.LOAD_GT:
                        print("3) Loading test masks . . .")
                        self.Y_test, _, _ = f_name(
                            self.cfg.DATA.TEST.GT_PATH,
                            check_channel=False,
                            check_drange=False,
                            preprocess_cfg=preprocess_cfg,
                            is_mask=is_y_mask,
                            preprocess_f=preprocess_fn,
                        )
                        if len(self.X_test) != len(self.Y_test):
                            raise ValueError(
                                "Different number of raw and ground truth items ({} vs {}). "
                                "Please check the data!".format(len(self.X_test), len(self.Y_test))
                            )
                    else:
                        self.Y_test = None
                else:
                    self.X_test, self.Y_test = None, None

                if self.original_test_path is None:
                    self.test_filenames = sorted(next(os.walk(self.cfg.DATA.TEST.PATH))[2])
                    if len(self.test_filenames) == 0:
                        self.test_filenames = sorted(next(os.walk(self.cfg.DATA.TEST.PATH))[1])
                else:
                    self.test_filenames = sorted(next(os.walk(self.original_test_path))[2])
                    if len(self.test_filenames) == 0:
                        self.test_filenames = sorted(next(os.walk(self.original_test_path))[1])
            else:
                # The test is the validation, and as it is only available when validation is obtained from train and when
                # cross validation is enabled, the test set files reside in the train folder
                self.test_filenames = sorted(next(os.walk(self.cfg.DATA.TRAIN.PATH))[2])
                self.X_test, self.Y_test = None, None
                if self.cross_val_samples_ids is None:
                    # Split the test as it was the validation when train is not enabled
                    skf = StratifiedKFold(
                        n_splits=self.cfg.DATA.VAL.CROSS_VAL_NFOLD,
                        shuffle=self.cfg.DATA.VAL.RANDOM,
                        random_state=self.cfg.SYSTEM.SEED,
                    )
                    fold = 1
                    test_index = None
                    A = B = np.zeros(len(self.test_filenames))

                    for _, te_index in skf.split(A, B):
                        if self.cfg.DATA.VAL.CROSS_VAL_FOLD == fold:
                            self.cross_val_samples_ids = te_index.copy()
                            break
                        fold += 1
                    if len(self.cross_val_samples_ids) > 5:
                        print(
                            "Fold number {} used for test data. Printing the first 5 ids: {}".format(
                                fold, self.cross_val_samples_ids[:5]
                            )
                        )
                    else:
                        print(
                            "Fold number {}. Indexes used in cross validation: {}".format(
                                fold, self.cross_val_samples_ids
                            )
                        )

                if self.cross_val_samples_ids is not None:
                    self.test_filenames = [
                        x for i, x in enumerate(self.test_filenames) if i in self.cross_val_samples_ids
                    ]
                self.original_test_path = self.orig_train_path
                self.original_test_mask_path = self.orig_train_mask_path

    def destroy_test_data(self):
        """
        Delete test variable to release memory.
        """
        print("Releasing memory . . .")
        if "X_test" in locals() or "X_test" in globals():
            del self.X_test
        if "Y_test" in locals() or "Y_test" in globals():
            del self.Y_test
        if "test_generator" in locals() or "test_generator" in globals():
            del self.test_generator
        if "_X" in locals() or "_X" in globals():
            del self._X
        if "_Y" in locals() or "_Y" in globals():
            del self._Y

    def prepare_test_generators(self):
        """
        Prepare test data generator.
        """
        if self.cfg.TEST.ENABLE:
            print("############################")
            print("#  PREPARE TEST GENERATOR  #")
            print("############################")
            self.test_generator, self.data_norm = create_test_augmentor(
                self.cfg, self.X_test, self.Y_test, self.cross_val_samples_ids
            )

    def apply_model_activations(self, pred, training=False):
        """
        Function that apply the last activation (if any) to the model's output.

        Parameters
        ----------
        pred : Torch Tensor
            Predictions of the model.

        training : bool, optional
            To advice the function if this is being applied during training of inference. During training,
            ``CE_Sigmoid`` activations will NOT be applied, as ``torch.nn.BCEWithLogitsLoss`` will apply
            ``Sigmoid`` automatically in a way that is more stable numerically
            (`ref <https://pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html>`_).

        Returns
        -------
        pred : Torch tensor
            Resulting predictions after applying last activation(s).
        """
        # Not apply the activation, as it will be done in the BMZ model
        if self.cfg.MODEL.SOURCE == "bmz":
            return pred

        if not isinstance(pred, list):
            multiple_heads = False
            pred = [pred]
        else:
            multiple_heads = True
            assert len(pred) == len(
                self.activations
            ), "Activations length need to match prediction list length in multiple heads setting"

        for out_heads in range(len(pred)):
            for key, value in self.activations[out_heads].items():
                # Ignore CE_Sigmoid as torch.nn.BCEWithLogitsLoss will apply Sigmoid automatically in a way
                # that is more stable numerically (ref: https://pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html)
                if (training and value not in ["Linear", "CE_Sigmoid"]) or (not training and value != "Linear"):
                    value = "Sigmoid" if value == "CE_Sigmoid" else value
                    act = getattr(torch.nn, value)()
                    if key == ":":
                        pred[out_heads] = act(pred[out_heads])
                    else:
                        pred[out_heads][:, int(key), ...] = act(pred[out_heads][:, int(key), ...])

        if not multiple_heads:
            return pred[0]
        else:
            return pred

    @torch.no_grad()
    def test(self):
        """
        Test/Inference step.
        """
        self.load_test_data()
        if not self.model_prepared:
            self.prepare_model()
        self.prepare_test_generators()

        # Switch to evaluation mode
        if self.cfg.MODEL.SOURCE != "bmz":
            self.model_without_ddp.eval()

        # Load best checkpoint on validation
        if self.cfg.TRAIN.ENABLE and self.cfg.MODEL.SOURCE == "biapy":
            self.start_epoch, self.checkpoint_path = load_model_checkpoint(
                cfg=self.cfg,
                jobname=self.job_identifier,
                model_without_ddp=self.model_without_ddp,
                device=self.device,
            )

        # Check possible checkpoint problems
        if self.start_epoch == -1:
            raise ValueError("There was a problem loading the checkpoint. Test phase aborted!")

        image_counter = 0

        print("###############")
        print("#  INFERENCE  #")
        print("###############")
        print("Making predictions on test data . . .")

        # Reactivate prints to see each rank progress
        if self.cfg.TEST.BY_CHUNKS.ENABLE and self.cfg.PROBLEM.NDIM == "3D":
            setup_for_distributed(True)

        # Process all the images
        for i, gen_obj in tqdm(
            enumerate(self.test_generator),
            total=len(self.test_generator),
            disable=not is_main_process(),
        ):
            self._X, X_norm, self._Y, Y_norm = None, None, None, None
            if "X" in gen_obj:
                self._X = gen_obj["X"]
            if "X_norm" in gen_obj:
                X_norm = gen_obj["X_norm"]
            if "Y" in gen_obj:
                self._Y = gen_obj["Y"]
            if "Y_norm" in gen_obj:
                Y_norm = gen_obj["Y_norm"]
            self.processing_filenames = (
                self.test_filenames[gen_obj["file"]] if isinstance(gen_obj["file"], int) else gen_obj["file"]
            )
            self.processing_filenames = [os.path.basename(self.processing_filenames)]
            self.f_numbers = [i]
            del gen_obj

            if self.cfg.TEST.BY_CHUNKS.ENABLE and self.cfg.PROBLEM.NDIM == "3D":
                print(f"[Rank {get_rank()} ({os.getpid()})] Processing image(s): {self.processing_filenames[0]}")
                self.process_test_sample_by_chunks(self.processing_filenames[0])
            else:
                if is_main_process():
                    print("Processing image: {}".format(self.processing_filenames[0]))
                    self.process_test_sample(norm=(X_norm, Y_norm))

            image_counter += 1

        self.destroy_test_data()

        if is_main_process():
            self.after_all_images()

            print("#############")
            print("#  RESULTS  #")
            print("#############")

            if self.cfg.TRAIN.ENABLE:
                print("Epoch number: {}".format(len(self.plot_values["val_loss"])))
                print("Train time (s): {}".format(self.total_training_time_str))
                print("Train loss: {}".format(np.min(self.plot_values["loss"])))

                for i in range(len(self.train_metric_names)):
                    metric_name = (
                        "Foreground IoU" if self.train_metric_names[i] == "IoU" else self.train_metric_names[i]
                    )
                    print(
                        "Train {}: {}".format(
                            metric_name,
                            (
                                np.max(self.plot_values[self.train_metric_names[i]])
                                if self.train_metric_best[i] == "max"
                                else np.min(self.plot_values[self.train_metric_names[i]])
                            ),
                        )
                    )
                print("Validation loss: {}".format(self.val_best_loss))
                for i in range(len(self.train_metric_names)):
                    metric_name = (
                        "Foreground IoU" if self.train_metric_names[i] == "IoU" else self.train_metric_names[i]
                    )
                    print(
                        "Validation {}: {}".format(
                            metric_name,
                            self.val_best_metric[i],
                        )
                    )
            self.print_stats(image_counter)

    def process_test_sample_by_chunks(self, filenames):
        """
        Function to process a sample in the inference phase. A final H5/Zarr file is created in "TZCYX" or "TZYXC" order
        depending on ``TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER`` ('T' is always included).

        Parameters
        ----------
        filenames : List of str
            Filenames fo the samples to process.
        """
        filename, file_extension = os.path.splitext(filenames)
        ext = ".h5" if self.cfg.TEST.BY_CHUNKS.FORMAT == "h5" else ".zarr"
        out_data_div_filename = os.path.join(self.cfg.PATHS.RESULT_DIR.PER_IMAGE, filename + ext)

        if not self.cfg.TEST.REUSE_PREDICTIONS:
            if file_extension not in [".hdf5", ".h5", ".zarr"]:
                print(
                    "WARNING: you could have saved more memory by converting input test images into H5 file format (.h5) "
                    "or Zarr (.zarr) as with 'TEST.BY_CHUNKS.ENABLE' option enabled H5/Zarr files will be processed by chunks"
                )
            # Load data
            if file_extension in [".hdf5", ".h5", ".zarr"]:
                self._X_file, self._X = read_chunked_data(self._X)
            else:  # Numpy array
                if self._X.ndim == 3:
                    c_pos = -1 if self.cfg.TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER[-1] == "C" else 1
                    self._X = np.expand_dims(self._X, c_pos)

            if is_main_process():
                print(f"Loaded image shape is {self._X.shape}")

            data_shape = self._X.shape
            out_data_shape = [x * y for x, y in zip(data_shape, self.cfg.DATA.PREPROCESS.ZOOM.ZOOM_FACTOR)]

            if self._X.ndim < 3:
                raise ValueError(
                    "Loaded image need to have at least 3 dimensions: {} (ndim: {})".format(self._X.shape, self._X.ndim)
                )

            if len(self.cfg.TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER) != self._X.ndim:
                raise ValueError(
                    "'TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER' value {} does not match the number of dimensions of the loaded H5/Zarr "
                    "file {} (ndim: {})".format(
                        self.cfg.TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER,
                        self._X.shape,
                        self._X.ndim,
                    )
                )

            # Data paths
            os.makedirs(self.cfg.PATHS.RESULT_DIR.PER_IMAGE, exist_ok=True)
            if self.cfg.SYSTEM.NUM_GPUS > 1:
                out_data_filename = os.path.join(
                    self.cfg.PATHS.RESULT_DIR.PER_IMAGE,
                    filename + "_part" + str(get_rank()) + ext,
                )
                out_data_mask_filename = os.path.join(
                    self.cfg.PATHS.RESULT_DIR.PER_IMAGE,
                    filename + "_part" + str(get_rank()) + "_mask" + ext,
                )
            else:
                out_data_filename = os.path.join(self.cfg.PATHS.RESULT_DIR.PER_IMAGE, filename + "_nodiv" + ext)
                out_data_mask_filename = os.path.join(self.cfg.PATHS.RESULT_DIR.PER_IMAGE, filename + "_mask" + ext)
            in_data = self._X

            # Process in charge of processing one predicted patch
            output_handle_proc = mp.Process(
                target=insert_patch_into_dataset,
                args=(
                    out_data_filename,
                    out_data_mask_filename,
                    out_data_shape,
                    self.output_queue,
                    self.extract_info_queue,
                    self.cfg,
                    self.dtype_str,
                    self.dtype,
                    self.cfg.TEST.BY_CHUNKS.FORMAT,
                    self.cfg.TEST.VERBOSE,
                ),
            )
            output_handle_proc.daemon = True
            output_handle_proc.start()

            # Process in charge of loading part of the data
            load_data_process = mp.Process(
                target=extract_patch_from_dataset,
                args=(
                    in_data,
                    self.cfg,
                    self.input_queue,
                    self.extract_info_queue,
                    self.cfg.TEST.VERBOSE,
                ),
            )
            load_data_process.daemon = True
            load_data_process.start()

            if "_X_file" in locals() and isinstance(self._X_file, h5py.File):
                self._X_file.close()
            del self._X, in_data

            # Lock the thread inferring until no more patches
            if self.cfg.TEST.VERBOSE and self.cfg.SYSTEM.NUM_GPUS > 1:
                print(f"[Rank {get_rank()} ({os.getpid()})] Doing inference ")
            while True:
                obj = self.input_queue.get(timeout=60)
                if obj == None:
                    break

                img, patch_coords = obj
                img, _ = self.test_generator.norm_X(img)
                if self.cfg.TEST.AUGMENTATION:
                    p = ensemble16_3d_predictions(
                        img[0],
                        batch_size_value=self.cfg.TRAIN.BATCH_SIZE,
                        axis_order_back=self.axis_order_back,
                        pred_func=self.model_call_func,
                        axis_order=self.axis_order,
                        device=self.device,
                        mode=self.cfg.TEST.AUGMENTATION_MODE,
                    )
                else:
                    with torch.cuda.amp.autocast():
                        p = self.model_call_func(img)
                p = self.apply_model_activations(p)
                # Multi-head concatenation
                if isinstance(p, list):
                    p = torch.cat((p[0], torch.argmax(p[1], axis=1).unsqueeze(1)), dim=1)
                p = to_numpy_format(p, self.axis_order_back)

                t_dim, z_dim, y_dim, x_dim, c_dim = order_dimensions(
                    self.cfg.DATA.PREPROCESS.ZOOM.ZOOM_FACTOR,
                    input_order=self.cfg.TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER,
                    output_order="TZYXC",
                    default_value=1,
                )

                # Create a mask with the overlap. Calculate the exact part of the patch that will be inserted in the
                # final H5/Zarr file
                p = p[
                    0,
                    z_dim * self.cfg.DATA.TEST.PADDING[0] : p.shape[1] - z_dim * self.cfg.DATA.TEST.PADDING[0],
                    y_dim * self.cfg.DATA.TEST.PADDING[1] : p.shape[2] - y_dim * self.cfg.DATA.TEST.PADDING[1],
                    x_dim * self.cfg.DATA.TEST.PADDING[2] : p.shape[3] - x_dim * self.cfg.DATA.TEST.PADDING[2],
                ]
                m = np.ones(p.shape, dtype=np.uint8)
                patch_coords = np.array(
                    [patch_coords[:, 0], patch_coords[:, 0] + np.array(p.shape)[:-1]]
                ).T  # should not be necessary?

                # Put the prediction into queue
                self.output_queue.put([p, m, patch_coords])

            # Get some auxiliar variables
            self.stats["patch_by_batch_counter"] = self.extract_info_queue.get(timeout=60)
            if is_main_process():
                z_vol_info = self.extract_info_queue.get(timeout=60)
                list_of_vols_in_z = self.extract_info_queue.get(timeout=60)
            load_data_process.join()
            output_handle_proc.join()

        # Wait until all threads are done so the main thread can create the full size image
        if self.cfg.SYSTEM.NUM_GPUS > 1:
            if self.cfg.TEST.VERBOSE:
                print(f"[Rank {get_rank()} ({os.getpid()})] Finish sample inference ")
            if is_dist_avail_and_initialized():
                dist.barrier()

        # Create the final H5/Zarr file that contains all the individual parts
        if is_main_process():
            if not self.cfg.TEST.REUSE_PREDICTIONS:
                if "C" not in self.cfg.TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER:
                    out_data_order = self.cfg.TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER + "C"
                    c_index = -1
                else:
                    out_data_order = self.cfg.TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER
                    c_index = out_data_order.index("C")

                if self.cfg.SYSTEM.NUM_GPUS > 1:
                    # Obtain parts of the data created by all GPUs
                    if self.cfg.TEST.BY_CHUNKS.FORMAT == "h5":
                        data_parts_filenames = sorted(next(os.walk(self.cfg.PATHS.RESULT_DIR.PER_IMAGE))[2])
                    else:
                        data_parts_filenames = sorted(next(os.walk(self.cfg.PATHS.RESULT_DIR.PER_IMAGE))[1])
                    parts = []
                    mask_parts = []
                    for x in data_parts_filenames:
                        if filename + "_part" in x and x.endswith(self.cfg.TEST.BY_CHUNKS.FORMAT):
                            if "_mask" not in x:
                                parts.append(x)
                            else:
                                mask_parts.append(x)
                    data_parts_filenames = parts
                    data_parts_mask_filenames = mask_parts
                    del parts, mask_parts

                    if max(1, self.cfg.SYSTEM.NUM_GPUS) != len(data_parts_filenames) != len(list_of_vols_in_z):
                        raise ValueError("Number of data parts is not the same as number of GPUs")

                    # Compose the large image
                    for i, data_part_fname in enumerate(data_parts_filenames):
                        print("Reading {}".format(os.path.join(self.cfg.PATHS.RESULT_DIR.PER_IMAGE, data_part_fname)))
                        data_part_file, data_part = read_chunked_data(
                            os.path.join(self.cfg.PATHS.RESULT_DIR.PER_IMAGE, data_part_fname)
                        )
                        data_mask_part_file, data_mask_part = read_chunked_data(
                            os.path.join(
                                self.cfg.PATHS.RESULT_DIR.PER_IMAGE,
                                data_parts_mask_filenames[i],
                            )
                        )

                        if "data" not in locals():
                            all_data_filename = os.path.join(self.cfg.PATHS.RESULT_DIR.PER_IMAGE, filename + ext)
                            if self.cfg.TEST.BY_CHUNKS.FORMAT == "h5":
                                allfile = h5py.File(all_data_filename, "w")
                                data = allfile.create_dataset(
                                    "data",
                                    data_part.shape,
                                    dtype=self.dtype_str,
                                    compression="gzip",
                                )
                            else:
                                allfile = zarr.open_group(all_data_filename, mode="w")
                                data = allfile.create_dataset(
                                    "data",
                                    shape=data_part.shape,
                                    dtype=self.dtype_str,
                                    compression="gzip",
                                )

                        for j, k in enumerate(list_of_vols_in_z[i]):

                            slices = (
                                slice(z_vol_info[k][0], z_vol_info[k][1]),  # z (only z axis is distributed across GPUs)
                                slice(None),  # y
                                slice(None),  # x
                                slice(None),  # Channel
                            )

                            data_ordered_slices = order_dimensions(
                                slices,
                                input_order="ZYXC",
                                output_order=out_data_order,
                                default_value=0,
                            )

                            if self.cfg.TEST.VERBOSE:
                                print(f"Filling {k} [{z_vol_info[k][0]}:{z_vol_info[k][1]}]")
                            data[data_ordered_slices] = (
                                data_part[data_ordered_slices] / data_mask_part[data_ordered_slices]
                            )

                            if self.cfg.TEST.BY_CHUNKS.FORMAT == "h5":
                                allfile.flush()

                        if self.cfg.TEST.BY_CHUNKS.FORMAT == "h5":
                            data_part_file.close()
                            data_mask_part_file.close()

                    # Save image
                    if self.cfg.TEST.BY_CHUNKS.SAVE_OUT_TIF and self.cfg.PATHS.RESULT_DIR.PER_IMAGE != "":
                        current_order = np.array(range(len(data.shape)))
                        transpose_order = order_dimensions(
                            current_order,
                            input_order=out_data_order,
                            output_order="TZYXC",
                            default_value=np.nan,
                        )
                        transpose_order = [x for x in transpose_order if not np.isnan(x)]
                        data = np.array(data, dtype=self.dtype).transpose(transpose_order)
                        if "T" not in out_data_order:
                            data = np.expand_dims(data, 0)

                        save_tif(
                            data,
                            self.cfg.PATHS.RESULT_DIR.PER_IMAGE,
                            [filename + ".tif"],
                            verbose=self.cfg.TEST.VERBOSE,
                        )

                    if self.cfg.TEST.BY_CHUNKS.FORMAT == "h5":
                        allfile.close()

                # Just make the division with the overlap
                else:
                    # Load predictions and overlapping mask
                    pred_file, pred = read_chunked_data(out_data_filename)
                    mask_file, mask = read_chunked_data(out_data_mask_filename)

                    # Create new file
                    if self.cfg.TEST.BY_CHUNKS.FORMAT == "h5":
                        fid_div = h5py.File(out_data_div_filename, "w")
                        pred_div = fid_div.create_dataset("data", pred.shape, dtype=pred.dtype, compression="gzip")
                    else:
                        fid_div = zarr.open_group(out_data_div_filename, mode="w")
                        pred_div = fid_div.create_dataset("data", shape=pred.shape, dtype=pred.dtype)

                    t_dim, z_dim, c_dim, y_dim, x_dim = order_dimensions(
                        out_data_shape, self.cfg.TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER
                    )

                    # Fill the new data
                    z_vols = math.ceil(z_dim / self.cfg.DATA.PATCH_SIZE[0])
                    y_vols = math.ceil(y_dim / self.cfg.DATA.PATCH_SIZE[1])
                    x_vols = math.ceil(x_dim / self.cfg.DATA.PATCH_SIZE[2])
                    for z in tqdm(range(z_vols), disable=not is_main_process()):
                        for y in range(y_vols):
                            for x in range(x_vols):

                                slices = (
                                    slice(
                                        z * self.cfg.DATA.PATCH_SIZE[0],
                                        min(z_dim, self.cfg.DATA.PATCH_SIZE[0] * (z + 1)),
                                    ),
                                    slice(
                                        y * self.cfg.DATA.PATCH_SIZE[1],
                                        min(y_dim, self.cfg.DATA.PATCH_SIZE[1] * (y + 1)),
                                    ),
                                    slice(
                                        x * self.cfg.DATA.PATCH_SIZE[2],
                                        min(x_dim, self.cfg.DATA.PATCH_SIZE[2] * (x + 1)),
                                    ),
                                    slice(0, pred.shape[c_index]),  # Channel
                                )

                                data_ordered_slices = order_dimensions(
                                    slices,
                                    input_order="ZYXC",
                                    output_order=out_data_order,
                                    default_value=0,
                                )
                                pred_div[data_ordered_slices] = pred[data_ordered_slices] / mask[data_ordered_slices]

                        if self.cfg.TEST.BY_CHUNKS.FORMAT == "h5":
                            fid_div.flush()

                    # Save image
                    if self.cfg.TEST.BY_CHUNKS.SAVE_OUT_TIF and self.cfg.PATHS.RESULT_DIR.PER_IMAGE != "":
                        current_order = np.array(range(len(pred_div.shape)))
                        transpose_order = order_dimensions(
                            current_order,
                            input_order=out_data_order,
                            output_order="TZYXC",
                            default_value=np.nan,
                        )
                        transpose_order = [x for x in transpose_order if not np.isnan(x)]
                        pred_div = np.array(pred_div, dtype=self.dtype).transpose(transpose_order)
                        if "T" not in out_data_order:
                            pred_div = np.expand_dims(pred_div, 0)

                        save_tif(
                            pred_div,
                            self.cfg.PATHS.RESULT_DIR.PER_IMAGE,
                            [
                                os.path.join(
                                    self.cfg.PATHS.RESULT_DIR.PER_IMAGE,
                                    filename + ".tif",
                                )
                            ],
                            verbose=self.cfg.TEST.VERBOSE,
                        )

                    if self.cfg.TEST.BY_CHUNKS.FORMAT == "h5":
                        pred_file.close()
                        mask_file.close()
                        fid_div.close()

            if self.cfg.TEST.BY_CHUNKS.WORKFLOW_PROCESS:
                if self.cfg.TEST.BY_CHUNKS.WORKFLOW_PROCESS.TYPE == "chunk_by_chunk":
                    self.after_merge_patches_by_chunks_proccess_patch(out_data_div_filename)
                else:
                    self.after_merge_patches_by_chunks_proccess_entire_pred(out_data_div_filename)

        # Wait until the main thread is done to predict the next sample
        if self.cfg.SYSTEM.NUM_GPUS > 1:
            if self.cfg.TEST.VERBOSE:
                print(f"[Rank {get_rank()} ({os.getpid()})] Process waiting . . . ")
            if is_dist_avail_and_initialized():
                dist.barrier()
            if self.cfg.TEST.VERBOSE:
                print(f"[Rank {get_rank()} ({os.getpid()})] Synched with main thread. Go for the next sample")

    def process_test_sample(self, norm):
        """
        Function to process a sample in the inference phase.

        Parameters
        ----------
        norm : List of dicts
            Normalization used during training. Required to denormalize the predictions of the model.
        """
        # Data channel check
        if self.cfg.DATA.PATCH_SIZE[-1] != self._X.shape[-1]:
            raise ValueError(
                "Channel of the DATA.PATCH_SIZE given {} does not correspond with the loaded image {}. "
                "Please, check the channels of the images!".format(self.cfg.DATA.PATCH_SIZE[-1], self._X.shape[-1])
            )

        # Save test_input if the user wants to export the model to BMZ later
        if "test_input" not in self.bmz_config:
            if self.cfg.PROBLEM.NDIM == "2D":
                self.bmz_config["test_input"] = self._X[0][
                    : self.cfg.DATA.PATCH_SIZE[0], : self.cfg.DATA.PATCH_SIZE[1]
                ].copy()
            else:
                self.bmz_config["test_input"] = self._X[0][
                    : self.cfg.DATA.PATCH_SIZE[0], : self.cfg.DATA.PATCH_SIZE[1], : self.cfg.DATA.PATCH_SIZE[2]
                ].copy()

        #################
        ### PER PATCH ###
        #################
        if not self.cfg.TEST.FULL_IMG or self.cfg.PROBLEM.NDIM == "3D":
            if not self.cfg.TEST.REUSE_PREDICTIONS:
                # Reflect data to complete the needed shape
                if self.cfg.DATA.REFLECT_TO_COMPLETE_SHAPE:
                    reflected_orig_shape = self._X.shape
                    self._X = np.expand_dims(
                        pad_and_reflect(
                            self._X[0],
                            self.cfg.DATA.PATCH_SIZE,
                            verbose=self.cfg.TEST.VERBOSE,
                        ),
                        0,
                    )
                    if self._Y is not None:
                        self._Y = np.expand_dims(
                            pad_and_reflect(
                                self._Y[0],
                                self.cfg.DATA.PATCH_SIZE,
                                verbose=self.cfg.TEST.VERBOSE,
                            ),
                            0,
                        )

                original_data_shape = self._X.shape

                # Crop if necessary
                if self._X.shape[1:-1] != self.cfg.DATA.PATCH_SIZE[:-1]:
                    # Copy X to be used later in full image
                    if self.cfg.PROBLEM.NDIM != "3D":
                        X_original = self._X.copy()

                    if self._Y is not None and self._X.shape[:-1] != self._Y.shape[:-1]:
                        raise ValueError(
                            "Image {} and mask {} differ in shape (without considering the channels, i.e. last dimension)".format(
                                self._X.shape, self._Y.shape
                            )
                        )

                    if self.cfg.PROBLEM.NDIM == "2D":
                        obj = crop_data_with_overlap(
                            self._X,
                            self.cfg.DATA.PATCH_SIZE,
                            data_mask=self._Y,
                            overlap=self.cfg.DATA.TEST.OVERLAP,
                            padding=self.cfg.DATA.TEST.PADDING,
                            verbose=self.cfg.TEST.VERBOSE,
                        )
                        if self._Y is not None:
                            self._X, self._Y = obj
                        else:
                            self._X = obj
                        del obj
                    else:
                        if self.cfg.TEST.REDUCE_MEMORY:
                            self._X = crop_3D_data_with_overlap(
                                self._X[0],
                                self.cfg.DATA.PATCH_SIZE,
                                overlap=self.cfg.DATA.TEST.OVERLAP,
                                padding=self.cfg.DATA.TEST.PADDING,
                                verbose=self.cfg.TEST.VERBOSE,
                                median_padding=self.cfg.DATA.TEST.MEDIAN_PADDING,
                            )
                            if self._Y is not None:
                                self._Y = crop_3D_data_with_overlap(
                                    self._Y[0],
                                    self.cfg.DATA.PATCH_SIZE[:-1] + (self._Y.shape[-1],),
                                    overlap=self.cfg.DATA.TEST.OVERLAP,
                                    padding=self.cfg.DATA.TEST.PADDING,
                                    verbose=self.cfg.TEST.VERBOSE,
                                    median_padding=self.cfg.DATA.TEST.MEDIAN_PADDING,
                                )
                        else:
                            if self._Y is not None:
                                self._Y = self._Y[0]
                            obj = crop_3D_data_with_overlap(
                                self._X[0],
                                self.cfg.DATA.PATCH_SIZE,
                                data_mask=self._Y,
                                overlap=self.cfg.DATA.TEST.OVERLAP,
                                padding=self.cfg.DATA.TEST.PADDING,
                                verbose=self.cfg.TEST.VERBOSE,
                                median_padding=self.cfg.DATA.TEST.MEDIAN_PADDING,
                            )
                            if self._Y is not None:
                                self._X, self._Y = obj
                            else:
                                self._X = obj
                            del obj

                # Predict each patch
                if self.cfg.TEST.AUGMENTATION:
                    for k in tqdm(range(self._X.shape[0]), leave=False):
                        if self.cfg.PROBLEM.NDIM == "2D":
                            p = ensemble8_2d_predictions(
                                self._X[k],
                                axis_order_back=self.axis_order_back,
                                pred_func=self.model_call_func,
                                axis_order=self.axis_order,
                                device=self.device,
                                mode=self.cfg.TEST.AUGMENTATION_MODE,
                            )
                        else:
                            p = ensemble16_3d_predictions(
                                self._X[k],
                                batch_size_value=self.cfg.TRAIN.BATCH_SIZE,
                                axis_order_back=self.axis_order_back,
                                pred_func=self.model_call_func,
                                axis_order=self.axis_order,
                                device=self.device,
                                mode=self.cfg.TEST.AUGMENTATION_MODE,
                            )
                        p = self.apply_model_activations(p)
                        # Multi-head concatenation
                        if isinstance(p, list):
                            p = torch.cat((p[0], torch.argmax(p[1], axis=1).unsqueeze(1)), dim=1)

                        # Calculate the metrics
                        if self._Y is not None:
                            metric_values = self.metric_calculation(
                                p,
                                to_pytorch_format(
                                    self._Y[k],
                                    self.axis_order,
                                    self.device,
                                    dtype=self.loss_dtype,
                                ),
                                train=False,
                            )
                            for metric in metric_values:
                                if str(metric).lower() not in self.stats["per_crop"]:
                                    self.stats["per_crop"][str(metric).lower()] = 0
                                self.stats["per_crop"][str(metric).lower()] += metric_values[metric]
                        self.stats["patch_by_batch_counter"] += 1

                        p = to_numpy_format(p, self.axis_order_back)
                        if "pred" not in locals():
                            pred = np.zeros((self._X.shape[0],) + p.shape[1:], dtype=self.dtype)
                        pred[k] = p
                else:
                    l = int(math.ceil(self._X.shape[0] / self.cfg.TRAIN.BATCH_SIZE))
                    for k in tqdm(range(l), leave=False):
                        top = (
                            (k + 1) * self.cfg.TRAIN.BATCH_SIZE
                            if (k + 1) * self.cfg.TRAIN.BATCH_SIZE < self._X.shape[0]
                            else self._X.shape[0]
                        )
                        with torch.cuda.amp.autocast():
                            p = self.apply_model_activations(
                                self.model_call_func(self._X[k * self.cfg.TRAIN.BATCH_SIZE : top])
                            )
                            # Multi-head concatenation
                            if isinstance(p, list):
                                p = torch.cat(
                                    (p[0], torch.argmax(p[1], axis=1).unsqueeze(1)),
                                    dim=1,
                                )

                        # Calculate the metrics
                        if self._Y is not None:
                            metric_values = self.metric_calculation(
                                p,
                                to_pytorch_format(
                                    self._Y[k * self.cfg.TRAIN.BATCH_SIZE : top],
                                    self.axis_order,
                                    self.device,
                                    dtype=self.loss_dtype,
                                ),
                                train=False,
                            )
                            for metric in metric_values:
                                if str(metric).lower() not in self.stats["per_crop"]:
                                    self.stats["per_crop"][str(metric).lower()] = 0
                                self.stats["per_crop"][str(metric).lower()] += metric_values[metric]
                        self.stats["patch_by_batch_counter"] += 1

                        p = to_numpy_format(p, self.axis_order_back)
                        if "pred" not in locals():
                            pred = np.zeros((self._X.shape[0],) + p.shape[1:], dtype=self.dtype)
                        pred[k * self.cfg.TRAIN.BATCH_SIZE : top] = p

                # Delete self._X as in 3D there is no full image
                if self.cfg.PROBLEM.NDIM == "3D":
                    del self._X, p

                # Reconstruct the predictions
                if original_data_shape[1:-1] != self.cfg.DATA.PATCH_SIZE[:-1]:
                    if self.cfg.PROBLEM.NDIM == "3D":
                        original_data_shape = original_data_shape[1:]
                    f_name = merge_data_with_overlap if self.cfg.PROBLEM.NDIM == "2D" else merge_3D_data_with_overlap

                    if self.cfg.TEST.REDUCE_MEMORY:
                        pred = f_name(
                            pred,
                            original_data_shape[:-1] + (pred.shape[-1],),
                            padding=self.cfg.DATA.TEST.PADDING,
                            overlap=self.cfg.DATA.TEST.OVERLAP,
                            verbose=self.cfg.TEST.VERBOSE,
                        )
                        if self._Y is not None:
                            self._Y = f_name(
                                self._Y,
                                original_data_shape[:-1] + (self._Y.shape[-1],),
                                padding=self.cfg.DATA.TEST.PADDING,
                                overlap=self.cfg.DATA.TEST.OVERLAP,
                                verbose=self.cfg.TEST.VERBOSE,
                            )
                    else:
                        obj = f_name(
                            pred,
                            original_data_shape[:-1] + (pred.shape[-1],),
                            data_mask=self._Y,
                            padding=self.cfg.DATA.TEST.PADDING,
                            overlap=self.cfg.DATA.TEST.OVERLAP,
                            verbose=self.cfg.TEST.VERBOSE,
                        )
                        if self._Y is not None:
                            pred, self._Y = obj
                        else:
                            pred = obj
                        del obj
                    if self.cfg.PROBLEM.NDIM != "3D":
                        self._X = X_original.copy()
                        del X_original
                    else:
                        pred = np.expand_dims(pred, 0)
                        if self._Y is not None:
                            self._Y = np.expand_dims(self._Y, 0)

                if self.cfg.DATA.REFLECT_TO_COMPLETE_SHAPE:
                    if self.cfg.PROBLEM.NDIM == "2D":
                        pred = pred[:, -reflected_orig_shape[1] :, -reflected_orig_shape[2] :]
                        if self._Y is not None:
                            self._Y = self._Y[
                                :,
                                -reflected_orig_shape[1] :,
                                -reflected_orig_shape[2] :,
                            ]
                    else:
                        pred = pred[
                            :,
                            -reflected_orig_shape[1] :,
                            -reflected_orig_shape[2] :,
                            -reflected_orig_shape[3] :,
                        ]
                        if self._Y is not None:
                            self._Y = self._Y[
                                :,
                                -reflected_orig_shape[1] :,
                                -reflected_orig_shape[2] :,
                                -reflected_orig_shape[3] :,
                            ]

                # Apply mask
                if self.cfg.TEST.POST_PROCESSING.APPLY_MASK:
                    pred = np.expand_dims(apply_binary_mask(pred[0], self.cfg.DATA.TEST.BINARY_MASKS), 0)

                # Save image
                if self.cfg.PATHS.RESULT_DIR.PER_IMAGE != "":
                    save_tif(
                        pred,
                        self.cfg.PATHS.RESULT_DIR.PER_IMAGE,
                        self.processing_filenames,
                        verbose=self.cfg.TEST.VERBOSE,
                    )

                # Argmax if needed
                if self.cfg.MODEL.N_CLASSES > 2 and self.cfg.DATA.TEST.ARGMAX_TO_OUTPUT:
                    _type = np.uint8 if self.cfg.MODEL.N_CLASSES < 255 else np.uint16
                    pred = np.expand_dims(np.argmax(pred, -1), -1).astype(_type)
                    if self._Y is not None:
                        self._Y = np.expand_dims(np.argmax(self._Y, -1), -1).astype(_type)

                # Calculate the metrics
                if self._Y is not None:
                    metric_values = self.metric_calculation(
                        to_pytorch_format(pred, self.axis_order, self.device),
                        to_pytorch_format(
                            self._Y,
                            self.axis_order,
                            self.device,
                            dtype=self.loss_dtype,
                        ),
                        train=False,
                    )
                    for metric in metric_values:
                        if str(metric).lower() not in self.stats["merge_patches"]:
                            self.stats["merge_patches"][str(metric).lower()] = 0
                        self.stats["merge_patches"][str(metric).lower()] += metric_values[metric]

                ############################
                ### POST-PROCESSING (3D) ###
                ############################
                if self.post_processing["per_image"]:
                    pred = apply_post_processing(self.cfg, pred)

                    # Calculate the metrics
                    if self._Y is not None:
                        metric_values = self.metric_calculation(
                            to_pytorch_format(pred, self.axis_order, self.device),
                            to_pytorch_format(
                                self._Y,
                                self.axis_order,
                                self.device,
                                dtype=self.loss_dtype,
                            ),
                            train=False,
                        )
                        for metric in metric_values:
                            if str(metric).lower() not in self.stats["merge_patches_post"]:
                                self.stats["merge_patches_post"][str(metric).lower()] = 0
                            self.stats["merge_patches_post"][str(metric).lower()] += metric_values[metric]

                    save_tif(
                        pred,
                        self.cfg.PATHS.RESULT_DIR.PER_IMAGE_POST_PROCESSING,
                        self.processing_filenames,
                        verbose=self.cfg.TEST.VERBOSE,
                    )
            else:
                # Load prediction from file
                folder = (
                    self.cfg.PATHS.RESULT_DIR.PER_IMAGE_POST_PROCESSING
                    if self.post_processing["per_image"]
                    else self.cfg.PATHS.RESULT_DIR.PER_IMAGE
                )
                test_file = os.path.join(folder, self.test_filenames[self.f_numbers[0]])
                pred = read_img(test_file, is_3d=self.cfg.PROBLEM.NDIM == "3D")
                pred = np.expand_dims(pred, 0)  # expand dimensions to include "batch"

            self.after_merge_patches(pred)

            if self.cfg.TEST.ANALIZE_2D_IMGS_AS_3D_STACK:
                self.all_pred.append(pred)
                if self._Y is not None:
                    self.all_gt.append(self._Y)

        ##################
        ### FULL IMAGE ###
        ##################
        if self.cfg.TEST.FULL_IMG and self.cfg.PROBLEM.NDIM == "2D":
            self._X, o_test_shape = check_downsample_division(self._X, len(self.cfg.MODEL.FEATURE_MAPS) - 1)
            if not self.cfg.TEST.REUSE_PREDICTIONS:
                if self._Y is not None:
                    self._Y, _ = check_downsample_division(self._Y, len(self.cfg.MODEL.FEATURE_MAPS) - 1)

                # Make the prediction
                if self.cfg.TEST.AUGMENTATION:
                    pred = ensemble8_2d_predictions(
                        self._X[0],
                        axis_order_back=self.axis_order_back,
                        pred_func=self.model_call_func,
                        axis_order=self.axis_order,
                        device=self.device,
                        mode=self.cfg.TEST.AUGMENTATION_MODE,
                    )
                else:
                    with torch.cuda.amp.autocast():
                        pred = self.model_call_func(self._X)
                pred = self.apply_model_activations(pred)
                # Multi-head concatenation
                if isinstance(pred, list):
                    pred = torch.cat((pred[0], torch.argmax(pred[1], axis=1).unsqueeze(1)), dim=1)
                pred = to_numpy_format(pred, self.axis_order_back)
                del self._X

                # Recover original shape if padded with check_downsample_division
                pred = pred[:, : o_test_shape[1], : o_test_shape[2]]
                if self._Y is not None:
                    self._Y = self._Y[:, : o_test_shape[1], : o_test_shape[2]]

                # Save image
                save_tif(
                    pred,
                    self.cfg.PATHS.RESULT_DIR.FULL_IMAGE,
                    self.processing_filenames,
                    verbose=self.cfg.TEST.VERBOSE,
                )

                # Argmax if needed
                if self.cfg.MODEL.N_CLASSES > 2 and self.cfg.DATA.TEST.ARGMAX_TO_OUTPUT:
                    _type = np.uint8 if self.cfg.MODEL.N_CLASSES < 255 else np.uint16
                    pred = np.expand_dims(np.argmax(pred, -1), -1).astype(_type)
                    if self._Y is not None:
                        self._Y = np.expand_dims(np.argmax(self._Y, -1), -1).astype(_type)

                if self.cfg.TEST.POST_PROCESSING.APPLY_MASK:
                    pred = apply_binary_mask(pred, self.cfg.DATA.TEST.BINARY_MASKS)

                # Calculate the metrics
                if self._Y is not None:
                    metric_values = self.metric_calculation(
                        to_pytorch_format(pred, self.axis_order, self.device),
                        to_pytorch_format(
                            self._Y,
                            self.axis_order,
                            self.device,
                            dtype=self.loss_dtype,
                        ),
                        train=False,
                    )
                    for metric in metric_values:
                        if str(metric).lower() not in self.stats["full_image"]:
                            self.stats["full_image"][str(metric).lower()] = 0
                        self.stats["full_image"][str(metric).lower()] += metric_values[metric]
            else:
                # load prediction from file
                test_file = os.path.join(
                    self.cfg.PATHS.RESULT_DIR.FULL_IMAGE,
                    self.test_filenames[self.f_numbers[0]],
                )
                pred = read_img(test_file, is_3d=self.cfg.PROBLEM.NDIM == "3D")
                pred = np.expand_dims(pred, 0)  # expand dimensions to include "batch"

            if self.cfg.TEST.ANALIZE_2D_IMGS_AS_3D_STACK:
                self.all_pred.append(pred)
                if self._Y is not None:
                    self.all_gt.append(self._Y)

            self.after_full_image(pred)

        # Save test_output if the user wants to export the model to BMZ later
        if "test_output" not in self.bmz_config:
            if self.cfg.PROBLEM.NDIM == "2D":
                self.bmz_config["test_output"] = pred[0][
                    : self.cfg.DATA.PATCH_SIZE[0], : self.cfg.DATA.PATCH_SIZE[1]
                ].copy()
            else:
                self.bmz_config["test_output"] = pred[0][
                    : self.cfg.DATA.PATCH_SIZE[0], : self.cfg.DATA.PATCH_SIZE[1], : self.cfg.DATA.PATCH_SIZE[2]
                ].copy()

    def normalize_stats(self, image_counter):
        """
        Normalize statistics.

        Parameters
        ----------
        image_counter : int
            Number of images to average the metrics.
        """
        # Per crop
        for metric in self.stats["per_crop"]:
            self.stats["per_crop"][metric] = (
                self.stats["per_crop"][metric] / self.stats["patch_by_batch_counter"]
                if self.stats["patch_by_batch_counter"] != 0
                else 0
            )

        # Merge patches
        for metric in self.stats["merge_patches"]:
            self.stats["merge_patches"][metric] = (
                self.stats["merge_patches"][metric] / image_counter if image_counter != 0 else 0
            )

        # Full image
        for metric in self.stats["full_image"]:
            self.stats["full_image"][metric] = (
                self.stats["full_image"][metric] / image_counter if image_counter != 0 else 0
            )

        # By chunks
        for metric in self.stats["by_chunks"]:
            self.stats["by_chunks"][metric] = (
                self.stats["by_chunks"][metric] / image_counter if image_counter != 0 else 0
            )

        if self.post_processing["per_image"]:
            for metric in self.stats["merge_patches_post"]:
                self.stats["merge_patches_post"][metric] = (
                    self.stats["merge_patches_post"][metric] / image_counter if image_counter != 0 else 0
                )

    def print_stats(self, image_counter):
        """
        Print statistics.

        Parameters
        ----------
        image_counter : int
            Number of images to call ``normalize_stats``.
        """
        self.normalize_stats(image_counter)
        if self.cfg.DATA.TEST.LOAD_GT and not self.cfg.TEST.REUSE_PREDICTIONS:
            if self.by_chunks:
                if len(self.stats["by_chunks"]) > 0:
                    for metric in self.test_metric_names:
                        if metric.lower() in self.stats["by_chunks"]:  # IoU is not calculated
                            print(
                                "Test {} (per image): {}".format(
                                    str(metric),
                                    self.stats["by_chunks"][metric.lower()],
                                )
                            )
            else:
                if not self.cfg.TEST.FULL_IMG or (
                    len(self.stats["per_crop"]) > 0 or len(self.stats["merge_patches"]) > 0
                ):
                    if len(self.stats["per_crop"]) > 0:
                        for metric in self.test_metric_names:
                            if metric.lower() in self.stats["per_crop"]:
                                metric_name = "Foreground IoU" if metric == "IoU" else metric
                                print(
                                    "Test {} (per patch): {}".format(
                                        metric_name,
                                        self.stats["per_crop"][metric.lower()],
                                    )
                                )

                    if len(self.stats["merge_patches"]) > 0:
                        for metric in self.test_metric_names:
                            if metric.lower() in self.stats["merge_patches"]:
                                metric_name = "Foreground IoU" if metric == "IoU" else metric
                                print(
                                    "Test {} (merge patches): {}".format(
                                        metric_name,
                                        self.stats["merge_patches"][metric.lower()],
                                    )
                                )
                else:
                    if len(self.stats["full_image"]) > 0:
                        for metric in self.test_metric_names:
                            if metric.lower() in self.stats["full_image"]:
                                metric_name = "Foreground IoU" if metric == "IoU" else metric
                                print(
                                    "Test {} (per image): {}".format(
                                        metric_name,
                                        self.stats["full_image"][metric.lower()],
                                    )
                                )

            print(" ")

            if self.post_processing["per_image"] and len(self.stats["merge_patches_post"]) > 0:
                for metric in self.test_metric_names:
                    if metric.lower() in self.stats["merge_patches_post"]:
                        metric_name = "Foreground IoU" if metric == "IoU" else metric
                        print(
                            "Test {} (merge patches - post-processing): {}".format(
                                metric_name,
                                self.stats["merge_patches_post"][metric.lower()],
                            )
                        )
                print(" ")

            if self.post_processing["as_3D_stack"] and len(self.stats["as_3D_stack_post"]) > 0:
                for metric in self.test_metric_names:
                    if metric.lower() in self.stats["as_3D_stack_post"]:
                        metric_name = "Foreground IoU" if metric == "IoU" else metric
                        print(
                            "Test {} (as 3D stack - post-processing): {}".format(
                                metric_name,
                                self.stats["as_3D_stack_post"][metric.lower()],
                            )
                        )
                print(" ")

    @abstractmethod
    def after_merge_patches(self, pred):
        """
        Place any code that needs to be done after merging all predicted patches into the original image.

        Parameters
        ----------
        pred : Torch Tensor
            Model prediction.
        """
        raise NotImplementedError

    def after_merge_patches_by_chunks_proccess_entire_pred(self, filename):
        """
        Place any code that needs to be done after merging all predicted patches into the original image
        but in the process made chunk by chunk. This function will operate over the entire predicted
        image.

        Parameters
        ----------
        filename : List of str
            Filename of the predicted image H5/Zarr.
        """
        # Load H5/Zarr and convert it into numpy array
        pred_file, pred = read_chunked_data(filename)
        pred = np.squeeze(np.array(pred, dtype=self.dtype))
        if self.cfg.TEST.BY_CHUNKS.FORMAT == "h5":
            pred_file.close()

        # Adjust shape
        if pred.ndim < 3:
            raise ValueError("Read image seems to be 2D: {}. Path: {}".format(pred.shape, filename))
        if pred.ndim == 3:
            pred = np.expand_dims(pred, -1)
        else:
            min_val = min(pred.shape)
            channel_pos = pred.shape.index(min_val)
            if channel_pos != 3 and pred.shape[channel_pos] <= 4:
                new_pos = [x for x in range(4) if x != channel_pos] + [
                    channel_pos,
                ]
                pred = pred.transpose(new_pos)

        if pred.ndim == 4:
            pred = np.expand_dims(pred, 0)

        fname, file_extension = os.path.splitext(os.path.basename(filename))
        self.processing_filenames = [fname + ".tif"]
        self.after_merge_patches(pred)

    @abstractmethod
    def after_merge_patches_by_chunks_proccess_patch(self, filename):
        """
        Place any code that needs to be done after merging all predicted patches into the original image
        but in the process made chunk by chunk. This function will operate patch by patch defined by
        ``DATA.PATCH_SIZE``.

        Parameters
        ----------
        filename : List of str
            Filename of the predicted image H5/Zarr.
        """
        raise NotImplementedError

    @abstractmethod
    def after_full_image(self, pred):
        """
        Place here any code that must be executed after generating the prediction by supplying the entire image to the model.
        To enable this, the model should be convolutional, and the image(s) should be in a 2D format. Using 3D images as
        direct inputs to the model is not feasible due to their large size.

        Parameters
        ----------
        pred : Torch Tensor
            Model prediction.
        """
        raise NotImplementedError

    def after_all_images(self):
        """
        Place here any code that must be done after predicting all images.
        """
        ############################
        ### POST-PROCESSING (2D) ###
        ############################
        if self.post_processing["as_3D_stack"]:
            self.all_pred = np.expand_dims(np.concatenate(self.all_pred), 0)
            self.all_gt = np.expand_dims(np.concatenate(self.all_gt), 0) if self.cfg.DATA.TEST.LOAD_GT else None
            save_tif(
                self.all_pred,
                self.cfg.PATHS.RESULT_DIR.AS_3D_STACK,
                verbose=self.cfg.TEST.VERBOSE,
            )
            save_tif(
                (self.all_pred > 0.5).astype(np.uint8),
                self.cfg.PATHS.RESULT_DIR.AS_3D_STACK_BIN,
                verbose=self.cfg.TEST.VERBOSE,
            )

            self.all_pred = apply_post_processing(self.cfg, self.all_pred)

            # Calculate the metrics
            if self.cfg.DATA.TEST.LOAD_GT:
                metric_values = self.metric_calculation(
                    to_pytorch_format(self.all_pred[0], self.axis_order, self.device),
                    to_pytorch_format(
                        self.all_gt[0],
                        self.axis_order,
                        self.device,
                        dtype=self.loss_dtype,
                    ),
                    train=False,
                )
                for metric in metric_values:
                    self.stats["as_3D_stack_post"][str(metric).lower()] = metric_values[metric]

            save_tif(
                self.all_pred,
                self.cfg.PATHS.RESULT_DIR.AS_3D_STACK_POST_PROCESSING,
                verbose=self.cfg.TEST.VERBOSE,
            )


def extract_patch_from_dataset(data, cfg, input_queue, extract_info_queue, verbose=False):
    """
    Extract patches from data and put them into a queue read by each GPU inference process.
    This function will be run by a child process created for every test sample.

    Parameters
    ----------
    data : Str or Numpy array
        If str it will be consider a path to load a H5/Zarr file. If not, it will be considered as the
        data to extract patches from.

    cfg : YACS configuration
        Running configuration.

    input_queue : Multiprocessing queue
        Queue to put each extracted patch into.

    extract_info_queue : Multiprocessing queue
        Auxiliary queue to pass information between processes.

    verbose : bool, optional
        To print useful information for debugging.
    """
    if verbose and cfg.SYSTEM.NUM_GPUS > 1:
        if isinstance(data, str):
            print(f"[Rank {get_rank()} ({os.getpid()})] In charge of extracting patch from data from {data}")
        else:
            print(
                f"[Rank {get_rank()} ({os.getpid()})] In charge of extracting patch from data from Numpy array {data.shape}"
            )

    # Load H5/Zarr in case we need it
    if isinstance(data, str):
        data_file, data = read_chunked_data(data)
    # Process of extracting each patch
    patch_counter = 0
    for obj in extract_3D_patch_with_overlap_yield(
        data,
        cfg.DATA.PATCH_SIZE,
        cfg.TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER,
        overlap=cfg.DATA.TEST.OVERLAP,
        padding=cfg.DATA.TEST.PADDING,
        total_ranks=max(1, cfg.SYSTEM.NUM_GPUS),
        rank=get_rank(),
        verbose=verbose,
    ):

        if is_main_process():
            img, patch_coords, total_vol, z_vol_info, list_of_vols_in_z = obj
        else:
            img, patch_coords, total_vol = obj

        img = np.expand_dims(img, 0)

        t_dim, z_dim, y_dim, x_dim, c_dim = order_dimensions(
            cfg.DATA.PREPROCESS.ZOOM.ZOOM_FACTOR,
            input_order=cfg.TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER,
            output_order="TZYXC",
            default_value=1,
        )
        patch_coords = (np.array([z_dim, y_dim, x_dim]) * np.array(patch_coords).T).T
        img = zoom(img, (t_dim, z_dim, y_dim, x_dim, c_dim), order=0, mode="nearest")

        input_queue.put([img, patch_coords])

        if patch_counter == 0:
            # This goes for the child process in charge of inserting data patches (insert_patch_into_dataset function)
            extract_info_queue.put(total_vol)
        patch_counter += 1

    # Send a sentinel so the main thread knows that there is no more data
    input_queue.put(None)

    # Send to the main thread patch_counter
    extract_info_queue.put(patch_counter)
    if is_main_process():
        extract_info_queue.put(z_vol_info)
        extract_info_queue.put(list_of_vols_in_z)

    if verbose and cfg.SYSTEM.NUM_GPUS > 1:
        if isinstance(data, str):
            print(f"[Rank {get_rank()} ({os.getpid()})] Finish extracting patches from data {data}")
        else:
            print(f"[Rank {get_rank()} ({os.getpid()})] Finish extracting patches from data {data.shape}")

    if "data_file" in locals() and cfg.TEST.BY_CHUNKS.FORMAT == "h5":
        data_file.close()


def insert_patch_into_dataset(
    data_filename,
    data_filename_mask,
    data_shape,
    output_queue,
    extract_info_queue,
    cfg,
    dtype_str,
    dtype,
    file_type,
    verbose=False,
):
    """
    Insert predicted patches (in ``output_queue``) in its original position in a H5/Zarr file. Each GPU will create
    a file containing the part it has processed (as we can not write the same H5/Zarr file ar the same time). Then,
    the main rank will create the final image. This function will be run by a child process created for every
    test sample.

    Parameters
    ----------
    data_filename : Str or Numpy array
        If str it will be consider a path to load a H5/Zarr file. If not, it will be considered as the
        data to extract patches from.

    data_shape : YACS configuration
        Shape of the H5/Zarr file dataset to create.

    output_queue : Multiprocessing queue
        Queue to get each prediction from.

    extract_info_queue : Multiprocessing queue
        Auxiliary queue to pass information between processes.

    cfg : YACS configuration
        Running configuration.

    dtype_str : str
        Type of the H5/Zarr dataset to create.

    dtype : Numpy dtype
        Type of the H5/Zarr dataset to create. Only used if a TIF file is created by selected to do so
        with ``TEST.BY_CHUNKS.SAVE_OUT_TIF`` variable.

    verbose : bool, optional
        To print useful information for debugging.
    """
    if verbose and cfg.SYSTEM.NUM_GPUS > 1:
        print(f"[Rank {get_rank()} ({os.getpid()})] In charge of inserting patches into data . . .")

    if file_type == "h5":
        fid = h5py.File(data_filename, "w")
        fid_mask = h5py.File(data_filename_mask, "w")
    else:
        fid = zarr.open_group(data_filename, mode="w")
        fid_mask = zarr.open_group(data_filename_mask, mode="w")

    filename, file_extension = os.path.splitext(os.path.basename(data_filename))

    # Obtain the total patches so we can display it for the user
    total_patches = extract_info_queue.get(timeout=60)
    for i in tqdm(range(total_patches), disable=not is_main_process()):
        p, m, patch_coords = output_queue.get(timeout=60)

        if "data" not in locals():
            # Channel dimension should be equal to the number of channel of the prediction
            out_data_shape = np.array(data_shape)
            if "C" not in cfg.TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER:
                out_data_shape = tuple(out_data_shape) + (p.shape[-1],)
                out_data_order = cfg.TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER + "C"
            else:
                out_data_shape[cfg.TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER.index("C")] = p.shape[-1]
                out_data_shape = tuple(out_data_shape)
                out_data_order = cfg.TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER

            if file_type == "h5":
                data = fid.create_dataset("data", out_data_shape, dtype=dtype_str, compression="gzip")
                mask = fid_mask.create_dataset("data", out_data_shape, dtype=dtype_str, compression="gzip")
            else:
                data = fid.create_dataset("data", shape=out_data_shape, dtype=dtype_str)
                mask = fid_mask.create_dataset("data", shape=out_data_shape, dtype=dtype_str)

        # Adjust slices to calculate where to insert the predicted patch. This slice does not have into account the
        # channel so any of them can be inserted
        slices = (
            slice(patch_coords[0][0], patch_coords[0][1]),
            slice(patch_coords[1][0], patch_coords[1][1]),
            slice(patch_coords[2][0], patch_coords[2][1]),
            slice(None),
        )
        data_ordered_slices = tuple(
            order_dimensions(
                slices,
                input_order="ZYXC",
                output_order=cfg.TEST.BY_CHUNKS.INPUT_IMG_AXES_ORDER,
                default_value=0,
            )
        )

        # Adjust patch slice to transpose it before inserting intop the final data
        current_order = np.array(range(len(p.shape)))
        transpose_order = order_dimensions(
            current_order,
            input_order="ZYXC",
            output_order=out_data_order,
            default_value=np.nan,
        )
        transpose_order = [x for x in transpose_order if not np.isnan(x)]

        data[data_ordered_slices] += p.transpose(transpose_order)
        mask[data_ordered_slices] += m.transpose(transpose_order)

        # Force flush after some iterations
        if i % cfg.TEST.BY_CHUNKS.FLUSH_EACH == 0 and file_type == "h5":
            fid.flush()
            fid_mask.flush()

    # Save image
    if cfg.TEST.BY_CHUNKS.SAVE_OUT_TIF and cfg.PATHS.RESULT_DIR.PER_IMAGE != "":
        current_order = np.array(range(len(data.shape)))
        transpose_order = order_dimensions(
            current_order,
            input_order=out_data_order,
            output_order="TZYXC",
            default_value=np.nan,
        )
        transpose_order = [x for x in transpose_order if not np.isnan(x)]
        data = np.array(data, dtype=dtype).transpose(transpose_order)
        mask = np.array(mask, dtype=dtype).transpose(transpose_order)
        if "T" not in out_data_order:
            data = np.expand_dims(data, 0)
            mask = np.expand_dims(mask, 0)
        save_tif(data, cfg.PATHS.RESULT_DIR.PER_IMAGE, [filename + ".tif"], verbose=verbose)
        save_tif(
            mask,
            cfg.PATHS.RESULT_DIR.PER_IMAGE,
            [filename + "_mask.tif"],
            verbose=verbose,
        )
    if file_type == "h5":
        fid.close()
        fid_mask.close()

    if verbose and cfg.SYSTEM.NUM_GPUS > 1:
        print(f"[Rank {get_rank()} ({os.getpid()})] Finish inserting patches into data . . .")
