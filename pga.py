import configparser
import tweepy

from converter import Converter
from image_manager import ImageDownloader


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

    djvu_file, content_id = image_downloader.get_random_image()
    image_downloader.get_image_metadata(content_id)

    converter = Converter(config)
    error = converter.convert()
    if error:
        # Try to get the thumbnail.
        image_downloader.get_thumbnail(content_id)


if __name__ == "__main__":
    main()
