# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from urllib.request import urlretrieve

from utils import db_connection


class GifDownloader(object):

    """
    Downloads latest gif from the pankreator.org site.
    """

    def __init__(self, logger, config, db):
        self.logger = logger
        self.config = config
        self.db = 'config/database.db'

    def extract_data_from_page(self):
        """
        Parse the site html.
        # TODO: this should be replaced with API call when site supports it.
        """
        results = []
        r = requests.get(self.config['default']['pankreator_site'])
        soup = BeautifulSoup(r.text, 'lxml')
        posts = [a for a in soup.findAll('div', attrs={'class': 'span2'})]
        for p in posts:
            post = {}
            figcaption = p.find('figcaption', {'class': 'gify'})
            figure = p.find('div', {'class': 'item-image'})
            post['title'] = figcaption.a.getText().replace('\t', '').replace('\n', '')
            post['gif_url'] = urljoin(self.config['default']['pankreator_site'],
                                      figure.a.img['src'])
            post['url'] = urljoin(self.config['default']['pankreator_site'],
                                  figure.a['href'])
            results.append(post)
        return results

    def download_image(self, url):
        urlretrieve(url, self.config['files']['gif_path'])
        return self.config['files']['gif_path']

    @staticmethod
    def compare_results(db_results, web_results):
        web_gifs = [w['gif_url'] for w in web_results]
        db_gifs = [d[3] for d in db_results if d]
        return set(web_gifs) - set(db_gifs)

    def check_new_posts(self):
        """
        Something that was found on the site, but wasn't added to the db yet.
        """
        results = self.extract_data_from_page()
        if not results:
            return None, None
        with db_connection(self.db) as cursor:
            cursor.execute('select * from pankreator_gifs order by id asc')

            differences = self.compare_results(cursor.fetchall(), results)

            if differences:
                for item in results:
                    if item['gif_url'] in differences:
                        new_item = item
                        self.logger.info('Something new! %s' % new_item['title'])
                        return self.download_image(new_item['gif_url']), new_item
        return None, None
