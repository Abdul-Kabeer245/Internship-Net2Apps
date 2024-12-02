from SeleniumHelperUtils import HelperMethod
from controllers import Controller_NominationSetup
from loginhelper import SAP
from selenium.webdriver.support.ui import Select

class NominationSetupAutomation:
    def __init__(self, driver):
        self.controller = Controller_NominationSetup()
        self.driver = driver
        self.helperMethods = HelperMethod(self.driver)

    def update_sap(self,data,date,checkboxes):
        field_helper = SAP(self.driver)
        date_field = self.helperMethods.getElement('//input[@class = "calendarTagInput"]', 'xpath')
        field_helper.fill_form_field(date, date_field)
        self.checking_box(checkboxes)
        self.select_dropdown_value(data)
        self.helperMethods.clickElement('//input[@value = "Save"]', 'xpath')
        self.driver.quit()

    def select_dropdown_value(self, data):
        for value in data:
            if self.helperMethods.isElementPresent(f'//td[text() = "{value.name}"]', 'xpath'):
                dropdown = self.helperMethods.getElement(f'//td[text() = "{value.name}"]//..//select', 'xpath')
                select = Select(dropdown)
                select.select_by_visible_text(value.selected_option)

    def checking_box(self, checkboxes):
        for i in checkboxes:
            value = self.helperMethods.getElementAttributeText(f'//td[contains(text()[1], "{i.label}") or contains(text()[2], "{i.label}")]//input', 'xpath','checked')
            value= 'false' if isinstance(value, bool) else 'true'
            if value.lower() != i.value.lower():
                self.helperMethods.clickElement(f'//td[contains(text()[1], "{i.label}") or contains(text()[2], "{i.label}")]//input', 'xpath')

    def run(self):
        data, date, checkboxes = self.controller.scrap_sheet()
        self.update_sap(data, date, checkboxes)