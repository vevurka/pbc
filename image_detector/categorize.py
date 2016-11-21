
import json
import numpy
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import KFold, cross_val_score

from prepare_image import load_images


def categorize(images, results):

    classifier = SVC(kernel='linear')
    
    data = images.reshape((len(images), -1))
    
    #target = numpy.array(list(results.values()), dtype=numpy.uint8)
    
    target = numpy.array([results[i] for i in results], dtype=numpy.uint8)
    
    x_train, x_test, y_train, y_test = train_test_split(
        data, target, test_size=0.25, random_state=0
    )

    # 5 fold cross validation. :o
    cross_validation = KFold(len(y_train), 5, shuffle=True, random_state=0)
    scores = cross_val_score(classifier, x_train, y_train, cv=cross_validation)
    print(scores)
    print(target)
    
    classifier.fit(x_train, y_train)
    print(classifier.score(x_train, y_train))
    
    print(classifier.predict(data[21]))
    

def run():
    
    images = load_images()
    images = numpy.array(images, dtype=numpy.uint8)
    
    with open('learned.json', 'r') as f:    
        results = json.load(f)
        categorize(images, results)

run()