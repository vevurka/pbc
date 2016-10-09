import configparser
import tweepy

from converter import Converter
from image_manager import ImageDownloader

IMG_DIR = "images/" # TODO: add to config?


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
    image, index = image_downloader.get_random_image()
    print(index)
    image_downloader.get_image_metadata(index)

    #twitter_poster = TwitterPoster(config)
    #twitter_poster.put_media_to_timeline(image)

    # jpg_path = os.path.join(IMG_DIR, "new_image.jpg")
    # image_downloader = ImageDownloader()
    # djvu_file = image_downloader.get_random_image()
    # converter = Converter(djvu_file, jpg_path)
    # converter.convert()


if __name__ == "__main__":
    main()
