#!/bin/env python

import subprocess


class Converter(object):

    def __init__(self, djvu_file, jpg_file):
        self.djvu_bin = "/usr/bin/ddjvu"
        self.djvu_file = djvu_file
        self.jpg_file = jpg_file
        self.error = None

    def convert(self):
        pnm = self.convert_to_pnm()
        self.convert_to_jpg(pnm)
        return self.error

    def convert_to_pnm(self):
        pnm_tmpfile = "/home/sir/Aktywatory/PANkreator_src/pbc/temp.pnm"
        try:
            p = subprocess.check_call([self.djvu_bin, "--format=pnm", self.djvu_file, pnm_tmpfile],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,)
            output, error = p.communicate()
            print(output, error)
        except Exception as e:
            self.error = "Nie udało się skonwertować do pnm!"
        return pnm_tmpfile

    def convert_to_jpg(self, pnm):
        try:
            subprocess.check_call(["convert", pnm, self.jpg_file],
                                  stdout=subprocess.PIPE)
        except Exception as e:
            self.error = "Nie udało się skowertować do jpg!"
