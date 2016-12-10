# -*- coding: utf-8 -*-

import os
import configparser

from converter import Converter
from image_detector.categorizer import Categorizer


class Analyzer(Categorizer):

    def __init__(self, config):
        self.config = config
        Categorizer.__init__(self)

    def run(self):
        converter = Converter(self.config)

        for jpg_file_path in converter.iterate():

            results = self.categorize_image(jpg_file_path)
            print(results['verdict'], jpg_file_path)
            percent_results = results['percent']
            preferred_key = max(percent_results, key=percent_results.get)
            if preferred_key == 'image':
                print(preferred_key, results)
            else:
                os.remove(jpg_file_path)


config = configparser.ConfigParser()
config.read('config.conf')
analyzer = Analyzer(config)
analyzer.run()