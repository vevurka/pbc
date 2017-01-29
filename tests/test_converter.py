# -*- coding: utf-8 -*-


import logging
import unittest
from unittest import mock

from converter import Converter


class TestConverter(unittest.TestCase):

    @mock.patch('logging.Logger')
    def get_converter(self, mock_logger):
        return Converter(
            mock_logger,
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
        with self.assertRaises(Exception):
            converter.get_number_of_pages(file_)
