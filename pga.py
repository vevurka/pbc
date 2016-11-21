# -*- coding: utf-8 -*-


import configparser

from oai_api import LibraryCrawler
from twitter_api import TwitterPoster
from converter import Converter
from image_manager import Downloader, cleanup
from redirect import unittest, RedirectTest


def main(config, tries):

    try:
        api = LibraryCrawler(config)
        record = api.run()
        content_id = record.metadata['identifier'][1].lstrip('oai:pbc.gda.pl:')

        if record:
            downloader = Downloader(content_id, config)
            downloader.get_file()
            downloader.unzip()
            filename = downloader.get_filename()

            converter = Converter(config, filename)
            media_file = converter.convert()
            if not media_file:
                # Try to get the thumbnail.
                media_file = downloader.get_thumbnail()

            print(media_file)
            twitter_poster = TwitterPoster(config)
            title = record.metadata['title'][0]
            #twitter_poster.put_media_to_timeline(media_file, title[:110] + ' http://pbc.gda.pl/dlibra/docmetadata?id=' + content_id)
            #cleanup(config)

    except Exception as e:
        print("Caught exception: %s" % e)
        print("Trying again...")
        cleanup(config)
        tries -= 1
        if tries > 0:
            main(config, tries)


config = configparser.ConfigParser()
config.read('config.conf')

main(config, 5)
