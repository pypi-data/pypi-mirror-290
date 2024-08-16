from abc import ABCMeta, abstractmethod
import torch
from torch.utils.data import Dataset
import numpy as np
import random
import os
from tqdm import tqdm
import imgaug as ia
from skimage.io import imread
from imgaug import augmenters as iaa
from typing import (
    List,
    Tuple,
    Literal,
    Dict,
)

from biapy.data.pre_processing import normalize, norm_range01, percentile_clip
from biapy.data.generators.augmentors import *
from biapy.utils.misc import is_main_process


class SingleBaseDataGenerator(Dataset, metaclass=ABCMeta):
    """
    Custom BaseDataGenerator based on `imgaug <https://github.com/aleju/imgaug-doc>`_
    and our own `augmentors.py <https://github.com/BiaPyX/BiaPy/blob/master/biapy/data/generators/augmentors.py>`_
    transformations.

    Based on `microDL <https://github.com/czbiohub/microDL>`_ and
    `Shervine's blog <https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly>`_.

    Parameters
    ----------
    ndim : int
        Dimensions of the data (``2`` for 2D and ``3`` for 3D).

    X : 4D/5D Numpy array
        Data. E.g. ``(num_of_images, y, x, channels)`` for ``2D`` or ``(num_of_images, z, y, x, channels)`` for ``3D``.

    Y : 2D Numpy array
        Image class. ``(num_of_images, class)``.

    data_path : List of str, optional
        If the data is in memory (``data_mode`` == ``'in_memory'``) this should contain the path to load images.

    ptype : str
        Problem type. Options ['mae','classification'].

    n_classes : int
        Number of classes to predict.

    seed : int, optional
        Seed for random functions.

    data_mode : str, optional
        Information about how the data needs to be managed. Options: ['in_memory', 'not_in_memory', 'chunked_data']

    da : bool, optional
        To activate the data augmentation.

    da_prob : float, optional
            Probability of doing each transformation.

    rotation90 : bool, optional
        To make square (90, 180,270) degree rotations.

    rand_rot : bool, optional
        To make random degree range rotations.

    rnd_rot_range : tuple of float, optional
        Range of random rotations. E. g. ``(-180, 180)``.

    shear : bool, optional
        To make shear transformations.

    shear_range : tuple of int, optional
        Degree range to make shear. E. g. ``(-20, 20)``.

    zoom : bool, optional
        To make zoom on images.

    zoom_range : tuple of floats, optional
        Zoom range to apply. E. g. ``(0.8, 1.2)``.

    zoom_in_z: bool, optional
        Whether to apply or not zoom in Z axis.

    shift : float, optional
        To make shifts.

    shift_range : tuple of float, optional
        Range to make a shift. E. g. ``(0.1, 0.2)``.

    affine_mode: str, optional
        Method to use when filling in newly created pixels. Same meaning as in `skimage` (and `numpy.pad()`).
        E.g. ``constant``, ``reflect`` etc.

    vflip : bool, optional
        To activate vertical flips.

    hflip : bool, optional
        To activate horizontal flips.

    elastic : bool, optional
        To make elastic deformations.

    e_alpha : tuple of ints, optional
        Strength of the distortion field. E. g. ``(240, 250)``.

    e_sigma : int, optional
        Standard deviation of the gaussian kernel used to smooth the distortion fields.

    e_mode : str, optional
        Parameter that defines the handling of newly created pixels with the elastic transformation.

    g_blur : bool, optional
        To insert gaussian blur on the images.

    g_sigma : tuple of floats, optional
        Standard deviation of the gaussian kernel. E. g. ``(1.0, 2.0)``.

    median_blur : bool, optional
        To blur an image by computing median values over neighbourhoods.

    mb_kernel : tuple of ints, optional
        Median blur kernel size. E. g. ``(3, 7)``.

    motion_blur : bool, optional
        Blur images in a way that fakes camera or object movements.

    motb_k_range : int, optional
        Kernel size to use in motion blur.

    gamma_contrast : bool, optional
        To insert gamma constrast changes on images.

    gc_gamma : tuple of floats, optional
        Exponent for the contrast adjustment. Higher values darken the image. E. g. ``(1.25, 1.75)``.

    dropout : bool, optional
        To set a certain fraction of pixels in images to zero.

    drop_range : tuple of floats, optional
        Range to take a probability ``p`` to drop pixels. E.g. ``(0, 0.2)`` will take a ``p`` folowing ``0<=p<=0.2``
        and then drop ``p`` percent of all pixels in the image (i.e. convert them to black pixels).

    val : bool, optional
        Advise the generator that the images will be to validate the model to not make random crops (as the val.
        data must be the same on each epoch). Valid when ``random_crops_in_DA`` is set.

    resize_shape : tuple of ints, optional
        If defined the input samples will be scaled into that shape.

    norm_dict : dict, optional
        Normalization instructions.

    convert_to_rgb : bool, optional
        In case RGB images are expected, e.g. if ``crop_shape`` channel is 3, those images that are grayscale are
        converted into RGB.
    """

    def __init__(
        self,
        ndim: int,
        X: np.ndarray | None,
        Y: np.ndarray | None,
        data_path: None | str = None,
        ptype: Literal["mae", "classification"] = "mae",
        n_classes: int = 2,
        seed: int = 0,
        data_mode: Literal["in_memory", "not_in_memory", "chunked_data"] = "in_memory",
        da: bool = True,
        da_prob: float = 0.5,
        rotation90: bool = False,
        rand_rot: bool = False,
        rnd_rot_range=(-180, 180),
        shear: bool = False,
        shear_range=(-20, 20),
        zoom: bool = False,
        zoom_range=(0.8, 1.2),
        zoom_in_z: bool = False,
        shift: bool = False,
        shift_range=(0.1, 0.2),
        affine_mode: Literal["constant", "edge", "symmetric", "reflect", "wrap"] = "constant",
        vflip: bool = False,
        hflip: bool = False,
        elastic: bool = False,
        e_alpha=(240, 250),
        e_sigma: int = 25,
        e_mode: Literal["constant", "edge", "symmetric", "reflect", "wrap"] = "constant",
        g_blur: bool = False,
        g_sigma: Tuple[float, float] = (1.0, 2.0),
        median_blur: bool = False,
        mb_kernel: Tuple[int, int] = (3, 7),
        motion_blur: bool = False,
        motb_k_range: Tuple[int, int] = (3, 8),
        gamma_contrast: bool = False,
        gc_gamma: Tuple[float, float] = (1.25, 1.75),
        dropout: bool = False,
        drop_range: Tuple[float, float] = (0, 0.2),
        val: bool = False,
        resize_shape: Tuple[int, ...] = (256, 256, 1),
        norm_dict: Dict | None = None,
        convert_to_rgb: bool = False,
    ):

        assert norm_dict != None, "Normalization instructions must be provided with 'norm_dict'"
        assert norm_dict["mask_norm"] in ["as_mask", "as_image", "none"]
        assert data_mode in ["in_memory", "not_in_memory", "chunked_data"]
        assert ptype in ["mae", "classification"]

        if data_mode == "in_memory":
            assert X is not None
            if X.ndim != (ndim + 2):
                raise ValueError("X must be a {}D Numpy array".format((ndim + 1)))

        if ptype == "classification":
            if data_mode == "in_memory" and (X is None or Y is None):
                raise ValueError("'X' and 'Y' need to be provided together with data_mode == 'in_memory'")
        else:
            if data_mode == "in_memory" and X is None:
                raise ValueError("'X' needs to be provided together with data_mode == 'in_memory'")

        self.ptype = ptype
        self.ndim = ndim
        self.z_size = -1
        self.convert_to_rgb = convert_to_rgb
        self.data_mode = data_mode
        self.norm_dict = norm_dict

        # Save paths where the data is stored
        if data_mode == "not_in_memory":
            assert data_path is not None
            self.data_path = data_path
            if ptype == "mae":
                self.all_samples = sorted(next(os.walk(data_path))[2])
            else:
                self.class_names = sorted(next(os.walk(data_path))[1])
                self.class_numbers = {}
                for i, c_name in enumerate(self.class_names):
                    self.class_numbers[c_name] = i
                self.classes = []
                self.all_samples = []
                print("Collecting data ids . . .")
                for folder in self.class_names:
                    print("Analizing folder {}".format(os.path.join(data_path, folder)))
                    ids = sorted(next(os.walk(os.path.join(data_path, folder)))[2])
                    print("Found {} samples".format(len(ids)))
                    for i in range(len(ids)):
                        self.classes.append(folder)
                        self.all_samples.append(ids[i])
                temp = list(zip(self.all_samples, self.classes))
                random.shuffle(temp)
                self.all_samples, self.classes = zip(*temp)
                del temp
                present_classes = np.unique(np.array(self.classes))
                if len(present_classes) != n_classes:
                    raise ValueError(
                        "MODEL.N_CLASSES is {} but {} classes found: {}".format(
                            n_classes, len(present_classes), present_classes
                        )
                    )

            self.length = len(self.all_samples)
            if self.length == 0:
                raise ValueError("No image found in {}".format(data_path))
        else:
            assert X is not None
            self.X = X
            if ptype == "classification":
                self.Y = Y

                present_classes = np.unique(np.array(self.Y))
                if len(present_classes) != n_classes:
                    raise ValueError(
                        "MODEL.N_CLASSES is {} but {} classes found: {}".format(
                            n_classes, len(present_classes), present_classes
                        )
                    )

            self.length = len(self.X)

        self.shape = resize_shape

        # X data analysis
        img, _ = self.load_sample(0, first_load=True)
        if norm_dict["enable"]:
            self.norm_dict["orig_dtype"] = img.dtype
            if norm_dict["type"] in ["div", "scale_range"]:
                if norm_dict["type"] == "div":
                    img, nsteps = norm_range01(img)
                else:
                    img, nsteps = norm_range01(img, div_using_max_and_scale=True)
                self.norm_dict.update(nsteps)
                if resize_shape[-1] != img.shape[-1]:
                    raise ValueError(
                        "Channel of the patch size given {} does not correspond with the loaded image {}. "
                        "Please, check the channels of the images!".format(resize_shape[-1], img.shape[-1])
                    )

        print("Normalization config used for X: {}".format(self.norm_dict))

        self.shape = resize_shape if resize_shape is not None else img.shape

        self.o_indexes = np.arange(self.length)
        self.n_classes = n_classes
        self.da = da
        self.da_prob = da_prob
        self.val = val
        self.zoom = zoom
        self.zoom_range = zoom_range
        self.zoom_in_z = zoom_in_z
        self.rand_rot = rand_rot
        self.rnd_rot_range = rnd_rot_range
        self.rotation90 = rotation90
        self.affine_mode = affine_mode
        self.gamma_contrast = gamma_contrast
        self.gc_gamma = gc_gamma

        self.da_options = []
        self.trans_made = ""
        if rotation90:
            self.trans_made += "_rot[90,180,270]"
        if rand_rot:
            self.trans_made += "_rrot" + str(rnd_rot_range)
        if shear:
            self.da_options.append(iaa.Sometimes(da_prob, iaa.Affine(rotate=shear_range, mode=affine_mode)))
            self.trans_made += "_shear" + str(shear_range)
        if zoom:
            self.trans_made += "_zoom" + str(zoom_range) + "+" + str(zoom_in_z)
        if shift:
            self.da_options.append(iaa.Sometimes(da_prob, iaa.Affine(translate_percent=shift_range, mode=affine_mode)))
            self.trans_made += "_shift" + str(shift_range)
        if vflip:
            self.da_options.append(iaa.Flipud(da_prob))  # type: ignore
            self.trans_made += "_vflip"
        if hflip:
            self.da_options.append(iaa.Fliplr(da_prob))  # type: ignore
            self.trans_made += "_hflip"
        if elastic:
            self.da_options.append(
                iaa.Sometimes(
                    da_prob,
                    iaa.ElasticTransformation(alpha=e_alpha, sigma=e_sigma, mode=e_mode),
                )
            )
            self.trans_made += "_elastic" + str(e_alpha) + "+" + str(e_sigma) + "+" + str(e_mode)
        if g_blur:
            self.da_options.append(iaa.Sometimes(da_prob, iaa.GaussianBlur(g_sigma)))
            self.trans_made += "_gblur" + str(g_sigma)
        if median_blur:
            self.da_options.append(iaa.Sometimes(da_prob, iaa.MedianBlur(k=mb_kernel)))
            self.trans_made += "_mblur" + str(mb_kernel)
        if motion_blur:
            self.da_options.append(iaa.Sometimes(da_prob, iaa.MotionBlur(k=motb_k_range)))
            self.trans_made += "_motb" + str(motb_k_range)
        if gamma_contrast:
            self.trans_made += "_gcontrast" + str(gc_gamma)
        if dropout:
            self.da_options.append(iaa.Sometimes(da_prob, iaa.Dropout(p=drop_range)))
            self.trans_made += "_drop" + str(drop_range)

        self.trans_made = self.trans_made.replace(" ", "")
        self.seq = iaa.Sequential(self.da_options)
        self.seed = seed
        ia.seed(seed)
        self.indexes = self.o_indexes.copy()
        self.random_crop_func = random_3D_crop_single if self.ndim == 3 else random_crop_single

    @abstractmethod
    def save_aug_samples(
        self,
        img: np.ndarray,
        orig_images: Dict,
        i: int,
        pos: int,
        out_dir: str,
        draw_grid: bool,
    ):
        """
        Save transformed samples in order to check the generator.

        Parameters
        ----------
        img : 3D/4D Numpy array
            Image to use as sample. E.g. ``(y, x, channels)`` for ``2D`` and ``(z, y, x, channels)`` for ``3D``.

        orig_images : dict
            Dict where the original image and mask are saved in "o_x" and "o_y", respectively.

        i : int
            Number of the sample within the transformed ones.

        pos : int
            Number of the sample within the dataset.

        out_dir : str
            Directory to save the images.

        draw_grid : bool
            Whether to draw a grid or not.
        """
        raise NotImplementedError

    @abstractmethod
    def ensure_shape(self, img: np.ndarray):
        """
        Ensures ``img`` correct axis number and their order.

        Parameters
        ----------
        img : Numpy array representing a ``2D`` or ``3D`` image
            Image to use as sample.

        Returns
        -------
        img : 3D/4D Numpy array
            Image to use as sample. E.g. ``(y, x, channels)`` for ``2D`` and ``(z, y, x, channels)`` for ``3D``.
        """
        raise NotImplementedError

    def __len__(self):
        """Defines the number of samples per epoch."""
        return self.length

    def load_sample(self, idx: int, first_load: bool = False) -> Tuple[np.ndarray, int]:
        """
        Load one data sample given its corresponding index.

        Parameters
        ----------
        idx : int
            Sample index counter.

        first_load : bool, optional
            Whether its the first time a sample is loaded to prevent normalizing it.

        Returns
        -------
        img : 3D/4D Numpy array
            X element. E.g. ``(y, x, channels)`` in  ``2D`` and ``(z, y, x, channels)`` in ``3D``.

        class : int
            Y element.
        """
        # Choose the data source
        if self.data_mode == "in_memory":
            img = np.squeeze(self.X[idx].copy())
            img_class = int(self.Y[idx]) if self.ptype == "classification" else 0
        else:
            sample_id = self.all_samples[idx]
            if self.ptype == "classification":
                sample_class_dir = self.classes[idx]
                f = os.path.join(self.data_path, sample_class_dir, sample_id)
                img_class = self.class_numbers[sample_class_dir]
            else:
                f = os.path.join(self.data_path, sample_id)
                img_class = 0
            img = np.load(f) if sample_id.endswith(".npy") else imread(f)
            img = np.squeeze(img)

        # X normalization
        if self.norm_dict["enable"] and not first_load:
            # Percentile clipping
            if "lower_bound" in self.norm_dict and self.norm_dict["application_mode"] == "image":
                img, _, _ = percentile_clip(
                    img,
                    lower=self.norm_dict["lower_bound"],
                    upper=self.norm_dict["upper_bound"],
                )

            if self.norm_dict["type"] == "div":
                img, _ = norm_range01(img)
            elif self.norm_dict["type"] == "scale_range":
                img, _ = norm_range01(img, div_using_max_and_scale=True)
            elif self.norm_dict["type"] == "custom":
                if self.norm_dict["application_mode"] == "image":
                    img = normalize(img, img.mean(), img.std())
                else:
                    img = normalize(img, self.norm_dict["mean"], self.norm_dict["std"])

        img = self.ensure_shape(img)

        return img, img_class

    def getitem(self, index: int) -> Tuple[torch.Tensor, int]:
        """
        Generation of one pair of data.

        Parameters
        ----------
        index : int
            Index counter.

        Returns
        -------
        item : tuple of 3D/4D Numpy arrays
            X and Y (if avail) elements. X is ``(z, y, x, channels)`` if ``3D`` or
            ``(y, x, channels)`` if ``2D``. Y is an integer.
        """
        return self.__getitem__(index)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int]:
        """
        Generation of one sample data.

        Parameters
        ----------
        index : int
            Sample index counter.

        Returns
        -------
        img : 3D/4D Numpy array
            X element, for instance, an image. E.g. ``(y, x, channels)`` in ``2D`` or
            ``(z, y, x, channels)`` in ``3D``.
        """
        img, img_class = self.load_sample(index)

        if img.shape[:-1] != self.shape[:-1]:
            img = self.random_crop_func(img, self.shape[:-1], self.val)
            img = resize_img(img, self.shape[:-1])  # type: ignore

        # Apply transformations
        if self.da:
            img = self.apply_transform(img)

        # If no normalization was applied, as is done with torchvision models, it can be an image of uint16
        # so we need to convert it to
        if img.dtype == np.uint16:
            img = torch.from_numpy(img.copy().astype(np.float32))
        else:
            img = torch.from_numpy(img.copy())

        return img, img_class

    def apply_transform(self, image: np.ndarray) -> np.ndarray:
        """
        Transform the input image with one of the selected choices based on a probability.

        Parameters
        ----------
        image : 3D/4D Numpy array
            Image to transform. E.g. ``(y, x, channels)`` in ``2D`` or ``(z, y, x, channels)`` in ``3D``.

        Returns
        -------
        image : 3D/4D Numpy array
            Transformed image. E.g. ``(y, x, channels)`` in ``2D`` or ``(z, y, x, channels)`` in ``3D``.
        """
        # Save shape
        o_img_shape = image.shape

        # Apply zoom
        if self.zoom and random.uniform(0, 1) < self.da_prob:
            image = zoom(
                image,
                zoom_range=self.zoom_range,
                zoom_in_z=self.zoom_in_z,
                mode=self.affine_mode,
                mask_type=self.norm_dict["mask_norm"],
            )  # type: ignore

        # Apply random rotations
        if self.rand_rot and random.uniform(0, 1) < self.da_prob:
            image = rotation(image, angles=self.rnd_rot_range, mode=self.affine_mode)  # type: ignore

        # Apply square rotations
        if self.rotation90 and random.uniform(0, 1) < self.da_prob:
            image = rotation(image, angles=[90, 180, 270], mode=self.affine_mode)  # type: ignore

        # Reshape 3D volumes to 2D image type with multiple channels to pass through imgaug lib
        if self.ndim == 3:
            image = image.reshape(image.shape[:2] + (image.shape[2] * image.shape[3],))

        # Apply gamma contrast
        if self.gamma_contrast and random.uniform(0, 1) < self.da_prob:
            image = gamma_contrast(image, gamma=self.gc_gamma)  # type: ignore

        # Apply transformations to the image
        image = self.seq(image=image)  # type: ignore

        # Recover the original shape
        image = image.reshape(o_img_shape)

        return image

    def draw_grid(self, im: np.ndarray, grid_width: int | None = None) -> np.ndarray:
        """
        Draw grid of the specified size on an image.

        Parameters
        ----------
        im : 3D/4D Numpy array
            Image to be modified. E.g. ``(y, x, channels)`` in ``2D`` or ``(z, y, x, channels)`` in ``3D``.

        grid_width : int, optional
            Grid's width.
        """
        v = np.max(im)
        if grid_width is not None:
            grid_y = grid_width
            grid_x = grid_width
        else:
            grid_y = im.shape[self.ndim - 2] // 5
            grid_x = im.shape[self.ndim - 2] // 5

        if self.ndim == 2:
            for i in range(0, im.shape[0], grid_y):
                im[i] = [v] * im.shape[-1]
            for j in range(0, im.shape[1], grid_x):
                im[:, j] = [v] * im.shape[-1]
        else:
            for k in range(0, im.shape[0]):
                for i in range(0, im.shape[2], grid_x):
                    im[k, :, i] = [v] * im.shape[-1]
                for j in range(0, im.shape[1], grid_y):
                    im[k, j] = [v] * im.shape[-1]
        return im

    def get_transformed_samples(
        self,
        num_examples: int,
        random_images: bool = True,
        save_to_dir: bool = True,
        out_dir: str = "aug",
        train: bool = False,
        draw_grid: bool = True,
    ):
        """
        Apply selected transformations to a defined number of images from the dataset.

        Parameters
        ----------
        num_examples : int
            Number of examples to generate.

        random_images : bool, optional
            Randomly select images from the dataset. If ``False`` the examples will be generated from the start of
            the dataset.

        save_to_dir : bool, optional
            Save the images generated. The purpose of this variable is to check the images generated by data
            augmentation.

        out_dir : str, optional
            Name of the folder where the examples will be stored.

        train : bool, optional
            To avoid drawing a grid on the generated images. This should be set when the samples will be used for
            training.

        draw_grid : bool, optional
            Draw a grid in the generated samples. Useful to see some types of deformations.

        Returns
        -------
        sample_x : 4D/5D Numpy array
            Batch of data. E.g. ``(num_examples, y, x, channels)`` in ``2D`` or ``(num_examples, z, y, x, channels)``
            in ``3D``.
        """

        if random_images == False and num_examples > self.length:
            num_examples = self.length
            print(
                "WARNING: More samples requested than the ones available. 'num_examples' fixed to {}".format(
                    num_examples
                )
            )

        sample_x = []

        # Generate the examples
        for i in tqdm(range(num_examples), disable=not is_main_process()):
            if random_images:
                pos = random.randint(0, self.length - 1) if self.length > 2 else 0
            else:
                pos = i

            img, img_class = self.load_sample(pos)

            if save_to_dir:
                orig_images = {}
                orig_images["o_x"] = np.copy(img)

            # Apply transformations
            if self.da:
                if not train and draw_grid:
                    img = self.draw_grid(np.copy(img))

                img = self.apply_transform(img)

            sample_x.append(img)

            if save_to_dir:
                self.save_aug_samples(sample_x[i], orig_images, i, pos, out_dir, draw_grid)

        print("### END TR-SAMPLES ###")
        return sample_x

    def get_data_normalization(self):
        return self.norm_dict
