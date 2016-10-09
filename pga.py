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

    def put_media_to_timeline(self, img_path, status):
        self.api.update_with_media(img_path, status)


def main():

    config = configparser.ConfigParser()
    config.read('config.conf')

    image_downloader = ImageDownloader(config)

    media_file, file_index = image_downloader.get_random_image()
    metadata = image_downloader.pretty_print_image_metadata(file_index)

    converter = Converter(config)
    error = converter.convert()
    if error:
        # Try to get the thumbnail.
        print(error)
        media_file = image_downloader.get_thumbnail(file_index)

    print(metadata)
    twitter_poster = TwitterPoster(config)
    twitter_poster.put_media_to_timeline(media_file, metadata)


if __name__ == "__main__":
    main()
