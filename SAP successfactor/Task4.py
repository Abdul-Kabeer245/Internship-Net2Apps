from selenium import webdriver
from SeleniumHelperUtils import HelperMethod
from controllers import Controller_RatingScale
from loginhelper import SAP

class RatingScaleAutomation:
    def __init__(self, driver):
        self.controller = Controller_RatingScale()
        self.driver = driver
        self.helperMethods = HelperMethod(self.driver)
        self.loginhelper = SAP(self.driver)

    def update_sap(self, data):
        data_dict = self.object_to_dict(data)
        for key, value in data_dict.items():
            if self.helperMethods.isElementPresent(f'(// span[contains( @ title, "Name of the rating")] // a[text() = "{key}"])','xpath'):
                self.helperMethods.clickElement(f'(// span[contains( @ title, "Name of the rating")] // a[text() = "{key}"])', 'xpath')
                self.update_existing_data(value)
            else:
                self.add_new_rating_scale(value)

    def update_existing_data(self, value):
        if self.helperMethods.isElementPresent('//button[@data-help-id="okButton"]', 'xpath'):
            self.helperMethods.clickElement('//button[@name = "OK"]', 'xpath')
        self.delete_score()
        name = self.helperMethods.getElement('//input[@data-testid = "sfTextField"]', 'xpath')
        rating_desc = self.helperMethods.getElement('//textarea[@id = "50:_txtArea"]', 'xpath')
        self.loginhelper.fill_form_field(value[0].name, name)
        self.loginhelper.fill_form_field(value[0].desc, rating_desc)
        for index, val in enumerate(value):
            self.helperMethods.clickElement('// a[text() = "Add New Score"]', 'xpath')
            score = self.helperMethods.getElement(f'//tr[contains(@class,"fd-table__row--compact")][{index + 1}]//td[1]//input', 'xpath')
            score_label = self.helperMethods.getElement(f'//tr[contains(@class,"fd-table__row--compact")][{index + 1}]//td[2]//input', 'xpath')
            score_desc = self.helperMethods.getElement(f'//tr[contains(@class,"fd-table__row--compact")][{index + 1}]//td[3]//textarea', 'xpath')
            self.loginhelper.fill_form_field(val.score, score)
            self.loginhelper.fill_form_field(val.label, score_label)
            self.loginhelper.fill_form_field(val.score_desc, score_desc)
        self.helperMethods.clickElement('(//span[text() = "Save"])', 'xpath')
        self.helperMethods.waitforElementTobeInvisible('//div[@class="overlayShim"]', 'xpath')
        self.helperMethods.clickElement('//a[text() = "Rating Scale Designer"]', 'xpath')

    def delete_score(self):
        delete_button = len(self.helperMethods.getElements('//a[@rel = "noopener noreferrer"]', 'xpath'))
        for i in range(1, delete_button):
            self.helperMethods.clickElement(f'(//a[@rel = "noopener noreferrer"])[1]', 'xpath')

    def add_new_rating_scale(self, data):
        self.helperMethods.clickElement('(//span[text() = "Create New Rating Scale"])', 'xpath')
        name = self.helperMethods.getElement('//input[@data-testid = "sfTextField"]', 'xpath')
        rating_desc = self.helperMethods.getElement('//textarea[@id = "50:_txtArea"]', 'xpath')
        self.loginhelper.fill_form_field(data[0].name, name)
        self.loginhelper.fill_form_field(data[0].desc, rating_desc)
        self.helperMethods.clickElement('(//span[text() = "Save"])', 'xpath')
        self.delete_score()
        for index, value in enumerate(data, start = 1):
            self.helperMethods.clickElement('// a[text() = "Add New Score"]', 'xpath')
            score = self.helperMethods.getElement(
                f'//tr[contains(@class,"fd-table__row--compact")][{index}]//td[1]//input', 'xpath')
            score_label = self.helperMethods.getElement(
                f'//tr[contains(@class,"fd-table__row--compact")][{index}]//td[2]//input', 'xpath')
            score_desc = self.helperMethods.getElement(
                f'//tr[contains(@class,"fd-table__row--compact")][{index}]//td[3]//textarea', 'xpath')
            self.loginhelper.fill_form_field(value.score, score)
            self.loginhelper.fill_form_field(value.label, score_label)
            self.loginhelper.fill_form_field(value.score_desc, score_desc)
        self.helperMethods.clickElement('//a[contains(@class, "toolbarButton")][1]', 'xpath')
        self.helperMethods.waitforElementTobeInvisible('//div[@class="overlayShim"]', 'xpath')
        self.helperMethods.clickElement('//a[text() = "Rating Scale Designer"]', 'xpath')

    def object_to_dict(self, data):
        names_dict = {}
        for d in data:
            if d.name not in names_dict:
                names_dict[d.name]= []
            names_dict[d.name].append(d)
        return names_dict

    def run(self):
        pending_names,  sheet_data = self.controller.load_sheet_data()
        if pending_names:
            self.update_sap(sheet_data)
        else:
            print("No rating scale is pending")