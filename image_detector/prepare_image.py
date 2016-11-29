
import numpy
import matplotlib.pyplot as plt
from skimage import io

from skimage.color import rgb2gray
from skimage import segmentation
from skimage.filters import threshold_otsu
from skimage.transform import resize


SIZE = (300, 300)
#PATH = '/home/sir/Aktywatory/PANkreator_src/learn3/*.jpg'
PATH = '/home/sir/Aktywatory/PANkreator_src/learn/*.jpg'

def display_image(image):
    plt.ion()
    plt.imshow(image) #, cmap='Greys_r')
    plt.show()


def prepare_image(image):
    
    resized = rgb2gray(resize(image, SIZE))
    
    filtered = threshold_otsu(resized)
    
    return resized > filtered


def load_images():
    images = io.ImageCollection(PATH)
    images = [prepare_image(i) for i in images]
    return images




