
import json
import numpy
from skimage import io

from sklearn import metrics
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import KFold, cross_val_score

from prepare_image import load_images, prepare_image, display_image


def categorize(images, results):

    new_data = io.imread('/home/sir/Aktywatory/PANkreator_src/files/do_rozpoznania.jpg')
    rescaled = prepare_image(new_data)
    rescaled = rescaled.ravel()

    classifier = SVC(kernel='linear')
    
    data = images.reshape((len(images), -1))
    
    print(results)
    target = numpy.array(results, dtype=numpy.uint8)
    print(target)

    x_train, x_test, y_train, y_test = train_test_split(
        data, target, test_size=0.25, random_state=0
    )

    # 5 fold cross validation. :o
    cross_validation = KFold(len(y_train), 5, shuffle=True, random_state=0)
    scores = cross_val_score(classifier, x_train, y_train, cv=cross_validation)
    print(scores)
    
    classifier.fit(x_train, y_train)
    print(classifier.score(x_train, y_train))

     

    print(classifier.predict(data[193]))
    print(classifier.predict(data[24]))
    print(classifier.predict(data[107]))

    print('ha!')
    print(classifier.predict(rescaled))
    print('______________________')


    print(classifier.coef_ )
    

def run():
    
    images = load_images()
    images = numpy.array(images, dtype=numpy.uint8)
    
    with open('learned.json', 'r') as f:    
        results = json.load(f)
        categorize(images, results)

run()