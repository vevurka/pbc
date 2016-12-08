# -*- coding: utf-8 -*-

import os
import subprocess


class Converter(object):

    """
    Convert the file:
    1) from djvu to pnm
    2) from pnm to jpg

    Srsly, no easier way.
    """

    def __init__(self, config):
        self.config = config
        self.djvu_bin = config['converter']['djvu_bin']
        self.error = None

    def to_jpg(self, djvu_filename):
        
        djvu_file_path = os.path.join(self.config['files']['zipdir'], djvu_filename)

        pdf_tmpfile_path = self.djvu_to_pdf(djvu_file_path)
        jpg_file_path = self.pdf_to_jpg(pdf_tmpfile_path)

        if not self.error:
            return jpg_file_path
        return None

    def djvu_to_pdf(self, djvu_file_path):
        print('Converting to pdf...')
        pdf_file_path = djvu_file_path.rstrip('djvu') + 'pdf'
        try:
            subprocess.check_call([self.djvu_bin, "--format=pdf", djvu_file_path, pdf_file_path],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,)
        except Exception as e:
            print(e)
            self.error = "Failed to convert file to pdf!"
            print(self.error)
        return pdf_file_path

    def pdf_to_jpg(self, pdf_tmpfile_path):
        print("Converting to jpg...")
        jpg_file_path = pdf_tmpfile_path.rstrip('pdf') + 'jpg'

        try:
            subprocess.check_call(["convert", pdf_tmpfile_path, jpg_file_path],
                                  stdout=subprocess.PIPE)
        except Exception as e:
            self.error = "Failed to convert file to jpg!"
            print(self.error)
        self.cleanup(pdf_tmpfile_path)
        return jpg_file_path


    def cleanup(self, file_path):
        os.remove(file_path)

        # Since we don't really know how many files convert will produce,
        # we need to check it.
        #zero_file = os.path.join(self.config['files']['imagesdir'], 'new_image-0.jpg')
        #if os.path.isfile(self.jpg_file):
        #    return self.jpg_file
        #elif os.path.isfile(zero_file):
        #    return zero_file
        #else:
        #    return None
