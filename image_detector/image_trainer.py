# -*- coding: utf-8 -*-

import json
import numpy

from skimage import io
import matplotlib.pyplot as plt

from prepare_image import load_images
from prepare_image import display_image


def teach():
    """
    Manually choose which page is a text, image or blank sheet of paper.
    The result will be used later to train the classifier.
    """
    path = './data/images/*.jpg'
    images = load_images(path)
    results = []
    i = 0
    
    plt.ion()
    drawed = plt.imshow(numpy.zeros([300, 300]), cmap='Greys_r')
    
    for image in images:
        drawed.set_data(image)
        drawed.autoscale()
        plt.draw()
        print("Showing... [%s]" % i)
        inp = input("Text, graphic or empty? 0/1/2: \n")
        if not inp:
            inp = 0
        print(inp)
        
        results.append(int(inp))
        i += 1
    print(results)
    with open('./data/learned.json', 'w') as f:
        json.dump(results, f)
    return results


results = teach()



