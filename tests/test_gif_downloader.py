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

    def get_downloader(self):
        return GifDownloader(
            {'default': {'pankreator_site': 'http://pankreator.org'},
             'files': {'gif_path': 'gif'}},
            'tests/data/test_db.db')

    def test_compare_results_the_same(self):
        downloader_cls = GifDownloader
        diffs = downloader_cls.compare_results(
            [(1, 'title', 'url', 'first gif', 'fake date'), (1, 'title', 'url', 'second gif', 'fake date')],
            [{'attr': 'blabla', 'gif_url': 'first gif'}, {'attr': 'blabla', 'gif_url': 'second gif'}]
        )
        self.assertEqual(set(), diffs)

    def test_compare_results_one_differs(self):
        downloader_cls = GifDownloader
        diffs = downloader_cls.compare_results(
            [(1, 'title', 'url', 'first gif', 'fake date'), (1, 'title', 'url', 'second gif', 'fake date')],
            [{'attr': 'blabla', 'gif_url': 'first gif'}, {'attr': 'blabla', 'gif_url': 'one that differs'}]
        )
        # Note that we always expect new item in the list from website.
        self.assertEqual({'one that differs'}, diffs)

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
        self.assertEqual(gif_url, result[0]['gif_url'])
        self.assertEqual(url, result[0]['url'])
        self.assertEqual(title, result[0]['title'])

    @mock.patch('requests.get')
    def test_extract_data_from_page_failed(self, method):
        with open('tests/data/pankreator_incorrect.html') as html:
            m = MockedRequest()
            m.text = html.read()
            method.return_value = m
        downloader = self.get_downloader()
        result = downloader.extract_data_from_page()
        self.assertEqual([], result)

    @mock.patch('requests.get')
    @mock.patch('sqlite3.connect')
    def test_check_new_posts_empty_html(self, connect, get):
        downloader = self.get_downloader()
        m = MockedRequest()
        m.text = ''
        get.return_value = m
        connect.side_effect = sqlite3.connect('tests/data/test_db.db')
        result1, result2 = downloader.check_new_posts()
        self.assertEqual((None, None), (result1, result2))

    @mock.patch('gif_downloader.GifDownloader.download_image')
    @mock.patch('gif_downloader.GifDownloader.extract_data_from_page')
    @mock.patch('sqlite3.connect')
    def test_check_new_posts_existing_record(self, m_connect, m_extract, m_download):
        m_extract.return_value = [{'title': 'mocked', 'gif_url': 'http://mocked.com/gif.gif'}]
        m_download.return_value = 'gif'
        downloader = self.get_downloader()
        cursor = self.connection.cursor()
        cursor.execute('insert into pankreator_gifs (id, gif_url) values (1, "http://mocked.com/gif.gif")')
        cursor.execute('insert into pankreator_gifs (id, gif_url) values (2, "http://mocked.com/gif2.gif")')
        self.connection.commit()
        m_connect.return_value = self.connection
        result1, result2 = downloader.check_new_posts()
        self.assertEqual((None, None), (result1, result2))

    @mock.patch('gif_downloader.GifDownloader.download_image')
    @mock.patch('gif_downloader.GifDownloader.extract_data_from_page')
    @mock.patch('utils.db_connection')
    def test_check_new_posts_new_record(self, m_connect, m_extract, m_download):
        m_extract.return_value = [{'title': 'mocked', 'gif_url': 'http://mocked.com/gif.gif'}]
        m_download.return_value = 'gif'
        downloader = self.get_downloader()
        m_connect.return_value = self.connection
        result1, result2 = downloader.check_new_posts()
        self.assertEqual('gif', result1)
        self.assertEqual('http://mocked.com/gif.gif', result2['gif_url'])