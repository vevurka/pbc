# -*- coding: utf-8 -*-


import configparser

from oai_api import LibraryCrawler
from twitter_api import TwitterPoster
from image_manager import Downloader, cleanup
from analyzer import ImageAnalyzer

QUERY = {
    'type': ['stary druk', 'fotografia', 'album', 'druk ulotny',
             'dokument ikonograficzny', 'dokument ikonograficzny',]
}


def main(config, tries):

    try:
        api = LibraryCrawler(config, QUERY)
        record = api.run()
        content_id = record.metadata['identifier'][1].lstrip('oai:pbc.gda.pl:')

        if record:
            downloader = Downloader(content_id, config)
            downloader.get_file()
            downloader.unzip()

            analyzer = ImageAnalyzer(config)
            media_file_path = analyzer.run()

            if not media_file_path:
                tries -= 1
                if tries > 0:
                    print("Trying again...")
                    main(config, tries)
                # Try to get the thumbnail.
                media_file_path = downloader.get_thumbnail()

            print("The winner is... %s" % media_file_path)

            twitter_poster = TwitterPoster(config)
            title = record.metadata['title'][0]
            twitter_poster.put_media_to_timeline(media_file_path, title[:110] + ' http://pbc.gda.pl/dlibra/docmetadata?id=' + content_id)
            cleanup(config)

    except Exception as e:
        print("Caught exception: %s" % e)
        print("Trying again...")
        cleanup(config)
        tries -= 1
        if tries > 0:
            main(config, tries)


config = configparser.ConfigParser()
config.read('config.conf')

main(config, 3)
