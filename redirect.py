# -*- coding: utf-8 -*-


from selenium import webdriver
import unittest, time

from urllib.parse import urlparse, parse_qs


class RedirectTest(unittest.TestCase):

    """
    All this dirty selenium hacking is for the sole purpose of
    getting the pbc library api working. Since data was exposed only
    through ajax requests, it was necessary to mock the user behavior.
    SHAME SHAME SHAME :D.
    """
    image_index = "0"

    def setUp(self):
        self.driver = webdriver.PhantomJS('../phantomjs')  #webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://pbc.gda.pl/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_proba3(self):
        driver = self.driver
        driver.get(self.base_url + "/dlibra/publication?id=29939")
        
        number = "%s" % (int(self.image_index) + 4)
        
        driver.find_element_by_xpath("(//img[contains(@src,'http://pbc.gda.pl/style/common/img/icons/desc.gif')])[%s]" % number).click()
        time.sleep(1)
        print(driver.current_url)
        content_id = parse_qs(urlparse(driver.current_url).query)['id'][0]
        with open('content_id.txt', 'w+') as content_id_file:
            content_id_file.write(content_id)

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
