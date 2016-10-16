import configparser
import tweepy

from oai_api import LibraryCrawler
from converter import Converter
from image_manager import Downloader
from redirect import unittest, RedirectTest


class TwitterPoster(object):

    def __init__(self, config):
        self.consumer_key = config['twitter']['consumer_key']
        self.consumer_secret = config['twitter']['consumer_secret']
        self.access_token = config['twitter']['access_token']
        self.access_token_secret = config['twitter']['access_token_secret']
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)

    def put_media_to_timeline(self, img_path, status):
        self.api.update_with_media(img_path, status)


def main():
    config = configparser.ConfigParser()
    config.read('config.conf')

    api = LibraryCrawler(config)
    record = api.run()

    content_id = 24617

    if record:
        downloader = Downloader(content_id, config)
        downloader.get_file()
        downloader.unzip()

        converter = Converter(config)
        error = converter.convert()
        if error:
            # Try to get the thumbnail.
            print(error)
            media_file = downloader.get_thumbnail(file_index)

    #twitter_poster = TwitterPoster(config)
    #twitter_poster.put_media_to_timeline(media_file, metadata + ' http://pbc.gda.pl/dlibra/docmetadata?id=' + str(file_index))


if __name__ == "__main__":
    main()
