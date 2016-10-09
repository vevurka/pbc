#!/bin/env python

import subprocess


class Converter(object):

    def __init__(self, djvu_file, jpg_file):
        self.djvu_bin = "ddjvu"
        self.djvu_file = djvu_file
        self.jpg_file = jpg_file

    def convert(self):
        pnm = self.convert_to_pnm()
        self.convert_to_jpg(pnm)

    def convert_to_pnm(self):
        tmpfile = "tmp.pnm"
        p = subprocess.check_call([self.djvu_bin, "--format=pnm", self.djvu_file, tmpfile],
                                  stdout=subprocess.PIPE)
        print([a for a in p.stdout.readline()])
        return tmpfile

    def convert_to_jpg(self, pnm):
        subprocess.check_call(["convert", pnm, self.jpg_file],
                              stdout=subprocess.PIPE)
