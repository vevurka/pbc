# -*- coding: utf-8 -*-


import configparser

from oai_api import LibraryCrawler
from twitter_api import TwitterPoster
from converter import Converter
from image_manager import Downloader
from redirect import unittest, RedirectTest


def main():
    config = configparser.ConfigParser()
    config.read('config.conf')

    api = LibraryCrawler(config)
    record = api.run()
    content_id = record.metadata['identifier'][1].lstrip('oai:pbc.gda.pl:')

    if record:
        downloader = Downloader(content_id, config)
        downloader.get_file()
        downloader.unzip
        filename = downloader.get_filename()

        converter = Converter(config, filename)
        error = converter.convert()
        if error:
            # Try to get the thumbnail.
            media_file = downloader.get_thumbnail()

        #twitter_poster = TwitterPoster(config)
        #twitter_poster.put_media_to_timeline(media_file, metadata + ' http://pbc.gda.pl/dlibra/docmetadata?id=' + str(file_index))
        downloader.cleanup()


if __name__ == "__main__":
    main()
