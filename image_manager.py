import random

import urllib.parse
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


class ImageDownloader(object):

    def __init__(self, config):
        self.url = config['default']['url']
        self.image_path = config['image']['image_path']
        self.metadata_url_part = config['default']['metadata_url']
        self.thumbnail_url = config['default']['thumbnail_url']
        self.jpg_path = config['image']['jpg_path']

    def get_images_list(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links_list = soup.find_all('a')
        image_list = []
        for link in links_list:
            href = link.get('href')
            if "edition" in href:
                image_list.append(href)
        return image_list

    @staticmethod
    def prepare_download_url(edition_url):
        # convert url from dlibra/editions-content?id=[id] to /Content/[id]
        parsed_url = urllib.parse.urlparse(edition_url)
        attrs = urllib.parse.parse_qs(parsed_url.query)
        content_id = attrs.get('id')[0]
        new_path = '/Content/' + content_id + "/"
        new_url = urllib.parse.ParseResult(scheme=parsed_url.scheme,
                                           netloc=parsed_url.netloc,
                                           path=new_path,
                                           params='',
                                           query='',
                                           fragment='')
        return urllib.parse.urlunparse(new_url), content_id

    def get_random_image(self):
        image_list = self.get_images_list()
        image_index = random.randrange(0, len(image_list))
        url, content_id = self.prepare_download_url(image_list[image_index])

        print("Downloading from url", url)
        urllib.request.urlretrieve(url, self.image_path)
        return self.image_path, content_id

    def get_image_metadata(self, image_index):
        url = self.metadata_url_part + str(image_index)
        response = requests.get(url)
        root = ET.fromstring(response.text)
        image_metadata = {}
        for child in root[0]:
            if 'title' in child.tag:
                image_metadata['title'] = child.text
        return image_metadata

    def get_thumbnail(self, content_id):
        print("Getting the thumbnail...")
        url = "%s%s" % (self.thumbnail_url, content_id)
        print(url)
        urllib.request.urlretrieve(url, self.jpg_path)
        return self.jpg_path

    def pretty_print_image_metadata(self, content_id):
        image_metadata = self.get_image_metadata(content_id)
        return image_metadata['title'][:140]
