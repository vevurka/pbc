#!/bin/env python

import subprocess


class Converter(object):

    def __init__(self, config):
        self.djvu_bin = config['converter']['djvu_bin']
        self.djvu_file = config['image']['image_path']
        self.jpg_file = config['image']['jpg_path']
        self.pnm_tmpfile = config['image']['pnm_tmpfile']
        self.error = None

    def convert(self):
        pnm = self.convert_to_pnm()
        self.convert_to_jpg(pnm)
        return self.error

    def convert_to_pnm(self):
        try:
            p = subprocess.check_call([self.djvu_bin, "--format=pnm", self.djvu_file, self.pnm_tmpfile],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,)
            output, error = p.communicate()
            print(output, error)
        except Exception as e:
            self.error = "Nie udało się skonwertować do pnm!"
        return self.pnm_tmpfile

    def convert_to_jpg(self, pnm):
        try:
            subprocess.check_call(["convert", pnm, self.jpg_file],
                                  stdout=subprocess.PIPE)
        except Exception as e:
            self.error = "Nie udało się skowertować do jpg!"
