# -*- coding: utf-8 -*-

from datetime import date
from freezegun import freeze_time
import os
import sqlite3
import unittest
from unittest import mock

from pga import PANkreator


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
    def get_pan(self, mock_logger):
        return PANkreator()

    @mock.patch('pga.PANkreator.get_gif')
    def test_choose_content_gif(self, m_get_gif):
        m_get_gif.return_value = 'gif', {'title': 'mocked title', 'url': 'mocked url',
                                         'gif_url': 'mocked gif url'}
        pan = self.get_pan()
        pan.db = 'tests/data/test_db.db'

        media_file_path, title = pan.choose_content()
        self.assertEqual('gif', media_file_path)

    @freeze_time('2017-02-01')
    @mock.patch('pga.PANkreator.get_gif')
    def test_choose_content_gif_was_not_yesterday(self, m_get_gif):
        m_get_gif.return_value = 'gif', {'title': 'mocked title', 'url': 'mocked url',
                                         'gif_url': 'mocked gif url'}
        self.connection.cursor().execute(
            'insert into pankreator_gifs (title, url, gif_url, date_added) values (?, ?, ?, ?) ',
            ('something', 'url', 'gif url', date(2017, 1, 30)))
        self.connection.commit()
        pan = self.get_pan()
        pan.db = 'tests/data/test_db.db'
        media_file_path, title = pan.choose_content()
        self.assertEqual('gif', media_file_path)

    @freeze_time('2017-02-01')
    @mock.patch('pga.PANkreator.get_gif')
    @mock.patch('pga.PANkreator.get_djvu')
    def test_choose_content_gif_was_added_yesterday(self, m_get_djvu, m_get_gif):
        m_get_gif.return_value = 'gif', {'title': 'mocked title', 'url': 'mocked url',
                                         'gif_url': 'mocked gif url'}
        m_get_djvu.return_value = 'djvu', 'djvu'
        self.connection.cursor().execute(
            'insert into pankreator_gifs (title, url, gif_url, date_added) values (?, ?, ?, ?) ',
            ('something', 'url', 'gif url', date(2017, 1, 31)))
        self.connection.commit()
        pan = self.get_pan()
        pan.db = 'tests/data/test_db.db'
        media_file_path, title = pan.choose_content()
        self.assertEqual('djvu', media_file_path)