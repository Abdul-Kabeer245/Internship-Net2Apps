import os, time
from selenium import webdriver
from SeleniumHelperUtils import HelperMethod
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException



class CatalogScraper:
    def __init__(self):
        self.download_folder = r'D:\Net2Apps\Catalog_files'
        self.options = Options()
        chrome_prefs = {
            "download.default_directory": self.download_folder,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        self.options.add_experimental_option('prefs', chrome_prefs)
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(60)
        self.helperMethod = HelperMethod(self.driver)

    def create_folder(self):
        if not os.path.exists(self.download_folder):
            os.mkdir(self.download_folder)
        else:
            print('Directory already exist.')


    def get_data(self):
        searchbox = self.helperMethod.getElement( "searchTextBox", 'id' )
        searchbox.send_keys('windows 11')
        self.helperMethod.clickElement("searchButtonBox", 'ID')
        for i in range(1,11):
            self.helperMethod.clickElement(f'(//input[@value="Download"])[{i}]', 'XPATH')
            self.driver.switch_to.window(self.driver.window_handles[1])
            file_name = self.helperMethod.getElementText("contentTextItemSpacerNoBreakLink", 'class_name')
            self.helperMethod.clickElement('//a[@class="contentTextItemSpacerNoBreakLink"]', 'XPATH')
            print("Downloading", file_name)
            time.sleep(2)
            if self.wait_for_download(file_name):
                print('File successfully downloaded')
            else:
                print('File download failed')
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])


    def wait_for_download(self, file_name):
        start_time = time.time()
        while time.time() - start_time < 600 :
            if not [f for f in os.listdir(self.download_folder) if f.endswith('.crdownload')]:
                return True
            else:
                if not [f for f in os.listdir(self.download_folder) if f != file_name]:
                    return True
                else:
                    time.sleep(3)
        return False

    def take_screenshot(self):
        self.helperMethod.scrollToViewElement("tableContainer", 'ID')
        screenshot_path = os.path.join(self.download_folder,'screenshot.png')
        screenshot_data = self.driver.get_screenshot_as_png()
        with open(screenshot_path, 'wb') as file:
            file.write(screenshot_data)


    def run(self):
        # Creating folder
        self.create_folder()
        # Open the target URL
        self.driver.get('https://www.catalog.update.microsoft.com/Home.aspx')
        # Downloading files
        self.driver.maximize_window()
        self.get_data()
        self.take_screenshot()
        self.driver.quit()


scraper = CatalogScraper()
scraper.run()