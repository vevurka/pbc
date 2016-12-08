# -*- coding: utf-8 -*-

import os
import glob
import configparser
import subprocess

from converter import Converter
from image_detector.categorizer import Categorizer


class Analyzer(Categorizer):
    
    def __init__(self, config):
        self.config = config
        Categorizer.__init__(self)
    
    def file_is_bundle(self, file):
        try:
            p = subprocess.check_call(["djvm", "-l", file],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,)
            out, err = p.communicate()
        except subprocess.CalledProcessError:
            return False
            
        if "Can't find form DJVM" in out:
            return False
        elif "Size" in out:
            print("Oh, we shouldn't convert that.")
            return True
        else:
            return False

    def run(self):
        converter = Converter(self.config)
        
        for file in glob.glob(os.path.join(self.config['files']['zipdir'], '*.djvu')):
            print(file)
            if not self.file_is_bundle(file):
                jpg_file_path = converter.to_jpg(file)
                self.categorize(jpg_file_path)
            
            
config = configparser.ConfigParser()
config.read('config.conf')
analyzer = Analyzer(config)
analyzer.run()