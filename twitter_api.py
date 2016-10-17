# -*- coding: utf-8 -*-

import tweepy


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
