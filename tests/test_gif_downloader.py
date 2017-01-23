# -*- coding: utf-8 -*-

import logging
import os
import sqlite3
import unittest
from unittest import mock

from gif_downloader import GifDownloader


class MockedRequest(object):

    text = None


class TestGifDownloader(unittest.TestCase):

    def setUp(self):
        #os.system('sqlite3 -init config/db_init.sql mocked.db')
        pass

    @mock.patch('logging.Logger')
    def get_downloader(self, mock_logger):
        return GifDownloader(
            mock_logger,
            {'default': {'pankreator_site': 'http://pankreator.org'}})

    @mock.patch('requests.get')
    def test_extract_data_from_page(self, method):
        with open('tests/data/pankreator.html') as html:
            m = MockedRequest()
            m.text = html.read()
            method.return_value = m
        downloader = self.get_downloader()
        result = downloader.extract_data_from_page()
        gif_url = 'http://pankreator.org/images/16237258_10211877173311574_2136600893_n.gif'
        url = 'http://pankreator.org/index.php?option=com_content&view=article&id=46:wicia-na-kocie-jedzie&catid=8&Itemid=101'
        title = 'Wicia na kocie jedzie!'
        self.assertEqual(result[0]['gif_url'], gif_url)
        self.assertEqual(result[0]['url'], url)
        self.assertEqual(result[0]['title'], title)

    @mock.patch('requests.get')
    def test_extract_data_from_page_failed(self, method):
        with open('tests/data/pankreator_incorrect.html') as html:
            m = MockedRequest()
            m.text = html.read()
            method.return_value = m
        downloader = self.get_downloader()
        result = downloader.extract_data_from_page()
        self.assertEqual(result, [])

    """
    @mock.patch('gif_downloader.GifDownloader.extract_data_from_page')
    @mock.patch('sqlite3.connect')
    def test_check_new_posts(self, method, connect):
        method.return_value = [{'title': 'mocked', 'gif_url': 'mocked'}]
        downloader = self.get_downloader()
        connect.side_effect = sqlite3.connect('test/data/test_db.db')
    """
