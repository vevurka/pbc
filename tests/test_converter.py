# -*- coding: utf-8 -*-

import unittest
from unittest import mock

from converter import Converter
from utils import ConverterException


class TestConverter(unittest.TestCase):

    def get_converter(self):
        return Converter(
            {'files': {'zipdir': 'aaaa'},
             'converter': {'ddjvu': 'ddjvu',
                           'djvudump': 'djvudump'},
             })

    def test_file_is_bundle(self):
        converter = self.get_converter()
        self.assertEqual(False, converter.file_is_bundle('tests/data/regular.djvu'))
        self.assertEqual(True, converter.file_is_bundle('tests/data/bundle.djvu'))
        self.assertEqual(False, converter.file_is_bundle('tests/data/incorrect_file.djvu'))

    def test_get_number_of_pages(self):
        converter = self.get_converter()
        file_ = 'tests/data/bundle.djvu'
        self.assertEqual(12, converter.get_number_of_pages(file_))

    def test_get_number_of_pages_raises_exception_on_not_bundle(self):
        # Should raise an exception on non bundle file.
        converter = self.get_converter()
        file_ = 'tests/data/regular.djvu'
        with self.assertRaises(ConverterException):
            converter.get_number_of_pages(file_)

    @mock.patch('converter.Converter.to_jpg', return_value='')
    def test_iterate_correct_djvu(self, *args):
        converter = self.get_converter()
        converter.glob_path = 'tests/data/djvu_dir/*.djvu'
        times_ran = 0
        for path in converter.iterate():
            times_ran += 1
        self.assertEqual(64, times_ran)

    @mock.patch('converter.Converter.file_is_bundle', return_value=False)
    def test_iterate_bundle_not_found(self, *args):
        converter = self.get_converter()
        converter.glob_path = 'tests/data/djvu_dir/*.fake'
        with self.assertRaisesRegexp(ConverterException, "Couldn't find the djvu bundle file!"):
            times_ran = 0
            for path in converter.iterate():
                times_ran += 1
        self.assertEqual(0, times_ran)
