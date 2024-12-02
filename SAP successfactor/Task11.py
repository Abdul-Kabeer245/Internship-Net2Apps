from SeleniumHelperUtils import HelperMethod
from controllers import Controller_GroupFilter
import time
from loginhelper import SAP
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert

class GroupFiltersAutomation:
    def __init__(self, driver):
        self.driver = driver
        self.helperMethod = HelperMethod(driver)
        self.controller = Controller_GroupFilter()
        self.fill_field = SAP(self.driver)

    def navigate(self):
        # waiting for overlay to disappear
        time.sleep(3)
        self.helperMethod.waitforElementTobeInvisible('//div[@class="overlayShim"]', 'xpath')
        self.helperMethod.clickElement('//div[@class="leftNavigation"]//a[text() = "Filters"]', 'xpath')
        self.helperMethod.clickElement('//a[@title = "Dynamic Group Filters"]', 'xpath')
        self.helperMethod.clickElement('//a[text() = "DGFilters"]', 'xpath')
        self.helperMethod.waitforElementTobeInvisible('//div[@class="overlayShim"]', 'xpath')
        self.helperMethod.clickElement('//button [@title= "Take Action"]', 'xpath')
        self.helperMethod.clickElement('//a [@title= "Make Correction"]', 'xpath')

    def update_sap(self, standard_element, HRIS_element):
        filter_count = len(self.helperMethod.getElements('//input[@aria-label = "Type"]', 'xpath'))
        standard_element_dict, HRIS_element_dict = self.object_to_dict(standard_element, HRIS_element)
        for i in range(1,filter_count):
            filter_name = self.helperMethod.getElementAttributeText(f'(//input[@aria-label = "Type"])[{i}]', 'xpath', 'value')
            if filter_name in standard_element_dict:
                self.helperMethod.clickElement(f'(//table[contains(@class, "dataGridLayout")]//a[contains(@class,  "writeComp")])[{i}]', 'xpath')
                self.update_standard_element(standard_element_dict)
                # self.update_HRIS_element(HRIS_element_dict)
            self.helperMethod.clickElement('//button[@name = "Done"]', 'xpath')
        self.helperMethod.clickElement('//button[text() = "Save"]', 'xpath')

    def update_standard_element(self, standard_element_dict):
        delete_button_count = len(self.helperMethod.getElements('(//table[@aria-label="Standard Element"]//button[contains(@title, "Delete")])', 'xpath'))
        for i in range(1, delete_button_count+1):
            self.helperMethod.clickElement(f'(//table[@aria-label="Standard Element"]//button[contains(@title, "Delete")])[1]', 'xpath')
        for key, values in standard_element_dict.items():
            filter_name = self.helperMethod.getElementAttributeText(
                '//div[@class = "sfOverlayMgr"]//input[@aria-label = "Type"]', 'xpath', 'value')
            if key == filter_name:
                for index, value in enumerate(values, start= 1):
                    selection = value.selected_value[:value.selected_value.find("(")-1]
                    dropdown = self.helperMethod.getElement(f'(//input[@aria-label="Standard Element"])[last()]', 'xpath')
                    dropdown.send_keys(Keys.CONTROL + "A")
                    dropdown.send_keys(Keys.DELETE)
                    dropdown.send_keys(selection)
                    self.helperMethod.waitforElementTobeVisible('//div[@class="globalMenu sf-combo-listselect"]', 'xpath')
                    self.helperMethod.clickElement('//div[@class="globalMenu sf-combo-listselect"]//li[1]', 'xpath')

    def update_HRIS_element(self, HRIS_element_dict):
        HRIS_element_count = len(self.helperMethod.getElements(
            '//table[@aria-label = "HRIS Elements"]//a[contains(@class, "writeComp")]', 'xpath'))
        for i in range(1, HRIS_element_count):
            print(f"HRIS elemnet number {i}")
            filter_name = self.helperMethod.getElementAttributeText(
            '//div[@class = "sfOverlayMgr"]//input[@aria-label = "Type"]', 'xpath', 'value')
            element_reference_name = self.helperMethod.getElementAttributeText(f'(//input[@aria-label="HRIS Element Reference"])[{i}]', 'xpath', 'value')
            if element_reference_name.endswith('..'):
                element_reference_name = self.helperMethod.getElementAttributeText(f'(//input[@aria-label="HRIS Element Reference"])[{i}]', 'xpath', 'title')
            search_key = (filter_name, element_reference_name)
            if search_key in HRIS_element_dict:
                self.helperMethod.clickElement(f'(//table[@aria-label = "HRIS Elements"]//a[contains(@class, "writeComp")])[{i}]', 'xpath')
                items = HRIS_element_dict[search_key]
                self.update_element_reference(items)
                self.update_extend_by_days(items)
                delete_button_count = len(self.helperMethod.getElements('//table[@aria-label="HRIS Field Reference"]//button[contains(@title, "Delete")]', 'xpath'))
                for j in range(1, delete_button_count+1):
                    self.helperMethod.clickElement('(//table[@aria-label="HRIS Field Reference"]//button[contains(@title, "Delete")])[1]', 'xpath')
                    time.sleep(2)
                self.update_field_id(items)
        self.helperMethod.clickElement('(//button[@name = "Done"])[2]', 'xpath')

    def update_element_reference(self, items):
        try:
            existing_value = self.helperMethod.getElementAttributeText(
                '//td[@class="field_value"]//input[@aria-label="HRIS Element Reference"]', 'xpath', 'value')
            if existing_value.endswith("..."):
                existing_value = self.helperMethod.getElementAttributeText(
                    '//td[@class="field_value"]//input[@aria-label="HRIS Element Reference"]', 'xpath', 'title')
            if existing_value != items[0].element_reference:
                element_reference_element = self.helperMethod.getElement(
                    '//td[@class="field_value"]//input[@aria-label="HRIS Element Reference"]', 'xpath')
                element_reference_element.send_keys(Keys.CONTROL + "A")
                element_reference_element.send_keys(Keys.DELETE)
                time.sleep(2)
                element_reference_value = items[0].element_reference[: items[0].element_reference.find('(') - 1]
                element_reference_element.send_keys(element_reference_value)
                self.helperMethod.waitforElementTobeVisible('//div[@class="globalMenu sf-combo-listselect"]', 'xpath')
                self.helperMethod.clickElement('//div[@class="globalMenu sf-combo-listselect"]//li[1]', 'xpath')
        except:
            alert = Alert(self.driver)
            print(alert.text)
            alert.accept()
            return


    def update_extend_by_days(self, items):
        existing_value = self.helperMethod.getElementAttributeText(
            '//td[@class = "field_value"]//input[@type = "text"]', 'xpath', 'value')
        if str(existing_value) != str(items[0].effective_date):
            days = str(items[0].effective_date)
            if days.lower() != "Click or focus to edit".lower():
                input_box = self.helperMethod.getElement('//td[@class = "field_value"]//input[@type = "text"]', 'xpath')
                input_box.send_keys(Keys.CONTROL + "a")
                input_box.send_keys(Keys.DELETE)
                time.sleep(2)
                input_box.send_keys(days)

    def update_field_id(self, items):
        sheet_data = []
        for item in items:
            sheet_data.append(item.field_id)
        sap_data = []
        field_id_count = self.helperMethod.getElements('//input[@aria-label="Field ID"]', 'xpath')
        for i in range(1, field_id_count):
            id = self.helperMethod.getElementAttributeText(f'(//input[@aria-label="Field ID"])[{i}]', 'xpath', 'value')
            if id.endswith('...'):
                id = self.helperMethod.getElementAttributeText(f'(//input[@aria-label="Field ID"])[{i}]', 'xpath', 'title')
            sap_data.append(id)
        try:
            for item in items:
                field_id = self.helperMethod.getElement('(//input[@aria-label="Field ID"])[last()]', 'xpath')
                field_id.send_keys(Keys.CONTROL + 'a')
                field_id.send_keys(Keys.DELETE)
                time.sleep(1)
                selection = item.field_id[ item.field_id.find('(')+1 : item.field_id.find(')') ]
                field_id.send_keys(selection)
                self.helperMethod.waitforElementTobeVisible('//div[@class="globalMenu sf-combo-listselect"]//li[1]', 'xpath')
                self.helperMethod.clickElement('//div[@class="globalMenu sf-combo-listselect"]//li[1]', 'xpath')
                reference_field_value = item.reference_field
                if reference_field_value.lower() != "Click or focus to edit".lower():
                    reference_field_element = self.helperMethod.getElement('(//label[text() = "Reference Field"]/following-sibling::input)[last()]', 'xpath')
                    reference_field_element.send_keys(Keys.CONTROL + 'a')
                    reference_field_element.send_keys(Keys.DELETE)
                    reference_field_element.send_keys(reference_field_value)
        except:
            alert = Alert(self.driver)
            print(alert.text)
            alert.accept()
        self.helperMethod.clickElement('(//button[@name = "Done"])[2]', 'xpath')

    def object_to_dict(self, standard_element, HRIS_element):
        standard_element_dict = dict()
        HRIS_element_dict = dict()
        for i in standard_element:
            if i.filter_type not in standard_element_dict:
                standard_element_dict[i.filter_type] = [i]
            else:
                standard_element_dict[i.filter_type].append(i)

        for i in HRIS_element:
            key = (i.filter_type, i.element_reference)
            if key not in HRIS_element_dict:
                HRIS_element_dict[key]= [i]
            else:
                HRIS_element_dict[key].append(i)
        return standard_element_dict, HRIS_element_dict

    def run(self):
        filter_types, standard_element, HRIS_element = self.controller.load_sheet_data()
        if standard_element and HRIS_element:
            self.navigate()
            self.update_sap(standard_element, HRIS_element)
        else:
            print("No element pending")