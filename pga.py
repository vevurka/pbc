# -*- coding: utf-8 -*-

from datetime import date
from dateutil.relativedelta import relativedelta
import configparser
import logging
import traceback

from analyzer import ImageAnalyzer
from downloader import Downloader
from gif_downloader import GifDownloader
from oai_api import LibraryCrawler
from twitter_api import TwitterPoster
from utils import db_connection, cleanup

QUERY = {
    'type': [
        'gazeta', 'stary druk', 'fotografia', 'fotografie', 'album',
        'dokument ikonograficzny', 'dokument ikonograficzny', 'inkunabuł',
        'kalendarz', 'karta pocztowa', 'mapa', 'obraz', 'pocztówka', 'rękopis',
        'rysunek', 'ulotka', 'druk ulotny',
    ]
}


class PANkreator(object):

    """
    Main body of the PANkreator bot.
    """

    dry_run = True

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config/config.conf')
        self.db = 'config/database.db'
        logging.basicConfig(filename='pankreator_app.log',
                            format='%(asctime)-15s %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger('PANkreator')
        self.logger.info('Starting...')

    def get_gif(self):
        gif_downloader = GifDownloader(self.logger, self.config, self.db)
        return gif_downloader.check_new_posts()

    def get_djvu(self, just_thumbnail=False):
        record, content_id = LibraryCrawler(self.logger, self.config, QUERY).run()
        if record:
            downloader = Downloader(self.logger, content_id, self.config)
            downloader.get_file()
            downloader.unzip()

            if just_thumbnail:
                media_file_path = downloader.get_thumbnail()
            else:
                analyzer = ImageAnalyzer(self.logger, self.config)
                media_file_path = analyzer.run()

            title = record.metadata['title'][0]
            title = title[:110] + self.config['default']['metadata_url'] + content_id
            return media_file_path, title
        return None, None

    def choose_content(self):
        """
        This can be either
        - gif from pankreator.org site
        or
        - djvu image from the PAN library.
        """

        with db_connection(self.db) as cursor:
            cursor.execute('select * from pankreator_gifs order by id desc limit 1;')
            last_record = cursor.fetchone()

            # If gif wasn't added yesterday, add one.
            yesterday = date.today() - relativedelta(days=+1)
            if (not last_record) or (last_record[4] < yesterday):
                media_file_path, result = self.get_gif()
                if media_file_path and result:
                    query = 'insert into pankreator_gifs (title, url, gif_url, date_added)'\
                            'values (?, ?, ?, ?)'
                    cursor.execute(query, (result['title'], result['url'], result['gif_url'], date.today()))
                    return media_file_path, result['title'] + ' ' + result['url']

            media_file_path, title = self.get_djvu()

        return media_file_path, title

    def main(self, tries=0):

        try:
            media_file_path, title = self.choose_content()

            if not media_file_path:
                tries -= 1
                if tries > 0:
                    self.logger.warning("Trying again...")
                    self.main(tries=tries)

                # Try to get the thumbnail.
                media_file_path, title = self.get_djvu(just_thumbnail=True)

            self.logger.info("The winner is... %s, %s" % (media_file_path, title))

            if not self.dry_run:
                twitter_poster = TwitterPoster(self.config)
                twitter_poster.put_media_to_timeline(
                    media_file_path,
                    title
                )
                cleanup(self.logger, self.config)

        except Exception as e:
            self.logger.error("Caught exception: %s" % e)
            traceback.print_exc()
            self.logger.warning("Trying again...")
            cleanup(self.logger, self.config)
            tries -= 1
            if tries > 0:
                self.main(tries=tries)


if __name__ == '__main__':
    pankreator = PANkreator()
    pankreator.main(tries=3)
