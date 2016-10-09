import random

import urllib.parse

import requests
from bs4 import BeautifulSoup


class ImageDownloader(object):
    def __init__(self):
        self.url = "http://pbc.gda.pl/dlibra/publication?id=29939"  # TODO: add to config

    def get_images_list(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links_list = soup.find_all('a')
        image_list = []
        for link in links_list:
            href = link.get('href')
            if "edition" in href:
                image_list.append(href)
        return image_list

    @staticmethod
    def prepare_download_url(edition_url):
        # convert url from dlibra/editions-content?id=[id] to /Content/[id]
        parsed_url = urllib.parse.urlparse(edition_url)
        attrs = urllib.parse.parse_qs(parsed_url.query)
        content_id = attrs.get('id')[0]
        new_path = '/Content/' + content_id + "/"
        new_url = urllib.parse.ParseResult(scheme=parsed_url.scheme,
                                           netloc=parsed_url.netloc,
                                           path=new_path,
                                           params='',
                                           query='',
                                           fragment='')
        return urllib.parse.urlunparse(new_url)

    def get_random_image(self):
        image_list = self.get_images_list()
        image_index = random.randrange(0, len(image_list))
        url = self.prepare_download_url(image_list[image_index])

        print("Downloading from url", url)
        urllib.request.urlretrieve(url, '~/PANkreator/temp.djvu')  # TODO: add to config


def main():
    image_downloader = ImageDownloader()
    image_downloader.get_random_image()


if __name__ == "__main__":
    main()
