# -*- coding: utf-8 -*-

import logging
import json
import numpy
from skimage import io

from sklearn.externals import joblib
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import KFold, cross_val_score

from .prepare_image import load_images, prepare_image


logger = logging.getLogger()


class Categorizer(object):

    TEXT = 0
    IMAGE = 1
    BLANK_PAGE = 2

    """
    This class implements machine learning algorithm for images classification.
    By default, it will use pre-trained classifier from pickled python object.

    To train new classifier, specify images path and json with target data.
    Be cautious! Order of the images and targed data is relevant!
    """

    def __init__(self, pre_trained=True):
        if pre_trained:
            self.classifier = joblib.load('./image_detector/data/trained_classifier.pkl')
        else:
            self.classifier = self.load_dataset('./image_detector/data/images/*.jpg')

    def train_classifier(self, images, results):
        """
        Feed the Support Vector Machine with data.
        train_test_split is used to split the data to train and test groups.
        """
        data = images.reshape((len(images), -1))
        target = numpy.array(results, dtype=numpy.uint8)

        classifier = SVC(kernel='linear', probability=True)

        x_train, x_test, y_train, y_test = train_test_split(
            data, target, test_size=0.25, random_state=0
        )

        cross_validation = KFold(len(y_train), 5, shuffle=True, random_state=0)
        scores = cross_val_score(classifier, x_train, y_train, cv=cross_validation)

        classifier.fit(x_train, y_train)

        logger.info(scores)
        logger.info(classifier.score(x_train, y_train))

        return classifier

    def load_dataset(self, learn_path):
        """
        Load images along with the classification list and train the classifier.
        """
        images = load_images(learn_path)
        images = numpy.array(images, dtype=numpy.uint8)

        with open('./image_detector/data/new_learned.json', 'r') as f:
            results = json.load(f)
            classifier = self.train_classifier(images, results)
            joblib.dump(
                classifier,
                './image_detector/data/trained_classifier.pkl',
                compress=9
            )

        return classifier

    def categorize_image(self, image_path):
        """
        Get one image and try to guess what it may be.
        - text
        - image
        - blank page
        The result is returned in percent.
        """
        prepared = prepare_image(io.imread(image_path)).ravel()

        # Get the most probable prediction.
        prediction = self.classifier.predict(prepared)

        # Get percent values for all alternatives.
        prediction_percent = self.classifier.predict_proba(prepared)

        logger.info("%s %s" % (prediction, prediction_percent))

        return {
            'path': image_path,
            'verdict': prediction[0],
            'percent': {
                'text': round(prediction_percent[0][self.TEXT], 3) * 100,
                'image': round(prediction_percent[0][self.IMAGE], 3) * 100,
                'blank': round(prediction_percent[0][self.BLANK_PAGE], 3) * 100,
            }
        }
