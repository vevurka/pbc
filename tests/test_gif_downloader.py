# -*- coding: utf-8 -*-

import os
import sqlite3
import unittest
from unittest import mock

from gif_downloader import GifDownloader


class MockedRequest(object):

    text = None


class TestGifDownloader(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect('tests/data/test_db.db',
                                          detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = self.connection.cursor()
        with open('config/db_init.sql') as file:
            cursor.execute(file.read())

    def tearDown(self):
        self.connection.close()
        os.remove('tests/data/test_db.db')

    @mock.patch('logging.Logger')
    def get_downloader(self, mock_logger):
        return GifDownloader(
            mock_logger,
            {'default': {'pankreator_site': 'http://pankreator.org'},
             'files': {'gif_path': 'gif'}},
            'tests/data/test_db.db')

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

    @mock.patch('sqlite3.connect')
    def test_check_new_posts_empty_html(self, connect):
        downloader = self.get_downloader()
        connect.side_effect = sqlite3.connect('tests/data/test_db.db')
        result1, result2 = downloader.check_new_posts()
        self.assertEqual((result1, result2), (None, None))

    @mock.patch('gif_downloader.GifDownloader.download_image')
    @mock.patch('gif_downloader.GifDownloader.extract_data_from_page')
    @mock.patch('sqlite3.connect')
    def test_check_new_posts_existing_record(self, m_connect, m_extract, m_download):
        m_extract.return_value = [{'title': 'mocked', 'gif_url': 'http://mocked.com/gif.gif'}]
        m_download.return_value = 'gif'
        downloader = self.get_downloader()
        cursor = self.connection.cursor()
        cursor.execute('insert into pankreator_gifs (id, gif_url) values (1, "http://mocked.com/gif.gif")')
        self.connection.commit()
        m_connect.return_value = self.connection
        result1, result2 = downloader.check_new_posts()
        self.assertEqual((result1, result2), (None, None))

    @mock.patch('gif_downloader.GifDownloader.download_image')
    @mock.patch('gif_downloader.GifDownloader.extract_data_from_page')
    @mock.patch('utils.db_connection')
    def test_check_new_posts_new_record(self, m_connect, m_extract, m_download):
        m_extract.return_value = [{'title': 'mocked', 'gif_url': 'http://mocked.com/gif.gif'}]
        m_download.return_value = 'gif'
        downloader = self.get_downloader()
        m_connect.return_value = self.connection
        result1, result2 = downloader.check_new_posts()
        self.assertEqual(result1, 'gif')
        self.assertEqual(result2['gif_url'], 'http://mocked.com/gif.gif')