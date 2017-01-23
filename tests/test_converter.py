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
        self.assertEqual(converter.file_is_bundle('tests/data/regular.djvu'), False)
        self.assertEqual(converter.file_is_bundle('tests/data/bundle.djvu'), True)
        self.assertEqual(converter.file_is_bundle('tests/data/incorrect_file.djvu'), False)

    def test_get_number_of_pages(self):
        converter = self.get_converter()
        file_ = 'tests/data/bundle.djvu'
        self.assertEqual(converter.get_number_of_pages(file_), 12)

    def test_get_number_of_pages(self):
        converter = self.get_converter()
        file_ = 'tests/data/regular.djvu'
        with self.assertRaises(Exception):
            converter.get_number_of_pages(file_)
