import random

import urllib.parse
import requests
from bs4 import BeautifulSoup

import configparser
import tweepy

from converter import Converter

IMG_DIR = "images/" # TODO: add to config?


class ImageDownloader(object):
    def __init__(self, config):
        self.url = config['default']['url']
        self.image_path = config['image']['image_path']

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
        return self.image_path

    def get_image_metadata(self, image_index):
        # http://pbc.gda.pl/dlibra/docmetadata?id=30530&from=publication
        pass


class TwitterPoster(object):

    def __init__(self, config):
        self.consumer_key = config['twitter']['consumer_key']
        self.consumer_secret = config['twitter']['consumer_secret']
        self.access_token = config['twitter']['access_token']
        self.access_token_secret = config['twitter']['access_token_secret']
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)

    def put_media_to_timeline(self, img_path): # TODO: status text
        self.api.update_with_media(img_path, "Mój pierwszy obrazek")


def main():
    config = configparser.ConfigParser()
    config.read('config.conf')
    image_downloader = ImageDownloader(config)
    image = image_downloader.get_random_image()
    print(image)

    #twitter_poster = TwitterPoster(config)
    #twitter_poster.put_media_to_timeline(image)

    # jpg_path = os.path.join(IMG_DIR, "new_image.jpg")
    # image_downloader = ImageDownloader()
    # djvu_file = image_downloader.get_random_image()
    # converter = Converter(djvu_file, jpg_path)
    # converter.convert()


if __name__ == "__main__":
    main()
