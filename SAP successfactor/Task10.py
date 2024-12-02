import time

from SeleniumHelperUtils import HelperMethod
from controllers import Controller_GroupFilter
from models import Model_GroupFilters_FilterType, Model_GroupFilters_Standard_Element, Model_GroupFilters_HRIS_ELement


class GroupFiltersScraper:
    def __init__(self, driver):
        self.driver = driver
        self.helperMethod = HelperMethod(self.driver)
        self.controller = Controller_GroupFilter()

    def navigate(self):
        # waiting for overlay to disappear
        self.helperMethod.waitforElementTobeInvisible('//div[@class="overlayShim"]', 'xpath')
        self.helperMethod.clickElement('//div[@class="leftNavigation"]//a[text() = "Filters"]', 'xpath')
        self.helperMethod.clickElement('//a[@title = "Dynamic Group Filters"]', 'xpath')
        self.helperMethod.clickElement('//a[text() = "DGFilters"]', 'xpath')
        self.helperMethod.waitforElementTobeInvisible('//div[@class="overlayShim"]', 'xpath')
        self.helperMethod.clickElement('//button [@title= "Take Action"]', 'xpath')
        self.helperMethod.clickElement('//a [@title= "Make Correction"]', 'xpath')

    def scrap_sap(self):
        standard_element_all_options = []
        self.helperMethod.clickElement('(//span[contains(@class, "toggle")])[2]', 'xpath')
        # Scraping all options of filter type dropdown
        filter_type_all_options = self.helperMethod.getListofElementText(
            '//ul[contains(@class, "fd-list--dropdown")]//li//a', 'xpath')
        filter_count = len(self.helperMethod.getElements('//input[@aria-label = "Type"]', 'xpath'))
        filter_types = []
        standard_elements_selected_options = []
        HRIS_element = []
        for i in range(1,filter_count):
            self.helperMethod.waitforElementTobeInvisible('//div[@class="overlayShim"]', 'xpath')
            # scraping filter type selected option
            filter_types.append(self.scrap_filter_type(i))
            self.helperMethod.clickElement(f'(//table[contains(@class, "dataGridLayout")]//a[contains(@class,  "writeComp")])[{i}]', 'xpath')
            standard_elements_selected_options.extend(self.scrap_standard_element())
            standard_element_all_options.extend(self.scrap_standard_elements_all_options())
            HRIS_element.extend(self.scrap_HRIS_element())
            self.helperMethod.clickElement('//button[@name = "Done"]', 'xpath')
        return filter_type_all_options, filter_types, standard_elements_selected_options, standard_element_all_options, HRIS_element,

    def scrap_filter_type(self, i):
        obj = Model_GroupFilters_FilterType()
        obj.itemId = '=Row()-1'
        obj.selected_value = self.helperMethod.getElementAttributeText(
            f'(//input[@aria-label = "Type"])[{i}]', 'xpath', 'value')
        obj.permission = True
        return obj

    def scrap_standard_element(self):
        standard_elements =[]
        standard_element_count = len(self.helperMethod.getElements('//input[@aria-label = "Standard Element"]', 'xpath'))
        for i in range(1, standard_element_count):
            obj = Model_GroupFilters_Standard_Element()
            obj.itemId = '=Row()-1'
            obj.filter_type = self.helperMethod.getElementAttributeText(
                '//div[@class = "sfOverlayMgr"]//input[@aria-label = "Type"]', 'xpath', 'value')
            obj.selected_value = self.helperMethod.getElementAttributeText(f'(//input[@aria-label="Standard Element"])[{i}]', 'xpath', 'value')
            if obj.selected_value.endswith("..."):
                obj.selected_value = self.helperMethod.getElementAttributeText(f'(//input[@aria-label="Standard Element"])[{i}]', 'xpath', 'title')
            standard_elements.append(obj)
        return standard_elements

    def scrap_standard_elements_all_options(self):
        self.helperMethod.clickElement('//table[@aria-label = "Standard Element"]//span[contains(@class, "toggle")]', 'xpath')
        self.helperMethod.waitforElementTobeVisible('//div[contains(@class, "viewportOverlay")]//div[contains(@class, "listselect")]', 'xpath')
        dropdown = self.helperMethod.getElement('//div[contains(@class, "Menu sf-combo-listselect")]', 'xpath')
        total_height = self.driver.execute_script("return arguments[0].scrollHeight;", dropdown)
        visible_height = self.driver.execute_script("return arguments[0].clientHeight;", dropdown)
        for i in range(0, total_height, visible_height):
            self.driver.execute_script(f"arguments[0].scrollTo(0, {i});", dropdown)
            time.sleep(2)
        all_options = self.helperMethod.getListofElementAttributeText('//li[contains(@class, "globalMenuItem")]//a', 'xpath', 'title')
        return all_options

    def scrap_HRIS_element(self):
        HRIS_element = []
        filter_type = self.helperMethod.getElementAttributeText(
            '//div[@class = "sfOverlayMgr"]//input[@aria-label = "Type"]', 'xpath', 'value')
        HRIS_element_count = len(self.helperMethod.getElements(
            '//table[@aria-label = "HRIS Elements"]//a[contains(@class, "writeComp")]', 'xpath'))
        for i in range(1, HRIS_element_count):
            self.helperMethod.clickElement(
                f'(//table[@aria-label = "HRIS Elements"]//a[contains(@class, "writeComp")])[{i}]', 'xpath')
            # scrolling and scraping HRIS element reference all options
            HRIS = self.scrap_HRIS_field_reference(filter_type)
            HRIS_element.extend(HRIS)
        return HRIS_element

    def scrap_HRIS_field_reference(self, filter_type):
        HRIS_element = []
        selected_value = self.helperMethod.getElementAttributeText(
            '//td[@class="field_value"]//input[@aria-label="HRIS Element Reference"]', 'xpath', 'value')
        if selected_value.endswith("..."):
            selected_value = self.helperMethod.getElementAttributeText('//td[@class="field_value"]//input[@aria-label="HRIS Element Reference"]', 'xpath', 'title')
        date = self.helperMethod.getElementAttributeText(
            '//td[@class = "field_value"]//input[@type = "text"]', 'xpath', 'value')
        field_id_count = len(self.helperMethod.getElements('//input[@aria-label="Field ID"]', 'xpath'))
        for i in range(1, field_id_count):
            obj = Model_GroupFilters_HRIS_ELement()
            obj.itemId = '=Row()-1'
            obj.filter_type = filter_type
            obj.element_reference = selected_value[selected_value.find(":")+1:].strip()
            obj.effective_date = date
            obj.field_id = self.helperMethod.getElementAttributeText(f'(//input[@aria-label="Field ID"])[{i}]', 'xpath','value')
            if obj.field_id.endswith("..."):
                obj.field_id = self.helperMethod.getElementAttributeText(f'(//input[@aria-label="Field ID"])[{i}]', 'xpath','title')
            obj.reference_field = self.helperMethod.getElementAttributeText(
                f'(//label[text() = "Reference Field"]/following-sibling::input)[{i}]', 'xpath', 'value')
            HRIS_element.append(obj)
        self.helperMethod.clickElement('(//button[@name = "Done"])[2]', 'xpath')
        return HRIS_element

    def parse_data_in_sheet(self, filter_type_all_options, filter_types, standard_elements_selected_options, standard_element_all_options, HRIS_element):
        self.controller.reset_sheet()
        header = ['ItemId', 'Filter Type', 'Enabled', '1', "ItemId Standard Element", 'Filter Type Standard Element', 'Standard Element', '2',
                   "ItemId Hris Element", 'Fitler Type Hris Element', 'HRIS Element Reference', 'Extend By N Days', 'HRIS Field ID',
                  'Reference Field', '3', 'Filter Type Processing Section', 'Processing Status']
        self.controller.fill_sheet_header(header)
        self.controller.fill_filter_type_section(filter_types)
        self.controller.fill_sheet_processing_section(filter_type_all_options)
        self.controller.fill_standard_element_section(standard_elements_selected_options, standard_element_all_options)
        self.controller.fill_HRIS_element_section(HRIS_element)

    def run(self):
        self.navigate()
        filter_type_all_options, filter_types, standard_elements_selected_options, standard_element_all_options, HRIS_element = self.scrap_sap()
        self.parse_data_in_sheet(filter_type_all_options, filter_types, standard_elements_selected_options, standard_element_all_options, HRIS_element,)