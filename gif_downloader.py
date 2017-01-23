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

    def __init__(self, logger, config):
        self.logger = logger
        self.config = config

    def extract_data_from_page(self):
        """
        Parse the site html.
        #TODO: this should be replaced with API call when site supports it.
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

    def check_new_posts(self):
        """
        Something that was found on the site, but wasn't added to the db yet.
        """
        results = self.extract_data_from_page()
        if not results:
            return None, None
        with db_connection() as cursor:
            for result in results:
                cursor.execute('select * from pankreator_gifs where gif_url=?', (result['gif_url'], ))
                db_result = cursor.fetchall()
                if not db_result:
                    self.logger.info('Something new! %s' % result['title'])
                    return self.download_image(result['gif_url']), result
        return None, None
