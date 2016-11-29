
import json

from skimage import io

from prepare_image import load_images
from prepare_image import display_image


def teach():
    
    images = load_images()
    print(images)
    results = []
    i = 0
    for image in images:
        display_image(image)
        print("Showing... [%s]" % i)
        inp = input("Graphic or text? 1/0: \n")
        if not inp:
            inp = 0
        print(inp)
        
        results.append(int(inp))
        i += 1
    print(results)
    with open('learned.json', 'w') as f:
        json.dump(results, f)
    return results


results = teach()



