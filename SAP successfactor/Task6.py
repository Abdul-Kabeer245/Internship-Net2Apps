from controllers import Controller_NominationSetup
from SeleniumHelperUtils import HelperMethod
from models import Model_NominationSetup, Model_NominationSetup_Checkbox
from selenium.webdriver.support.ui import Select

class NominationsSetupScraper:
    def __init__(self, driver):
        self.driver = driver
        self.helperMethod = HelperMethod(self.driver)
        self.controller = Controller_NominationSetup()

    def nomination_scrap(self):
        data = []
        date = self.helperMethod.getElementAttributeText('//input[@class = "calendarTagInput"]', 'xpath', 'value')
        checkboxes_number = self.helperMethod.getListofElementText('//input[@type = "checkbox"]//..', 'xpath')
        checkboxes = []
        for i in range(1, len(checkboxes_number)+1):
            obj = Model_NominationSetup_Checkbox()
            obj.label = self.helperMethod.getElementText(f'(//input[@type = "checkbox"]//..)[{i}]', 'xpath')
            if self.helperMethod.getElementAttributeText(f'(//input[@type = "checkbox"])[{i}]', 'xpath', 'checked'):
                obj.value = True
            else:
                obj.value = False
            checkboxes.append(obj)
        all_options = self.helperMethod.getListofElementText(f'(//table[@type = "form"]//table//tr)[2]/td[4]//option', 'xpath')
        nominations = self.helperMethod.getElements('//table[@type = "form"]//table//tr', 'xpath')
        for i in range(2, len(nominations)+1):
            name = self.helperMethod.getElementText(f'(//table[@type = "form"]//table//tr)[{i}]/td[2]', 'xpath')
            select = Select(self.helperMethod.getElement(f'(//table[@type = "form"]//table//tr)[{i}]/td[4]/select', 'xpath'))
            option = select.first_selected_option
            row_data = Model_NominationSetup()
            row_data.itemId = "=Row()-1"
            row_data.name = name
            row_data.selected_option = option.text
            data.append(row_data)
        return data, date, all_options, checkboxes

    def parse_data_in_sheet(self, data,date, all_options, checkboxes):
        header = ['ItemId',	'Name',	'Form Template', '', 'Checkbox Label', 'Checkbox Value', 'History Date']
        self.controller.reset_sheet()
        self.controller.fill_sheet_header(header)
        self.controller.fill_history_date(date)
        self.controller.fill_checkboxes_data(checkboxes)
        self.controller.fill_sheet_data(data, all_options)

    def run(self):
        data, date, all_options,  checkboxes = self.nomination_scrap()
        self.parse_data_in_sheet(data, date, all_options, checkboxes)
