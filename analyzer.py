# -*- coding: utf-8 -*-

import os

from converter import Converter
from image_detector.categorizer import Categorizer


class ImageAnalyzer(Categorizer):

    """
    Decide which image is worth publishing.
    """

    def __init__(self, config):
        self.config = config
        Categorizer.__init__(self)

    def get_best_result(self, results_dict):
        if results_dict:
            return max(results_dict, key=results_dict.get)
        else:
            return None

    def get_preferred_key(self, percent_results):
        """
        Since the classification from classifier.predict and classifier.predict_proba
        differ, sometimes we want to get the prediction of the highest value.
        text / image / blank

        UNUSED NOW
        """
        return max(percent_results, key=percent_results.get)

    def run(self):
        results_dict = {}
        converter = Converter(self.config)
        i = 0
        for jpg_file_path in converter.iterate():

            results = self.categorize_image(jpg_file_path)
            print(results['verdict'], jpg_file_path)
            percent_results = results['percent']
            if results['percent']['image'] >= 30.0:
                results_dict[jpg_file_path] = percent_results['image']
                i += 1
                if i > 10:
                    break
            else:
                os.remove(jpg_file_path)

        return self.get_best_result(results_dict)
