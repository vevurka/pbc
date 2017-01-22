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
             'converter': {'ddjvu': 'ddjvu'}})

    def test_file_is_bundle(self):
        converter = self.get_converter()
        self.assertEqual(converter.file_is_bundle('tests/data/regular.djvu'), False)
        self.assertEqual(converter.file_is_bundle('tests/data/bundle.djvu'), True)
        self.assertEqual(converter.file_is_bundle('tests/data/incorrect_file.djvu'), False)