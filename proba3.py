# -*- coding: utf-8 -*-


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

from urllib.parse import urlparse, parse_qs


class RedirectTest(unittest.TestCase):

    """
    All this dirty selenium hacking is for the sole purpose of
    getting the 
    """
    content_id = "0"

    def setUp(self):
        self.driver = webdriver.PhantomJS('/home/sir/Aktywatory/PANkreator_src/phantomjs')  #webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://pbc.gda.pl/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_proba3(self):
        driver = self.driver
        driver.get(self.base_url + "/dlibra/publication?id=29939")
        
        number = "%s" % (int(self.content_id) + 4)
        
        driver.find_element_by_xpath("(//img[contains(@src,'http://pbc.gda.pl/style/common/img/icons/desc.gif')])[%s]" % number).click()
        time.sleep(1)
        print(driver.current_url)
        content_id = parse_qs(urlparse(driver.current_url).query)['id'][0]
        with open('content_id.txt', 'w') as content_id_file:
            content_id_file.write(content_id)

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

#if __name__ == '__main__':
#    unittest.main()