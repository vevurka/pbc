# -*- coding: utf-8 -*-

import glob
import json
import numpy
from collections import OrderedDict
from natsort import natsorted

import matplotlib.pyplot as plt

from .prepare_image import load_images


def teach():
    """
    Manually choose which page is a text, image or blank sheet of paper.
    The result will be used later to train the classifier.
    """
    path = './image_detector/data/images/*.jpg'
    images_list = natsorted(glob.glob(path))
    print(images_list[-1])
    images = load_images(path)
    results = OrderedDict()
    i = 0

    plt.ion()
    drawed = plt.imshow(numpy.zeros([300, 300]), cmap='Greys_r')

    for filename, image in zip(images_list, images):
        drawed.set_data(image)
        drawed.autoscale()
        plt.draw()
        print("Showing... [%s], %s" % (i, filename))
        inp = input("Text, graphic or empty? 0/1/2: \n")
        if not inp:
            inp = 0
        print(inp)

        results[filename] = int(inp)
        i += 1

    print(results.values())
    with open('./image_detector/data/learned.json', 'w') as f:
        json.dump(results.values(), f)
    return results


results = teach()



