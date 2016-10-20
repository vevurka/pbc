# -*- coding: utf-8 -*-

import os
import subprocess


class Converter(object):

    """
    Convert the file:
    1) from djvu to pnm
    2) from pnm to jpg

    Srsly, no easiest way.
    """

    def __init__(self, config, djvu_filename):
        self.config = config
        self.djvu_file = os.path.join(config['files']['zipdir'], djvu_filename)
        self.djvu_bin = config['converter']['djvu_bin']
        self.jpg_file = config['files']['jpg_path']
        self.pnm_tmpfile = config['files']['pnm_tmpfile']
        self.error = None

    def convert(self):
        pnm = self.convert_to_pnm()
        jpg = self.convert_to_jpg(pnm)

        if not self.error:
            return jpg
        return None

    def convert_to_pnm(self):
        print('Converting to pnm...')
        try:
            subprocess.check_call([self.djvu_bin, "--format=pnm", self.djvu_file, self.pnm_tmpfile],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,)
        except Exception as e:
            print(e)
            self.error = "Failed to convert file to pnm!"
            print(self.error)
        return self.pnm_tmpfile

    def convert_to_jpg(self, pnm):
        print("Converting to jpg...")
        try:
            subprocess.check_call(["convert", pnm, self.jpg_file],
                                  stdout=subprocess.PIPE)
        except Exception as e:
            self.error = "Failed to convert file to jpg!"
            print(self.error)
            return None

        # Since we don't really know how many files convert will produce,
        # we need to check it.
        zero_file = os.path.join(self.config['files']['imagesdir'], 'new_image-0.jpg')
        if os.path.isfile(self.jpg_file):
            return self.jpg_file
        elif os.path.isfile(zero_file):
            return zero_file
        else:
            return None
