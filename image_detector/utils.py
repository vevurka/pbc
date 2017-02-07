
import matplotlib.pyplot as plt


# Aux functions for trainer.

def display_image(image):
    plt.ion()
    plt.imshow(image, cmap='Greys_r')
    plt.draw()