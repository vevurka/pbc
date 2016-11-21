
import json
import matplotlib.pyplot as plt
from skimage import io

from prepare_image import load_images


def display_image(image):
    plt.ion()
    plt.imshow(image)
    plt.show()


def teach():
    
    images = load_images()
    results = {}
    i = 0
    for image in images:
        display_image(image)
        print("Showing... [%s]" % i)
        inp = input("Graphic or text? 1/0: \n")
        if not inp:
            inp = 0
        
        results[str(i)] = int(inp)
        i += 1
    print(results)
    with open('learned.json', 'w') as f:
        json.dump(results, f)
    return results


results = teach()



