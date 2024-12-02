from selenium import webdriver
from loginhelper import SAP


class ScrubID:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)
        self.driver.get('https://hcm41preview.sapsf.com/')

    def get_scrub_id(self):
        loginHelper = SAP(self.driver)
        loginHelper.login()
        url = self.driver.current_url
        print(url[url.find("_s.crb="):])

id = ScrubID()
id.get_scrub_id()