# -*- coding: utf-8 -*-

from skimage import io

from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage.transform import resize


SIZE = (300, 300)


def prepare_image(image):
    """
    Reduce the image to gray, resize and remove the background.
    """
    resized = rgb2gray(resize(image, SIZE))
    filtered = threshold_otsu(resized)

    return resized > filtered


def load_images(images_path):
    """
    Return the numpy array of images.
    """
    images = io.ImageCollection(images_path)
    images = [prepare_image(i) for i in images]

    return images
