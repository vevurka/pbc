# -*- coding: utf-8 -*-

import glob
import os
import re
import subprocess


class Converter(object):

    """
    Converts djvu to jpg.
    """

    def __init__(self, config):
        self.config = config
        self.glob_path = os.path.join(config['files']['zipdir'], '*.djvu')

        self.djvu_bin = config['converter']['ddjvu']
        self.error = None

    def iterate(self):

        bundle_file = list(filter(self.file_is_bundle, glob.glob(self.glob_path)))[0]

        for page in range(0, self.pages):
            yield self.to_jpg(bundle_file, page)

    def file_is_bundle(self, file):
        out = ''
        with subprocess.Popen([self.config['converter']['djvudump'], file],
                                 stdout=subprocess.PIPE) as p:
            out, err = p.communicate()

            out = out.decode()
            out = out[:100]
            if "Document directory" in out:
                self.pages = int(re.search("([0-9]+)\ pages", out).group(1))
                print("I will be iterating over %s pages." % self.pages)
                return True

        return False

    def to_jpg(self, bundle_file, page):

        pdf_tmpfile_path = self.djvu_to_pdf(bundle_file, page)

        jpg_file_path = self.pdf_to_jpg(pdf_tmpfile_path, page)

        if not self.error:
            return jpg_file_path
        return None

    def djvu_to_pdf(self, djvu_file_path, page):
        print('Converting to pdf...')
        pdf_file_path = djvu_file_path.rstrip('djvu') + 'pdf'
        try:
            subprocess.check_call([self.djvu_bin, "--format=pdf", "--page=%s" % page, djvu_file_path, pdf_file_path])
        except subprocess.CalledProcessError:
            self.error = "Failed to convert file to pdf!"
            print(self.error)
        return pdf_file_path

    def pdf_to_jpg(self, pdf_tmpfile_path, page):
        print("Converting to jpg...")
        jpg_file_path = pdf_tmpfile_path.rstrip('.pdf') + '_%s.jpg' % page

        try:
            subprocess.check_call(["convert", pdf_tmpfile_path, jpg_file_path])
        except subprocess.CalledProcessError:
            self.error = "Failed to convert file to jpg!"
            print(self.error)
        return jpg_file_path
