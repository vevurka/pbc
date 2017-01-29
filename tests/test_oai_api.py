# -*- coding: utf-8 -*-

import logging
import unittest
from unittest import mock
from unittest.mock import Mock
from sickle import Sickle

from oai_api import LibraryCrawler

"""
class Iterator(object):

    def __init__(self):
        self.number = 1

    def __iter__(self):
        return self

    def next(self):
        if self.number < 1:
            raise StopIteration
        self.number -= 1
        return self.record

    class record:
        class metadata:
            def __getitem__(self, key):
                return {'type': ['gazeta']}
"""


class TestConverter(unittest.TestCase):

    @mock.patch('logging.Logger')
    def get_crawler(self, mock_logger):
        return LibraryCrawler(
            mock_logger,
            {'default': {'oai_api_url': 'fake'}},
            {'type': ['gazeta']}
        )

    @mock.patch('sickle.Sickle.ListRecords', return_value=iter([1, 2, 3]))
    @mock.patch('oai_api.LibraryCrawler.get_token', side_effect=lambda: 'aaa')
    def test_query_iterator(self, *args):

        res = Mock(complete_list_size=100, token='_DL_LAST_ITEM_2000_DL_')
        crawler = self.get_crawler()
        crawler.resumption_token = res
        l = list(crawler.query_itarator())
        self.assertEqual([1, 2, 3], l)

    """
    # TODO: simulate sickle iterator and complete this.
    @mock.patch('sickle.Sickle.ListRecords', return_value=iter([1, 2, 3]))
    @mock.patch('oai_api.LibraryCrawler.get_token', side_effect=lambda: 'aaa')
    @mock.patch('oai_api.LibraryCrawler.query_itarator', side_effect=Iterator)
    def test_run(self, *args):
        crawler = self.get_crawler()
        crawler.run()
    """

    def test_book_is_small_enough(self):
        lc = LibraryCrawler
        self.assertEqual(True, lc.is_small_enough([]))
        self.assertEqual(True, lc.is_small_enough(['[6] k.', '8°']))
        self.assertEqual(True, lc.is_small_enough(['[8] k., 100 s.,']))
        self.assertEqual(False, lc.is_small_enough(['[8] k., 730 s.,']))

if __name__ == '__main__':
    unittest.main()
