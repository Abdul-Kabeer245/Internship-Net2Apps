from selenium import webdriver
from SeleniumHelperUtils import HelperMethod

class CountryScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)
        self.helperMethod = HelperMethod(self.driver)
    def extract_data(self):
        self.helperMethod.clickElement(  '(//h3[@class="page-title"])[1]/a', 'XPATH')
        data = []
        countries = self.helperMethod.getElements('//div[@class= "col-md-4 country"]', 'XPATH')
        for i in range(1,len(countries)+1):
            country_name = self.helperMethod.getElementText( f'(//h3[@class="country-name"])[{i}]', 'XPATH')
            capital = self.helperMethod.getElementText( f'(//span[@class="country-capital"])[{i}]', 'XPATH')
            population = self.helperMethod.getElementText( f'(//span[@class="country-population"])[{i}]', 'XPATH')
            area = self.helperMethod.getElementText(f'(//span[@class="country-area"])[{i}]', 'XPATH')
            data.append({
                 'Country': country_name,
                 'Capital': capital,
                 'Population': population,
                 'Area': area
            })
        return data

    def run(self):
        self.driver.get('https://www.scrapethissite.com/pages/')
        data = self.extract_data()
        self.driver.quit()
        self.helperMethod.saveData(data, 'Task 1', 'csv')

scraper = CountryScraper()
scraper.run()