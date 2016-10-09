import random

import urllib.parse
import requests
from bs4 import BeautifulSoup


class ImageDownloader(object):

    def __init__(self, config):
        self.url = config['default']['url']
        self.image_path = config['image']['image_path']
        self.metadata_url_part = config['default']['metadata_url']
        self.thumbnail_url = config['default']['thumbnail_url']

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
        return urllib.parse.urlunparse(new_url)

    def get_random_image(self):
        image_list = self.get_images_list()
        image_index = random.randrange(0, len(image_list))
        url = self.prepare_download_url(image_list[image_index])

        print("Downloading from url", url)
        urllib.request.urlretrieve(url, self.image_path)
        return (self.image_path, image_index)

    def get_image_metadata(self, image_index):
        url = self.metadata_url_part + str(image_index)
        print(url)
        response = requests.get(url)
        print(response.text)

    def get_thumbnail(self):
        url = self.thumbnail_url
        urllib.request.urlretrieve(self.thumbnail_url, self.image_path)
