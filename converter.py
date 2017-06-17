# -*- coding: utf-8 -*-

import glob
import logging
import os
import re
import subprocess

from utils import ConverterException


logger = logging.getLogger()


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
        """
        Yields file path to the converted jpg.
        """
        bundle_file = None
        djvu_files = glob.glob(self.glob_path)

        # Find the bundle file to determine how many images should we convert.
        for djvu_file in djvu_files:
            if self.file_is_bundle(djvu_file):
                bundle_file = djvu_file
                break

        if not bundle_file:
            raise ConverterException("Couldn't find the djvu bundle file!")

        pages_num = self.get_number_of_pages(bundle_file)
        for page in range(0, pages_num):
            yield self.to_jpg(bundle_file, page)

    def file_is_bundle(self, file_):
        """
        Instead of using costly djvudump, just peek the first 128 bytes of the
        djvu file and check whether it contains certain keyword.
        """
        with open(file_, 'rb') as descriptor:
            output = descriptor.read(128)
            if b'DJVMDIRM' in output:
                logger.info("Found bundle file.")
                return True

        return False

    def get_number_of_pages(self, file):
        with subprocess.Popen([self.config['converter']['djvudump'], file],
                              stdout=subprocess.PIPE) as p:
            out, err = p.communicate()

            out = out.decode()
            out = out[:100]
            if "Document directory" in out:
                return int(re.search("([0-9]+)\ pages", out).group(1))

        raise ConverterException("Failed to get number of pages!")

    def to_jpg(self, bundle_file, page):
        pdf_tmpfile_path = self.djvu_to_pdf(bundle_file, page)
        jpg_file_path = self.pdf_to_jpg(pdf_tmpfile_path, page)

        if not self.error:
            return jpg_file_path
        return None

    def djvu_to_pdf(self, djvu_file_path, page):
        pdf_file_path = djvu_file_path.rstrip('djvu') + 'pdf'
        try:
            subprocess.check_call([self.djvu_bin, "--format=pdf", "--page=%s" % page, djvu_file_path, pdf_file_path])
        except subprocess.CalledProcessError:
            self.error = "Failed to convert file to pdf!"
            logger.error(self.error)
        return pdf_file_path

    def pdf_to_jpg(self, pdf_tmpfile_path, page):
        jpg_file_path = pdf_tmpfile_path.rstrip('.pdf') + '_%s.jpg' % page

        try:
            subprocess.check_call(["convert", pdf_tmpfile_path, jpg_file_path])
        except subprocess.CalledProcessError:
            self.error = "Failed to convert file to jpg!"
            logger.error(self.error)
        return jpg_file_path
