import os
from typing import List, Dict, Any, Optional, Tuple, Union
from torch.utils.data import (
    DistributedSampler,
    DataLoader,
    DistributedSampler,
    SequentialSampler,
)
import numpy as np
from tqdm import tqdm

from biapy.utils.util import save_tif
from biapy.data.pre_processing import (
    calculate_2D_volume_prob_map,
    calculate_3D_volume_prob_map,
    save_tif,
    percentile_clip,
)
from biapy.data.generators.pair_data_2D_generator import Pair2DImageDataGenerator
from biapy.data.generators.pair_data_3D_generator import Pair3DImageDataGenerator
from biapy.data.generators.single_data_2D_generator import Single2DImageDataGenerator
from biapy.data.generators.single_data_3D_generator import Single3DImageDataGenerator
from biapy.data.generators.test_pair_data_generators import test_pair_data_generator
from biapy.data.generators.test_single_data_generator import test_single_data_generator
from biapy.config.config import Config


def create_train_val_augmentors(
    cfg: type[Config],
    X_train: np.ndarray | None,
    Y_train: np.ndarray | None,
    X_val: Any,
    Y_val: Any,
    world_size: int,
    global_rank: int,
) -> Tuple[DataLoader, DataLoader, Dict, int]:
    """
    Create training and validation generators.

    Parameters
    ----------
    cfg : Config
        BiaPy configuration.

    X_train : 4D/5D Numpy array
        Training data. E.g. ``(num_of_images, y, x, channels)`` for ``2D`` or ``(num_of_images, z, y, x, channels)`` for ``3D``.

    Y_train : 4D/5D Numpy array
        Training data mask/class. E.g. ``(num_of_images, y, x, channels)`` for ``2D`` or ``(num_of_images, z, y, x, channels)`` for ``3D``
        in all the workflows except classification. For this last the shape is ``(num_of_images, class)`` for both ``2D`` and ``3D``.

    X_val : 4D/5D Numpy array
        Validation data mask/class. E.g. ``(num_of_images, y, x, channels)`` for ``2D`` or ``(num_of_images, z, y, x, channels)`` for ``3D``.

    Y_val : 4D/5D Numpy array
        Validation data mask/class. E.g. ``(num_of_images, y, x, channels)`` for ``2D`` or ``(num_of_images, z, y, x, channels)`` for ``3D``
        in all the workflows except classification. For this last the shape is ``(num_of_images, class)`` for both ``2D`` and ``3D``.

    world_size: int
        Number of processes participating in the training.

    global_rank: int
        Rank of the current process.

    Returns
    -------
    train_generator : DataLoader
        Training data generator.

    val_generator : DataLoader
        Validation data generator.

    data_norm: dict
        Normalization of the data.

    num_training_steps_per_epoch: int
        Number of training steps per epoch.
    """

    # Calculate the probability map per image
    prob_map = None
    if cfg.DATA.PROBABILITY_MAP and cfg.DATA.EXTRACT_RANDOM_PATCH:
        if os.path.exists(cfg.PATHS.PROB_MAP_DIR):
            print("Loading probability map")
            prob_map_file = os.path.join(cfg.PATHS.PROB_MAP_DIR, cfg.PATHS.PROB_MAP_FILENAME)
            num_files = len(next(os.walk(cfg.PATHS.PROB_MAP_DIR))[2])
            prob_map = cfg.PATHS.PROB_MAP_DIR if num_files > 1 else np.load(prob_map_file)
        else:
            f_name = calculate_2D_volume_prob_map if cfg.PROBLEM.NDIM == "2D" else calculate_3D_volume_prob_map
            prob_map = f_name(
                Y_train,
                cfg.DATA.TRAIN.GT_PATH,
                cfg.DATA.W_FOREGROUND,
                cfg.DATA.W_BACKGROUND,
                save_dir=cfg.PATHS.PROB_MAP_DIR,
            )

    # Normalization checks
    norm_dict = {}
    norm_dict["type"] = cfg.DATA.NORMALIZATION.TYPE
    norm_dict["mask_norm"] = "as_mask"
    norm_dict["application_mode"] = cfg.DATA.NORMALIZATION.APPLICATION_MODE
    norm_dict["enable"] = True

    # Percentile clipping
    if cfg.DATA.NORMALIZATION.PERC_CLIP:
        norm_dict["lower_bound"] = cfg.DATA.NORMALIZATION.PERC_LOWER
        norm_dict["upper_bound"] = cfg.DATA.NORMALIZATION.PERC_UPPER
        if cfg.DATA.NORMALIZATION.APPLICATION_MODE == "dataset":
            (
                X_train,
                norm_dict["dataset_X_lower_value"],
                norm_dict["dataset_X_upper_value"],
            ) = percentile_clip(X_train, norm_dict["lower_bound"], norm_dict["upper_bound"])
            os.makedirs(os.path.dirname(cfg.PATHS.LWR_X_FILE), exist_ok=True)
            np.save(cfg.PATHS.LWR_X_FILE, norm_dict["dataset_X_lower_value"])
            np.save(cfg.PATHS.UPR_X_FILE, norm_dict["dataset_X_upper_value"])
            print(f"X_train clipped using the following values: {norm_dict}")

    if cfg.DATA.NORMALIZATION.TYPE == "custom":
        if cfg.DATA.NORMALIZATION.APPLICATION_MODE == "dataset":
            if cfg.DATA.NORMALIZATION.CUSTOM_MEAN == -1 and cfg.DATA.NORMALIZATION.CUSTOM_STD == -1:
                print("Train/Val normalization: trying to load mean from {}".format(cfg.PATHS.MEAN_INFO_FILE))
                print("Train/Val normalization: trying to load std from {}".format(cfg.PATHS.STD_INFO_FILE))
                if not os.path.exists(cfg.PATHS.MEAN_INFO_FILE) or not os.path.exists(cfg.PATHS.STD_INFO_FILE):
                    print("Train/Val normalization: mean and/or std files not found. Calculating it for the first time")
                    if isinstance(X_train, np.ndarray):
                        norm_dict["mean"] = np.mean(X_train)
                        norm_dict["std"] = np.std(X_train)
                    os.makedirs(os.path.dirname(cfg.PATHS.MEAN_INFO_FILE), exist_ok=True)
                    np.save(cfg.PATHS.MEAN_INFO_FILE, norm_dict["mean"])
                    np.save(cfg.PATHS.STD_INFO_FILE, norm_dict["std"])
                else:
                    norm_dict["mean"] = float(np.load(cfg.PATHS.MEAN_INFO_FILE))
                    norm_dict["std"] = float(np.load(cfg.PATHS.STD_INFO_FILE))
                    print("Train/Val normalization values loaded!")
            else:
                norm_dict["mean"] = cfg.DATA.NORMALIZATION.CUSTOM_MEAN
                norm_dict["std"] = cfg.DATA.NORMALIZATION.CUSTOM_STD
        if "mean" in norm_dict:
            print("Train/Val normalization: using mean {} and std: {}".format(norm_dict["mean"], norm_dict["std"]))

    if cfg.PROBLEM.NDIM == "2D":
        if cfg.PROBLEM.TYPE == "CLASSIFICATION" or (
            cfg.PROBLEM.TYPE == "SELF_SUPERVISED" and cfg.PROBLEM.SELF_SUPERVISED.PRETEXT_TASK == "masking"
        ):
            f_name = Single2DImageDataGenerator
        else:
            f_name = Pair2DImageDataGenerator
    else:
        if cfg.PROBLEM.TYPE == "CLASSIFICATION" or (
            cfg.PROBLEM.TYPE == "SELF_SUPERVISED" and cfg.PROBLEM.SELF_SUPERVISED.PRETEXT_TASK == "masking"
        ):
            f_name = Single3DImageDataGenerator
        else:
            f_name = Pair3DImageDataGenerator

    ndim = 3 if cfg.PROBLEM.NDIM == "3D" else 2
    if cfg.PROBLEM.TYPE != "DENOISING":
        data_paths = [cfg.DATA.TRAIN.PATH, cfg.DATA.TRAIN.GT_PATH]
    else:
        data_paths = [cfg.DATA.TRAIN.PATH]

    if cfg.DATA.TRAIN.IN_MEMORY:
        data_mode = "in_memory"
    else:
        if (
            cfg.PROBLEM.NDIM == "3D"
            and X_train is not None
            and (isinstance(X_train, list) or isinstance(X_train, dict))
            and isinstance(X_train[0], dict)
            and "filepath" in X_train[0]
            and (".zarr" in X_train[0]["filepath"] or ".h5" in X_train[0]["filepath"])
        ):
            data_mode = "chunked_data"
        else:
            data_mode = "not_in_memory"

    if cfg.PROBLEM.TYPE == "CLASSIFICATION" or (
        cfg.PROBLEM.TYPE == "SELF_SUPERVISED" and cfg.PROBLEM.SELF_SUPERVISED.PRETEXT_TASK == "masking"
    ):
        r_shape = cfg.DATA.PATCH_SIZE
        if cfg.MODEL.ARCHITECTURE == "efficientnet_b0" and cfg.DATA.PATCH_SIZE[:-1] != (
            224,
            224,
        ):
            r_shape = (224, 224) + (cfg.DATA.PATCH_SIZE[-1],)
            print("Changing patch size from {} to {} to use efficientnet_b0".format(cfg.DATA.PATCH_SIZE[:-1], r_shape))
        ptype = "classification" if cfg.PROBLEM.TYPE == "CLASSIFICATION" else "mae"
        dic = dict(
            ndim=ndim,
            X=X_train,
            Y=Y_train,
            data_path=cfg.DATA.TRAIN.PATH,
            ptype=ptype,
            n_classes=cfg.MODEL.N_CLASSES,
            seed=cfg.SYSTEM.SEED,
            da=cfg.AUGMENTOR.ENABLE,
            data_mode=data_mode,
            da_prob=cfg.AUGMENTOR.DA_PROB,
            rotation90=cfg.AUGMENTOR.ROT90,
            rand_rot=cfg.AUGMENTOR.RANDOM_ROT,
            rnd_rot_range=cfg.AUGMENTOR.RANDOM_ROT_RANGE,
            shear=cfg.AUGMENTOR.SHEAR,
            shear_range=cfg.AUGMENTOR.SHEAR_RANGE,
            zoom=cfg.AUGMENTOR.ZOOM,
            zoom_range=cfg.AUGMENTOR.ZOOM_RANGE,
            zoom_in_z=cfg.AUGMENTOR.ZOOM_IN_Z,
            shift=cfg.AUGMENTOR.SHIFT,
            shift_range=cfg.AUGMENTOR.SHIFT_RANGE,
            affine_mode=cfg.AUGMENTOR.AFFINE_MODE,
            vflip=cfg.AUGMENTOR.VFLIP,
            hflip=cfg.AUGMENTOR.HFLIP,
            elastic=cfg.AUGMENTOR.ELASTIC,
            e_alpha=cfg.AUGMENTOR.E_ALPHA,
            e_sigma=cfg.AUGMENTOR.E_SIGMA,
            e_mode=cfg.AUGMENTOR.E_MODE,
            g_blur=cfg.AUGMENTOR.G_BLUR,
            g_sigma=cfg.AUGMENTOR.G_SIGMA,
            median_blur=cfg.AUGMENTOR.MEDIAN_BLUR,
            mb_kernel=cfg.AUGMENTOR.MB_KERNEL,
            motion_blur=cfg.AUGMENTOR.MOTION_BLUR,
            motb_k_range=cfg.AUGMENTOR.MOTB_K_RANGE,
            gamma_contrast=cfg.AUGMENTOR.GAMMA_CONTRAST,
            gc_gamma=cfg.AUGMENTOR.GC_GAMMA,
            dropout=cfg.AUGMENTOR.DROPOUT,
            drop_range=cfg.AUGMENTOR.DROP_RANGE,
            resize_shape=r_shape,
            norm_dict=norm_dict,
            convert_to_rgb=cfg.DATA.FORCE_RGB,
        )
    else:
        dic = dict(
            ndim=ndim,
            X=X_train,
            Y=Y_train,
            seed=cfg.SYSTEM.SEED,
            data_mode=data_mode,
            data_paths=data_paths,
            da=cfg.AUGMENTOR.ENABLE,
            da_prob=cfg.AUGMENTOR.DA_PROB,
            rotation90=cfg.AUGMENTOR.ROT90,
            rand_rot=cfg.AUGMENTOR.RANDOM_ROT,
            rnd_rot_range=cfg.AUGMENTOR.RANDOM_ROT_RANGE,
            shear=cfg.AUGMENTOR.SHEAR,
            shear_range=cfg.AUGMENTOR.SHEAR_RANGE,
            zoom=cfg.AUGMENTOR.ZOOM,
            zoom_range=cfg.AUGMENTOR.ZOOM_RANGE,
            zoom_in_z=cfg.AUGMENTOR.ZOOM_IN_Z,
            shift=cfg.AUGMENTOR.SHIFT,
            affine_mode=cfg.AUGMENTOR.AFFINE_MODE,
            shift_range=cfg.AUGMENTOR.SHIFT_RANGE,
            vflip=cfg.AUGMENTOR.VFLIP,
            hflip=cfg.AUGMENTOR.HFLIP,
            elastic=cfg.AUGMENTOR.ELASTIC,
            e_alpha=cfg.AUGMENTOR.E_ALPHA,
            e_sigma=cfg.AUGMENTOR.E_SIGMA,
            e_mode=cfg.AUGMENTOR.E_MODE,
            g_blur=cfg.AUGMENTOR.G_BLUR,
            g_sigma=cfg.AUGMENTOR.G_SIGMA,
            median_blur=cfg.AUGMENTOR.MEDIAN_BLUR,
            mb_kernel=cfg.AUGMENTOR.MB_KERNEL,
            motion_blur=cfg.AUGMENTOR.MOTION_BLUR,
            motb_k_range=cfg.AUGMENTOR.MOTB_K_RANGE,
            gamma_contrast=cfg.AUGMENTOR.GAMMA_CONTRAST,
            gc_gamma=cfg.AUGMENTOR.GC_GAMMA,
            brightness=cfg.AUGMENTOR.BRIGHTNESS,
            brightness_factor=cfg.AUGMENTOR.BRIGHTNESS_FACTOR,
            brightness_mode=cfg.AUGMENTOR.BRIGHTNESS_MODE,
            contrast=cfg.AUGMENTOR.CONTRAST,
            contrast_factor=cfg.AUGMENTOR.CONTRAST_FACTOR,
            contrast_mode=cfg.AUGMENTOR.CONTRAST_MODE,
            dropout=cfg.AUGMENTOR.DROPOUT,
            drop_range=cfg.AUGMENTOR.DROP_RANGE,
            cutout=cfg.AUGMENTOR.CUTOUT,
            cout_nb_iterations=cfg.AUGMENTOR.COUT_NB_ITERATIONS,
            cout_size=cfg.AUGMENTOR.COUT_SIZE,
            cout_cval=cfg.AUGMENTOR.COUT_CVAL,
            cout_apply_to_mask=cfg.AUGMENTOR.COUT_APPLY_TO_MASK,
            cutblur=cfg.AUGMENTOR.CUTBLUR,
            cblur_size=cfg.AUGMENTOR.CBLUR_SIZE,
            cblur_down_range=cfg.AUGMENTOR.CBLUR_DOWN_RANGE,
            cblur_inside=cfg.AUGMENTOR.CBLUR_INSIDE,
            cutmix=cfg.AUGMENTOR.CUTMIX,
            cmix_size=cfg.AUGMENTOR.CMIX_SIZE,
            cutnoise=cfg.AUGMENTOR.CUTNOISE,
            cnoise_size=cfg.AUGMENTOR.CNOISE_SIZE,
            cnoise_nb_iterations=cfg.AUGMENTOR.CNOISE_NB_ITERATIONS,
            cnoise_scale=cfg.AUGMENTOR.CNOISE_SCALE,
            misalignment=cfg.AUGMENTOR.MISALIGNMENT,
            ms_displacement=cfg.AUGMENTOR.MS_DISPLACEMENT,
            ms_rotate_ratio=cfg.AUGMENTOR.MS_ROTATE_RATIO,
            missing_sections=cfg.AUGMENTOR.MISSING_SECTIONS,
            missp_iterations=cfg.AUGMENTOR.MISSP_ITERATIONS,
            grayscale=cfg.AUGMENTOR.GRAYSCALE,
            channel_shuffle=cfg.AUGMENTOR.CHANNEL_SHUFFLE,
            gridmask=cfg.AUGMENTOR.GRIDMASK,
            grid_ratio=cfg.AUGMENTOR.GRID_RATIO,
            grid_d_range=cfg.AUGMENTOR.GRID_D_RANGE,
            grid_rotate=cfg.AUGMENTOR.GRID_ROTATE,
            grid_invert=cfg.AUGMENTOR.GRID_INVERT,
            gaussian_noise=cfg.AUGMENTOR.GAUSSIAN_NOISE,
            gaussian_noise_mean=cfg.AUGMENTOR.GAUSSIAN_NOISE_MEAN,
            gaussian_noise_var=cfg.AUGMENTOR.GAUSSIAN_NOISE_VAR,
            gaussian_noise_use_input_img_mean_and_var=cfg.AUGMENTOR.GAUSSIAN_NOISE_USE_INPUT_IMG_MEAN_AND_VAR,
            poisson_noise=cfg.AUGMENTOR.POISSON_NOISE,
            salt=cfg.AUGMENTOR.SALT,
            salt_amount=cfg.AUGMENTOR.SALT_AMOUNT,
            pepper=cfg.AUGMENTOR.PEPPER,
            pepper_amount=cfg.AUGMENTOR.PEPPER_AMOUNT,
            salt_and_pepper=cfg.AUGMENTOR.SALT_AND_PEPPER,
            salt_pep_amount=cfg.AUGMENTOR.SALT_AND_PEPPER_AMOUNT,
            salt_pep_proportion=cfg.AUGMENTOR.SALT_AND_PEPPER_PROP,
            shape=cfg.DATA.PATCH_SIZE,
            resolution=cfg.DATA.TRAIN.RESOLUTION,
            random_crops_in_DA=cfg.DATA.EXTRACT_RANDOM_PATCH,
            prob_map=prob_map,
            n_classes=cfg.MODEL.N_CLASSES,
            extra_data_factor=cfg.DATA.TRAIN.REPLICATE,
            norm_dict=norm_dict,
            random_crop_scale=cfg.PROBLEM.SUPER_RESOLUTION.UPSCALING,
            convert_to_rgb=cfg.DATA.FORCE_RGB,
        )

        if cfg.PROBLEM.NDIM == "3D":
            dic["zflip"] = cfg.AUGMENTOR.ZFLIP
        if cfg.PROBLEM.TYPE == "INSTANCE_SEG":
            dic["instance_problem"] = True
        elif cfg.PROBLEM.TYPE in ["SELF_SUPERVISED", "SUPER_RESOLUTION"]:
            norm_dict["mask_norm"] = "as_image"
        elif cfg.PROBLEM.TYPE == "IMAGE_TO_IMAGE":
            norm_dict["mask_norm"] = "as_image"
            if cfg.PROBLEM.IMAGE_TO_IMAGE.MULTIPLE_RAW_ONE_TARGET_LOADER:
                dic["multiple_raw_images"] = True
        elif cfg.PROBLEM.TYPE == "DENOISING":
            dic["n2v"] = True
            dic["n2v_perc_pix"] = cfg.PROBLEM.DENOISING.N2V_PERC_PIX
            dic["n2v_manipulator"] = cfg.PROBLEM.DENOISING.N2V_MANIPULATOR
            dic["n2v_neighborhood_radius"] = cfg.PROBLEM.DENOISING.N2V_NEIGHBORHOOD_RADIUS
            dic["n2v_structMask"] = (
                np.array([[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]]) if cfg.PROBLEM.DENOISING.N2V_STRUCTMASK else None
            )

    if (
        norm_dict["mask_norm"] == "as_image"
        and cfg.DATA.NORMALIZATION.PERC_CLIP
        and cfg.DATA.NORMALIZATION.APPLICATION_MODE == "dataset"
    ):
        (
            Y_train,
            norm_dict["dataset_Y_lower_value"],
            norm_dict["dataset_Y_upper_value"],
        ) = percentile_clip(Y_train, norm_dict["lower_bound"], norm_dict["upper_bound"])
        np.save(cfg.PATHS.LWR_Y_FILE, norm_dict["dataset_Y_lower_value"])
        np.save(cfg.PATHS.UPR_Y_FILE, norm_dict["dataset_Y_upper_value"])
        print(f"Y_train clipped using the following values: {norm_dict}")

    print("Initializing train data generator . . .")
    train_generator = f_name(**dic)  # type: ignore
    data_norm = train_generator.get_data_normalization()

    print("Initializing val data generator . . .")
    if cfg.DATA.VAL.FROM_TRAIN:
        if data_mode == "chunked_data":
            val_data_mode = "chunked_data"
        else:
            val_data_mode = "in_memory"
    else:
        if cfg.DATA.VAL.IN_MEMORY:
            val_data_mode = "in_memory"
        else:
            if (
                cfg.PROBLEM.NDIM == "3D"
                and X_val is not None
                and (isinstance(X_val, list) or isinstance(X_val, dict))
                and isinstance(X_val[0], dict)
                and "filepath" in X_val[0]
                and (".zarr" in X_val[0]["filepath"] or ".h5" in X_val[0]["filepath"])
            ):
                val_data_mode = "chunked_data"
            else:
                val_data_mode = "not_in_memory"

    if (
        norm_dict["mask_norm"] == "as_image"
        and cfg.DATA.NORMALIZATION.PERC_CLIP
        and cfg.DATA.NORMALIZATION.APPLICATION_MODE == "dataset"
    ):
        X_val, _, _ = percentile_clip(
            X_val,
            lwr_perc_val=norm_dict["dataset_X_lower_value"],
            uppr_perc_val=norm_dict["dataset_X_upper_value"],
        )
        Y_val, _, _ = percentile_clip(
            Y_val,
            lwr_perc_val=norm_dict["dataset_Y_lower_value"],
            uppr_perc_val=norm_dict["dataset_Y_upper_value"],
        )
        print(f"X_val clipped using the following values: {norm_dict}")
        print(f"Y_val clipped using the following values: {norm_dict}")

    if cfg.PROBLEM.TYPE == "CLASSIFICATION" or (
        cfg.PROBLEM.TYPE == "SELF_SUPERVISED" and cfg.PROBLEM.SELF_SUPERVISED.PRETEXT_TASK == "masking"
    ):
        ptype = "classification" if cfg.PROBLEM.TYPE == "CLASSIFICATION" else "mae"
        val_generator = f_name(
            ndim=ndim,
            X=X_val,
            Y=Y_val,
            data_path=cfg.DATA.VAL.PATH,
            ptype=ptype,
            n_classes=cfg.MODEL.N_CLASSES,
            seed=cfg.SYSTEM.SEED,
            da=False,
            resize_shape=r_shape,
            norm_dict=norm_dict,
            data_mode=val_data_mode,
        )
    else:
        if cfg.PROBLEM.TYPE != "DENOISING":
            data_paths = [cfg.DATA.VAL.PATH, cfg.DATA.VAL.GT_PATH]
        else:
            data_paths = [cfg.DATA.VAL.PATH]
        dic = dict(
            ndim=ndim,
            X=X_val,
            Y=Y_val,
            data_mode=val_data_mode,
            data_paths=data_paths,
            da=False,
            shape=cfg.DATA.PATCH_SIZE,
            random_crops_in_DA=cfg.DATA.EXTRACT_RANDOM_PATCH,
            val=True,
            n_classes=cfg.MODEL.N_CLASSES,
            seed=cfg.SYSTEM.SEED,
            norm_dict=norm_dict,
            resolution=cfg.DATA.VAL.RESOLUTION,
            random_crop_scale=cfg.PROBLEM.SUPER_RESOLUTION.UPSCALING,
        )
        if cfg.PROBLEM.TYPE == "INSTANCE_SEG":
            dic["instance_problem"] = True
        elif cfg.PROBLEM.TYPE in ["SELF_SUPERVISED", "SUPER_RESOLUTION"]:
            norm_dict["mask_norm"] = "as_image"
        elif cfg.PROBLEM.TYPE == "IMAGE_TO_IMAGE":
            norm_dict["mask_norm"] = "as_image"
            if cfg.PROBLEM.IMAGE_TO_IMAGE.MULTIPLE_RAW_ONE_TARGET_LOADER:
                dic["multiple_raw_images"] = True
        elif cfg.PROBLEM.TYPE == "DENOISING":
            dic["n2v"] = True
            dic["n2v_perc_pix"] = cfg.PROBLEM.DENOISING.N2V_PERC_PIX
            dic["n2v_manipulator"] = cfg.PROBLEM.DENOISING.N2V_MANIPULATOR
            dic["n2v_neighborhood_radius"] = cfg.PROBLEM.DENOISING.N2V_NEIGHBORHOOD_RADIUS

        val_generator = f_name(**dic)  # type: ignore

    # Generate examples of data augmentation
    if cfg.AUGMENTOR.AUG_SAMPLES and cfg.AUGMENTOR.ENABLE:
        print("Creating generator samples . . .")
        train_generator.get_transformed_samples(
            cfg.AUGMENTOR.AUG_NUM_SAMPLES,
            save_to_dir=True,
            train=False,
            out_dir=cfg.PATHS.DA_SAMPLES,
            draw_grid=cfg.AUGMENTOR.DRAW_GRID,
        )

    # Training dataset
    total_batch_size = cfg.TRAIN.BATCH_SIZE * world_size * cfg.TRAIN.ACCUM_ITER
    training_samples = len(train_generator)
    # Reduce number of workers in case there is no training data
    num_workers = min(cfg.SYSTEM.NUM_WORKERS, training_samples)
    # To not create more than 8 processes per GPU
    if cfg.SYSTEM.NUM_GPUS >= 1:
        num_workers = min(num_workers, 8 * cfg.SYSTEM.NUM_GPUS)
    num_training_steps_per_epoch = training_samples // total_batch_size
    print(f"Number of workers: {num_workers}")
    print("Accumulate grad iterations: %d" % cfg.TRAIN.ACCUM_ITER)
    print("Effective batch size: %d" % total_batch_size)
    sampler_train = DistributedSampler(train_generator, num_replicas=world_size, rank=global_rank, shuffle=True)
    print("Sampler_train = %s" % str(sampler_train))
    train_dataset = DataLoader(
        train_generator,
        sampler=sampler_train,
        batch_size=cfg.TRAIN.BATCH_SIZE,
        num_workers=num_workers,
        pin_memory=cfg.SYSTEM.PIN_MEM,
        drop_last=False,
    )

    # Validation dataset
    sampler_val = None
    if cfg.DATA.VAL.DIST_EVAL:
        if len(val_generator) % world_size != 0:
            print(
                "Warning: Enabling distributed evaluation with an eval dataset not divisible by process number. "
                "This will slightly alter validation results as extra duplicate entries are added to achieve "
                "equal num of samples per-process."
            )
        sampler_val = DistributedSampler(val_generator, num_replicas=world_size, rank=global_rank, shuffle=False)
    else:
        sampler_val = SequentialSampler(val_generator)

    val_dataset = DataLoader(
        val_generator,
        sampler=sampler_val,
        batch_size=cfg.TRAIN.BATCH_SIZE,
        num_workers=num_workers,
        pin_memory=cfg.SYSTEM.PIN_MEM,
        drop_last=False,
    )

    return train_dataset, val_dataset, data_norm, num_training_steps_per_epoch


def create_test_augmentor(
    cfg: type[Config],
    X_test: Any,
    Y_test: Any,
    cross_val_samples_ids: Optional[List[int] | None] = None,
) -> Tuple[Union[test_pair_data_generator, test_single_data_generator], Dict]:
    """
    Create test data generator.

    Parameters
    ----------
    cfg : Config
        BiaPy configuration.

    X_test : 4D Numpy array
        Test data. E.g. ``(num_of_images, y, x, channels)`` for ``2D`` or ``(num_of_images, z, y, x, channels)`` for ``3D``.

    Y_test : 4D Numpy array
        Test data mask/class. E.g. ``(num_of_images, y, x, channels)`` for ``2D`` or ``(num_of_images, z, y, x, channels)`` for ``3D``
        in all the workflows except classification. For this last the shape is ``(num_of_images, class)`` for both ``2D`` and ``3D``.

    cross_val_samples_ids : List of ints, optional
        When cross validation is used training data samples' id are passed.

    Returns
    -------
    test_generator : test_pair_data_generator/test_single_data_generator
        Test data generator.

    data_norm : dict
        Normalization of the data.
    """
    norm_dict = {}
    norm_dict["type"] = cfg.DATA.NORMALIZATION.TYPE
    norm_dict["mask_norm"] = "as_mask"
    norm_dict["application_mode"] = cfg.DATA.NORMALIZATION.APPLICATION_MODE
    norm_dict["enable"] = True

    # Percentile clipping
    if cfg.DATA.NORMALIZATION.PERC_CLIP:
        norm_dict["lower_bound"] = cfg.DATA.NORMALIZATION.PERC_LOWER
        norm_dict["upper_bound"] = cfg.DATA.NORMALIZATION.PERC_UPPER
        norm_dict["clipped"] = X_test is not None
        bmz_clip = False
        if cfg.DATA.NORMALIZATION.APPLICATION_MODE == "dataset":
            if not os.path.exists(cfg.PATHS.LWR_X_FILE) or not os.path.exists(cfg.PATHS.UPR_X_FILE):
                if cfg.MODEL.SOURCE == "bmz" and X_test is not None:
                    (
                        X_test,
                        norm_dict["dataset_X_lower_value"],
                        norm_dict["dataset_X_upper_value"],
                    ) = percentile_clip(X_test, norm_dict["lower_bound"], norm_dict["upper_bound"])
                    bmz_clip = True
                else:
                    raise FileNotFoundError(
                        "Lower/uper percentile files not found in {} and {}".format(
                            cfg.PATHS.LWR_X_FILE, cfg.PATHS.UPR_X_FILE
                        )
                    )
            else:
                norm_dict["dataset_X_lower_value"] = float(np.load(cfg.PATHS.LWR_X_FILE))
                norm_dict["dataset_X_upper_value"] = float(np.load(cfg.PATHS.UPR_X_FILE))

            if X_test is not None and not bmz_clip:
                X_test, _, _ = percentile_clip(
                    X_test,
                    lwr_perc_val=norm_dict["dataset_X_lower_value"],
                    uppr_perc_val=norm_dict["dataset_X_upper_value"],
                )
                print(f"X_test clipped using the following values: {norm_dict}")

    if cfg.DATA.NORMALIZATION.TYPE == "custom":
        if cfg.DATA.NORMALIZATION.APPLICATION_MODE == "dataset":
            if cfg.DATA.NORMALIZATION.CUSTOM_MEAN == -1 and cfg.DATA.NORMALIZATION.CUSTOM_STD == -1:
                print("Test normalization: trying to load mean from {}".format(cfg.PATHS.MEAN_INFO_FILE))
                print("Test normalization: trying to load std from {}".format(cfg.PATHS.STD_INFO_FILE))
                if not os.path.exists(cfg.PATHS.MEAN_INFO_FILE) or not os.path.exists(cfg.PATHS.STD_INFO_FILE):
                    if cfg.MODEL.SOURCE == "bmz" and X_test is not None:
                        norm_dict["mean"] = np.mean(X_test)
                        norm_dict["std"] = np.std(X_test)
                    else:
                        raise FileNotFoundError(
                            "Mean/std files not found in {} and {}".format(
                                cfg.PATHS.MEAN_INFO_FILE, cfg.PATHS.STD_INFO_FILE
                            )
                        )
                else:
                    norm_dict["mean"] = float(np.load(cfg.PATHS.MEAN_INFO_FILE))
                    norm_dict["std"] = float(np.load(cfg.PATHS.STD_INFO_FILE))
            else:
                norm_dict["mean"] = cfg.DATA.NORMALIZATION.CUSTOM_MEAN
                norm_dict["std"] = cfg.DATA.NORMALIZATION.CUSTOM_STD
            print("Test normalization: using mean {} and std: {}".format(norm_dict["mean"], norm_dict["std"]))

    instance_problem = True if cfg.PROBLEM.TYPE == "INSTANCE_SEG" else False
    if cfg.PROBLEM.TYPE == "SELF_SUPERVISED" and cfg.PROBLEM.SELF_SUPERVISED.PRETEXT_TASK == "masking":
        provide_Y = False
    else:
        provide_Y = cfg.DATA.TEST.LOAD_GT or cfg.DATA.TEST.USE_VAL_AS_TEST
    if cfg.PROBLEM.TYPE in ["SUPER_RESOLUTION", "IMAGE_TO_IMAGE", "SELF_SUPERVISED"]:
        norm_dict["mask_norm"] = "none"

    ndim: int = 3 if cfg.PROBLEM.NDIM == "3D" else 2
    dic = dict(
        ndim=ndim,
        X=X_test,
        d_path=(cfg.DATA.TEST.PATH if cross_val_samples_ids is None else cfg.DATA.TRAIN.PATH),
        test_by_chunks=cfg.TEST.BY_CHUNKS.ENABLE,
        provide_Y=provide_Y,
        Y=Y_test,
        dm_path=(cfg.DATA.TEST.GT_PATH if cross_val_samples_ids is None else cfg.DATA.TRAIN.GT_PATH),
        seed=cfg.SYSTEM.SEED,
        instance_problem=instance_problem,
        norm_dict=norm_dict,
        reduce_mem=cfg.TEST.REDUCE_MEMORY,
        sample_ids=cross_val_samples_ids,
        convert_to_rgb=cfg.DATA.FORCE_RGB,
    )

    if cfg.PROBLEM.TYPE == "CLASSIFICATION" or (
        cfg.PROBLEM.TYPE == "SELF_SUPERVISED" and cfg.PROBLEM.SELF_SUPERVISED.PRETEXT_TASK == "masking"
    ):
        gen_name = test_single_data_generator
        r_shape = cfg.DATA.PATCH_SIZE
        if cfg.MODEL.ARCHITECTURE == "efficientnet_b0" and cfg.DATA.PATCH_SIZE[:-1] != (
            224,
            224,
        ):
            r_shape = (224, 224) + (cfg.DATA.PATCH_SIZE[-1],)
            print("Changing patch size from {} to {} to use efficientnet_b0".format(cfg.DATA.PATCH_SIZE[:-1], r_shape))
        if cfg.PROBLEM.TYPE == "CLASSIFICATION":
            dic["crop_center"] = True
            dic["resize_shape"] = r_shape
            dic["ptype"] = "classification"
        else:
            dic["ptype"] = "ssl"
    else:
        gen_name = test_pair_data_generator

    if cfg.PROBLEM.TYPE == "IMAGE_TO_IMAGE" and cfg.PROBLEM.IMAGE_TO_IMAGE.MULTIPLE_RAW_ONE_TARGET_LOADER:
        dic["multiple_raw_images"] = True

    test_generator = gen_name(**dic)
    data_norm = test_generator.get_data_normalization()
    return test_generator, data_norm


def check_generator_consistence(
    gen: DataLoader, data_out_dir: str, mask_out_dir: str, filenames: List[str] | None = None
):
    """
    Save all data of a generator in the given path.

    Parameters
    ----------
    gen : Pair2DImageDataGenerator/Single2DImageDataGenerator (2D) or Pair3DImageDataGenerator/Single3DImageDataGenerator (3D)
        Generator to extract the data from.

    data_out_dir : str
        Path to store the generator data samples.

    mask_out_dir : str
        Path to store the generator data mask samples.

    Filenames : List, optional
        Filenames that should be used when saving each image.
    """

    print("Check generator . . .")
    it = iter(gen)

    c = 0
    for i in tqdm(range(len(gen))):
        sample = next(it)
        X_test, Y_test = sample

        for k in range(len(X_test)):
            fil = filenames[c] if filenames is not None else ["sample_" + str(c) + ".tif"]
            save_tif(np.expand_dims(X_test[k], 0), data_out_dir, fil, verbose=False)
            save_tif(np.expand_dims(Y_test[k], 0), mask_out_dir, fil, verbose=False)
            c += 1


# To accelerate each first batch in epoch without need to.
# Sources: https://discuss.pytorch.org/t/enumerate-dataloader-slow/87778/4
#          https://github.com/huggingface/pytorch-image-models/pull/140/files
# Explanation:
# When using the data loader of pytorch, at the beginning of every epoch, we have to wait a
# lot and the training speed is very low from the first iteration. It is because the pytorch
# data loader is reinitialized from scratch. With this, we do not waste time, and just the
# first initialization of the the dataloader at the first epoch takes time, but for the next
# epochs, the first iteration of every new epoch is as fast as the iterations in the middle
# of an epoch.
class MultiEpochsDataLoader(DataLoader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._DataLoader__initialized = False
        self.batch_sampler = _RepeatSampler(self.batch_sampler)
        self._DataLoader__initialized = True
        self.iterator = super().__iter__()

    def __len__(self):
        return len(self.batch_sampler.sampler)  # type: ignore

    def __iter__(self):
        for i in range(len(self)):
            yield next(self.iterator)


class _RepeatSampler(object):
    """
    Sampler that repeats forever.

    Parameters
    ----------
    sampler (Sampler)
    """

    def __init__(self, sampler):
        self.sampler = sampler

    def __iter__(self):
        while True:
            yield from iter(self.sampler)
