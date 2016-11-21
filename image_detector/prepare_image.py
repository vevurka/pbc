
import numpy
from skimage import io

from skimage.color import rgb2gray
from skimage.transform import resize


SIZE = (300, 300)
PATH = '.'

def load_images():

    images = io.ImageCollection(PATH)

    images = [rgb2gray(resize(i, SIZE)) for i in images]

    return images




