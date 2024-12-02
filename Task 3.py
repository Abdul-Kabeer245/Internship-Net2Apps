from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from SeleniumHelperUtils import HelperMethod

class JacketScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)
        self.actions = ActionChains(self.driver)
        self.helperMethod = HelperMethod(self.driver)


    def navigator(self):
        # Hovering over men's menu
        men_menu = self.helperMethod.getElement('//li[@class= "level0 nav-3 category-item level-top parent ui-menu-item"]', 'XPATH')
        self.actions.move_to_element(men_menu).perform()

        # Hovering over tops menu
        tops_menu = self.helperMethod.getElement('//li[contains(@class, "level1 nav-3-1")]', 'XPATH')
        self.actions.move_to_element(tops_menu).perform()

        # Clicking Jacket
        self.helperMethod.clickElement('//li[contains(@class, "nav-3-1-1")]', 'XPATH')

    def filter(self):
        # Clicking size dropdown
        self.helperMethod.clickElement('(//div[@class="filter-options-title"])[2]', 'XPATH')

        # Clicking XS size
        self.helperMethod.clickElement('(//div[@class="swatch-option text "])[1]', 'XPATH')

        # Clicking on color dropdown
        self.helperMethod.clickElement('(//div[@class="filter-options-title"])[3]', 'XPATH')

        # Clicking on green color
        self.helperMethod.clickElement('(//a[@aria-label="Green"])/div', 'XPATH')

        # Clicking Material filter
        self.helperMethod.clickElement('(//div[@class="filter-options-title"])[5]','XPATH')

        # Clicking Nylon material
        self.helperMethod.clickElement('Nylon', 'partial_LINK_TEXT')

    def get_data(self):
        data = []
        item_number = self.helperMethod.getElements('//li[@class="item product product-item"]', 'XPATH')

        for i in range(1, len(item_number) + 1):
            data.append({
                'Product Name': self.helperMethod.getElementText(f'(//strong[@class="product name product-item-name"])[{i}]', 'XPATH'),
                'Price': float(self.helperMethod.getElementText(f'(//span[@class="price"])[{i}]', 'XPATH').replace('$', '')) * 280,
                'Size': 'XS',
                'Color': 'Green'
            })
        return data


    def run(self):
        # Open the target URL
        self.driver.get('https://magento.softwaretestingboard.com/')
        # Navigate and filter items
        self.navigator()
        self.filter()
        # Get data
        data = self.get_data()
        # Close the WebDriver
        self.driver.quit()
        # save data
        self.helperMethod.saveData(data,'Task 3', 'xlsx')

# Run the scraper
scraper = JacketScraper()
scraper.run()
