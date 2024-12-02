from selenium import webdriver
from SeleniumHelperUtils import HelperMethod


class HockeyScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)
        self.helperMethod = HelperMethod(self.driver)

    def get_data(self):
        self.helperMethod.clickElement( '(//h3[@class="page-title"])[2]', 'XPATH')
        headers = [header for header in self.helperMethod.getListofElementText( '//table/tbody/tr[1]/th', 'XPATH')]
        data = []
        pages = self.helperMethod.getElements( '//ul[@class="pagination"]/li', 'XPATH')
        for i in range(1, len(pages)):
            self.helperMethod.clickElement('//a[@aria-label="Next"]', 'XPATH')
            self.helperMethod.waitforElementTobeVisible( '//table', 'XPATH')
            teams = self.helperMethod.getElements('//tr[@class="team"]', 'XPATH')
            for team in range(1, len(teams) + 1):
                row = {}
                for cell in range(1, len(headers) + 1):
                    col_name = headers[cell - 1]
                    cell_value = self.helperMethod.getElementText(f'//tr[@class="team"][{team}]/td[{cell}]', 'XPATH')
                    if cell_value:
                        row[col_name] = cell_value
                    else:
                        row[col_name] = 'Not found'
                data.append(row)
        return data


    def run(self):
        self.driver.get('https://www.scrapethissite.com/pages')
        data = self.get_data()
        self.driver.quit()
        self.helperMethod.saveData(data, 'Task 2', 'csv')


scraper = HockeyScraper()
scraper.run()