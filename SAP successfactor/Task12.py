import time

from SeleniumHelperUtils import HelperMethod
from controllers import Controller_GroupFilter
from models import Model_GroupFilters_FilterType, Model_GroupFilters_Standard_Element, Model_GroupFilters_HRIS_ELement
from gspread_formatting import *
from gspread.utils import rowcol_to_a1

class GroupFiltersValidation:
    def __init__(self, driver):
        self.driver = driver
        self.helperMethod = HelperMethod(driver)
        self.controller = Controller_GroupFilter()

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

    def scrap_sap(self):
        filter_count = len(self.helperMethod.getElements('//input[@aria-label = "Type"]', 'xpath'))
        filter_types = []
        standard_elements = []
        HRIS_element = []
        for i in range(1,filter_count):
            self.helperMethod.waitforElementTobeInvisible('//div[@class="overlayShim"]', 'xpath')
            # scraping filter type selected option
            filter_types.append(self.scrap_filter_type(i))
            self.helperMethod.clickElement(f'(//table[contains(@class, "dataGridLayout")]//a[contains(@class,  "writeComp")])[{i}]', 'xpath')
            standard_elements.extend(self.scrap_standard_element())
            HRIS_element.extend(self.scrap_HRIS_element())
            self.helperMethod.clickElement('//button[@name = "Done"]', 'xpath')
        return filter_types, standard_elements, HRIS_element

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
            selected_value = self.helperMethod.getElementAttributeText(
            '//td[@class="field_value"]//input[@aria-label="HRIS Element Reference"]', 'xpath', 'title')
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

    def compare_data(self, sheet_filter_types, sap_filter_types, sheet_standard_elemenet, sap_standard_elements, sheet_HRIS_element, sap_HRIS_element):
        cell_list = []
        cell_list.extend(self.compare_standard_elements(sap_standard_elements, sheet_standard_elemenet))
        cell_list.extend(self.compare_HRIS_element(sap_HRIS_element, sheet_HRIS_element))
        return cell_list

    def compare_standard_elements(self, sap_standard_elements, sheet_standard_elements):
        cell_list = []
        green = cellFormat(backgroundColor=color(0, 1, 0))
        red = cellFormat(backgroundColor=color(1, 0, 0))
        attribute_names = ["filter_type", "selected_value"]
        sheet_dict = {(value.filter_type, value.selected_value): value for value in sheet_standard_elements}
        for sap_obj in sap_standard_elements:
            key = (sap_obj.filter_type, sap_obj.selected_value)
            if key in sheet_dict:
                sheet_obj = sheet_dict[key]
                for col, attribute_name in enumerate(attribute_names, start = 6):
                    if str(getattr(sap_obj, attribute_name)) == str(getattr(sheet_obj, attribute_name)):
                        cell_list.append((rowcol_to_a1(sheet_obj.itemId+1, col), green))
                    else:
                        cell_list.append((rowcol_to_a1(sheet_obj.itemId +1, col), red))
                del sheet_dict[key]
        if sheet_dict:
            for value in sheet_dict.values():
                for col, attribute_name in enumerate(attribute_names, start=6):
                    cell_list.append((rowcol_to_a1(value.itemId + 1, col), red))
        return cell_list

    def compare_HRIS_element(self, sap_HRIS_element, sheet_HRIS_element ):
        cell_list = []
        green = cellFormat(backgroundColor=color(0, 1, 0))
        red = cellFormat(backgroundColor=color(1, 0, 0))
        attribute_names = ['filter_type', 'element_reference', 'effective_date', 'field_id', 'reference_field']
        sheet_dict = {(value.element_reference, value.field_id, value.reference_field) : value for value in sheet_HRIS_element}
        for sap_obj in sap_HRIS_element:
            key = (sap_obj.element_reference, sap_obj.field_id, sap_obj.reference_field)
            if key in sheet_dict:
                sheet_obj = sheet_dict[key]
                for col, attribute_name in enumerate(attribute_names, start=10):
                    if str(getattr(sap_obj, attribute_name)) == str(getattr(sheet_obj, attribute_name)):
                        cell_list.append((rowcol_to_a1(sheet_obj.itemId+1, col), green))
                    else:
                        cell_list.append((rowcol_to_a1(sheet_obj.itemId+1, col), red))
                del sheet_dict[key]
        if sheet_dict:
            for value in sheet_dict.values():
                for col, attribute_name in enumerate(attribute_names, start=10):
                    cell_list.append((rowcol_to_a1(value.itemId + 1, col), red))
        return cell_list

    def run(self):
        sheet_filter_types, sheet_standard_elemenet, sheet_HRIS_element = self.controller.load_sheet_data()
        if sheet_HRIS_element and sheet_HRIS_element:
            self.navigate()
            sap_filter_types, sap_standard_elements, sap_HRIS_element = self.scrap_sap()
            cell_list = self.compare_data(sheet_filter_types, sap_filter_types, sheet_standard_elemenet, sap_standard_elements, sheet_HRIS_element, sap_HRIS_element)
            self.controller.sheet_formatting(cell_list)
            self.controller.change_status()
        else:
            print("No element pending")