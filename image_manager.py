# -*- coding: utf-8 -*-

import os
import shutil
import random
import zipfile

import requests
import urllib.request
import urllib.parse
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


class Downloader(object):

    """
    Authorize into the library, save the zip file and extract it.
    """

    def __init__(self, content_id, config):
        self.content_id = str(content_id)
        self.config = config

    def unzip(self):
        with zipfile.ZipFile(self.config['files']['zipfile'], 'r') as zip_file:
            zip_file.extractall(self.config['files']['zipdir'])

    def get_filename(self):
        """
        In order to get the name of the file, we attempt to download it.
        This name will used later to find the file in the zip bundle.
        """
        response = urllib.request.urlopen(self.config['default']['content_url'] + self.content_id)
        return response.url.split('/')[-1]

    def get_file(self):
        """
        Download the whole zip of the publication.
        """

        jar = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        opener.addheaders = [('User-agent', 'LibraryMiner')]
        urllib.request.install_opener(opener)

        payload = {
            'login': self.config['default']['pbc_login'],
            'password': self.config['default']['pbc_password']
        }

        data = urllib.parse.urlencode(payload)
        d = data.encode('utf-8')
        request = urllib.request.Request(self.config['default']['auth_url'], d)
        response = urllib.request.urlopen(request, timeout=60)
        response2 = urllib.request.urlretrieve(self.config['default']['content_url'] + self.content_id + '/zip/',
                                               self.config['files']['zipfile'])
        self.unzip()

    def get_thumbnail(self):
        """
        Last resort: just take the thumbnail.
        """

        print("Getting the thumbnail...")
        url = "%s%s" % (self.config['default']['thumbnail_url'], self.content_id)
        urllib.request.urlretrieve(url, self.config['files']['jpg_path'])
        return self.config['files']['jpg_path']

    def cleanup(self):

        def del_files(directory):
            [os.remove(os.path.join(directory, f)) for f in os.listdir(directory)]

        try:
            os.remove(self.config['files']['zipfile'])
            del_files(self.config['files']['zipdir'])
            del_files(self.config['files']['imagesdir'])
        except Exception as e:
            print(e)