from SeleniumHelperUtils import HelperMethod
from models import Model_RatingScale
from controllers import Controller_RatingScale
import time

class RatingScaleScraper:
    def __init__(self, driver):
        self.driver = driver
        self.helperMethod = HelperMethod(self.driver)
        self.controller = Controller_RatingScale()

    def navigate_rating_scales(self):
        data = []
        name_list = self.helperMethod.getElements('(//span[contains(@title, "Name of the rating")]//a)', 'xpath')
        for i in range(1, len(name_list)+1):
            self.helperMethod.clickElement(f'(//span[contains(@title, "Name of the rating")]//a)[{i}]','XPATH')
            if self.helperMethod.isElementPresent('//button[@data-help-id="okButton"]', 'xpath'):
                self.helperMethod.clickElement('//button[@name = "OK"]', 'xpath')
            item_data = self.extract_data()
            data.extend(item_data)
            self.helperMethod.clickElement('//a[text() = "Rating Scale Designer"]', 'xpath')
        return data

    def extract_data(self):
        data = []
        name = self.helperMethod.getElementAttributeText('//input[@data-testid = "sfTextField"]', 'xpath', 'value')
        rating_desc = self.helperMethod.getElementAttributeText('//span[@class="ratingScaleTextArea"]/textarea', 'xpath', 'value')
        scales = len(self.helperMethod.getElements('(//table[contains(@class,  "inner-table")])[5]//tr', 'xpath'))
        for row in range(1, scales):
            item_number = "=ROW()-1"
            score = self.helperMethod.getElementAttributeText(
                f'//tr[contains(@class,"fd-table__row--compact")][{row}]//td[1]//input', 'xpath', 'value')
            score_label = self.helperMethod.getElementAttributeText(
                f'//tr[contains(@class,"fd-table__row--compact")][{row}]//td[2]//input', 'xpath', 'value')
            score_desc = self.helperMethod.getElementAttributeText(
                f'//tr[contains(@class,"fd-table__row--compact")][{row}]//td[3]//textarea', 'xpath', 'value')
            row_data = Model_RatingScale()
            row_data.itemId = item_number
            row_data.name = name or ""
            row_data.desc = rating_desc or ""
            row_data.score = score or ""
            row_data.label = score_label or ""
            row_data.score_desc = score_desc or ""
            data.append(row_data)
        return data

    def parse_data_in_sheet(self, data):
        header = ["ItemId", 'Name', 'Description', "Score", "Label", "Score Description", "", "Rating Scale Name", "Status"]
        unique_name = self.get_unique_name(data)
        self.controller.reset_sheet()
        time.sleep(5)
        self.controller.fill_rating_scale_name(unique_name)
        self.controller.fill_sheet_header(header)
        self.controller.fill_sheet_data(data)


    # Function to find all the unique name of rating scale from list of objects
    def get_unique_name(self, data):
        unseen_data = set()
        unique_name = []
        for d in data:
            if d.name not in unseen_data:
                unseen_data.add(d.name)
                unique_name.append([d.name])
        return unique_name

    def run(self):
        scraped_data = self.navigate_rating_scales()
        self.parse_data_in_sheet(scraped_data)