import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from SeleniumHelperUtils import HelperMethod

class MobileScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)
        self.helperMethod = HelperMethod(self.driver)

    def navigator(self):
        action = ActionChains(self.driver)
        # Clicking on shop menu
        self.helperMethod.clickElement('(//li[@class="style-module_rootMenuItem__RK6kc"])[1]', 'XPATH')

        # Clicking on cell phones and accessories
        self.helperMethod.clickElement('(//a[@title="Cell Phones and Accessories"])', 'XPATH')

        #Clicking unlocked phones
        self.helperMethod.clickElement('(//a[@title="Unlocked Phones"])', 'XPATH')

        # Clicking on unlocked samsung smartphones
        self.helperMethod.clickElement('(//a[@title="Unlocked Samsung Smartphones"])', 'XPATH')

        # Locate product condition
        product_condition = self.helperMethod.getElement('(//button[@data-automation="expandable-button"])[5]', 'XPATH')
        # Scroll the element into view
        self.helperMethod.scrollToViewElement('(//button[@data-automation="expandable-button"])[5]', 'XPATH')

        # Wait for the element to be clickable
        action.move_to_element(product_condition).click().perform()

        # Clicking brand-new check box
        brand_new = self.helperMethod.getElement('(//label[@for="facetFilter-ProductCondition_BrandNew"])[2]', 'XPATH')
        action.move_to_element(brand_new).click().perform()


    def show_more(self):
        time.sleep(2)
        number = int(self.helperMethod.getElementText('//div[@data-testid="PRODUCT_LIST_RESULT_COUNT_DATA_AUTOMATION"]', 'XPATH').split()[0])
        item = len(self.helperMethod.getElements('(//ul[@class="list_3khgt"])/div/div', 'XPATH'))
        for i in range(number//item):
            if len(self.helperMethod.getElements('(//ul[@class="list_3khgt"])/div/div', 'XPATH')) < number:
                self.helperMethod.scrollToViewElement('//button[contains(@class,"loadMore_3AoXT")]', 'XPATH')
                time.sleep(2)
                self.helperMethod.clickElement('//button[contains(@class,"loadMore_3AoXT")]', 'XPATH')
            else:
                break


    def get_data(self):
        item_numbers = int(self.helperMethod.getElementText('(//div[@data-testid="PRODUCT_LIST_RESULT_COUNT_DATA_AUTOMATION"])', 'XPATH').split()[0])
        data = []
        for i in range(1,item_numbers+1):
            print(f"item number {i}")
            name = self.helperMethod.getElementText(f'(//div[@class="productItemName_3IZ3c"])[{i}]', 'XPATH')
            link = self.helperMethod.getElementAttributeText(f'(//ul[@class="list_3khgt"])/div/div[{i}]/div/a','XPATH', 'href')
            price = self.helperMethod.getElementText(f'(//span[@class="style-module_screenReaderOnly__4QmbS style-module_large__g5jIz"])[{i}]', 'XPATH').replace('$', '')
            data.append(
                {'Mobile Name': name,
                 'Link': link,
                 'Price':price
                 }
            )
        return data


    def run(self):
        # open the target url
        self.driver.get('https://www.bestbuy.ca/en-ca')
        # Navigate to smartphone page
        self.navigator()
        # Scroll to load all smartphone
        self.show_more()
        # Extracting data
        data = self.get_data()
        # Close the Webdriver
        self.driver.quit()
        # Saving data
        self.helperMethod.saveData(data, 'Task 5', 'csv')


# Run the Scraper
scraper = MobileScraper()
scraper.run()