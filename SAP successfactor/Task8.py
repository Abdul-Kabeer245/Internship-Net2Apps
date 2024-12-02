from selenium import webdriver
from controllers import Controller_NominationSetup
from models import Model_NominationSetup, Model_NominationSetup_Checkbox
from selenium.webdriver.support.ui import Select
from SeleniumHelperUtils import HelperMethod
from gspread_formatting import *
from gspread.utils import rowcol_to_a1

class NominationSetupValidation:
    def __init__(self, driver):
        self.controller = Controller_NominationSetup()
        self.driver = driver
        self.helperMethod = HelperMethod(self.driver)


    def scrap_sap(self, sheet_data):
        sap_date = self.helperMethod.getElementAttributeText('//input[@class = "calendarTagInput"]', 'xpath', 'value')
        sap_checkboxes = self.extract_checkbox_value()
        sap_found_data= self.extract_dropdown(sheet_data)
        return sap_found_data, sap_date, sap_checkboxes

    def extract_dropdown(self, sheet_data):
        found_data = []
        for data in sheet_data:
            if self.helperMethod.isElementPresent(f'//td[text() = "{data.name}"]', 'xpath'):
                dropdown = self.helperMethod.getElement(f'//td[text() = "{data.name}"]//..//select', 'xpath')
                select = Select(dropdown)
                row_data = Model_NominationSetup()
                row_data.itemId = '=ROW()-1'
                row_data.name = data.name
                row_data.selected_option = select.first_selected_option.text
                found_data.append(row_data)
        return found_data

    def extract_checkbox_value(self):
        checkboxes_number = self.helperMethod.getListofElementText('//input[@type = "checkbox"]//..', 'xpath')
        checkboxes = []
        for i in range(1, len(checkboxes_number)+1):
            obj = Model_NominationSetup_Checkbox()
            obj.label = self.helperMethod.getElementText(f'(//input[@type = "checkbox"]//..)[{i}]', 'xpath').strip()
            if self.helperMethod.getElementAttributeText(f'(//input[@type = "checkbox"])[{i}]', 'xpath', 'checked'):
                obj.value = 'True'
            else:
                obj.value = 'False'
            checkboxes.append(obj)
        return checkboxes

    def compare_values(self, sheet_data, sheet_date, sheet_checkboxes, sap_data, sap_date, sap_checkboxes):
        cell_list = []
        green = cellFormat(backgroundColor=color(0, 1, 0))
        red = cellFormat(backgroundColor=color(1, 0, 0))
        if sheet_date == sap_date:
            cell_list.append(('G2', green))
        else:
            cell_list.append(('G2', red))
        cell_list.extend(self.compare_checkbox(sheet_checkboxes, sap_checkboxes))
        cell_list.extend(self.compare_data(sheet_data,sap_data))
        return cell_list

    def compare_data(self, sheet_data, sap_data):
        cell_list = []
        green = cellFormat(backgroundColor=color(0, 1, 0))
        red = cellFormat(backgroundColor=color(1, 0, 0))
        sap_data_dict = {i.name: i.selected_option for i in sap_data}
        for sheet_obj in sheet_data:
            key = sheet_obj.name
            if key in sap_data_dict:
                value = sap_data_dict[key]
                if value.lower() == sheet_obj.selected_option.lower():
                    cell_list.append((rowcol_to_a1(int(sheet_obj.itemId)+1, 2), green))
                    cell_list.append((rowcol_to_a1(int(sheet_obj.itemId)+1, 3), green))
                else:
                    cell_list.append((rowcol_to_a1(int(sheet_obj.itemId)+1, 2), red))
                    cell_list.append((rowcol_to_a1(int(sheet_obj.itemId)+1, 3), red))
        return cell_list

    def compare_checkbox(self, sheet_checkboxes, sap_checkboxes):
        cell_list = []
        green = cellFormat(backgroundColor=color(0, 1, 0))
        red = cellFormat(backgroundColor=color(1, 0, 0))
        sheet_checkbox_dict = {i.label: i.value for i in sheet_checkboxes}
        for index, sap_obj in enumerate(sap_checkboxes, start = 2):
            key = sap_obj.label
            if key in sheet_checkbox_dict:
                value = sheet_checkbox_dict[key]
                if value.lower() == sap_obj.value.lower():
                    cell_list.append((rowcol_to_a1(index, 6), green))
                else:
                    cell_list.append((rowcol_to_a1(index, 6), red))
        return cell_list

    def run(self):
        sheet_data, sheet_date, sheet_checkboxes = self.controller.scrap_sheet()
        sap_data, sap_date, sap_checkboxes  = self.scrap_sap(sheet_data)
        cell_list = self.compare_values(sheet_data, sheet_date, sheet_checkboxes, sap_data, sap_date, sap_checkboxes)
        self.controller.sheet_formatting(cell_list)