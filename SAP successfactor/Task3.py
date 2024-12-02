from selenium import webdriver
from models import Model_RatingScale
from SeleniumHelperUtils import HelperMethod
from controllers import Controller_RatingScale
from gspread.utils import rowcol_to_a1
from loginhelper import SAP
from gspread_formatting import *
class RatingScaleValidation:
    def __init__(self, driver):
        self.controller = Controller_RatingScale()
        self.driver = driver

    def scrap_sap(self, rating_scale_names):
        sap_data = []
        unfound_names = []
        helperMethods = HelperMethod(self.driver)
        for rating_scale_name in rating_scale_names:
            if helperMethods.isElementPresent(f'(// span[contains( @ title, "Name of the rating")] // a[text() = "{rating_scale_name}"])', 'xpath'):
                helperMethods.clickElement(f'(// span[contains( @ title, "Name of the rating")] // a[text() = "{rating_scale_name}"])',
                    'xpath')
                if helperMethods.isElementPresent('//button[@data-help-id="okButton"]', 'xpath'):
                    helperMethods.clickElement('//button[@name = "OK"]', 'xpath')
                item_data = self.extract_data(helperMethods)
                sap_data.extend(item_data)
                helperMethods.clickElement('//a[text() = "Rating Scale Designer"]', 'xpath')
            else:
                unfound_names.append(rating_scale_name)
        return sap_data, unfound_names

    def extract_data(self, helperMethod):
        data = []
        name = helperMethod.getElementAttributeText('//input[@data-testid = "sfTextField"]', 'xpath', 'value')
        rating_desc = helperMethod.getElementAttributeText('//textarea[@id = "50:_txtArea"]', 'xpath', 'value')
        scales = len(helperMethod.getElements('//table[@id = "66:m-m-tbl"]//tr', 'xpath'))
        for row in range(1, scales):
            score = helperMethod.getElementAttributeText(
                f'//tr[contains(@class,"fd-table__row--compact")][{row}]//td[1]//input', 'xpath', 'value')
            score_label = helperMethod.getElementAttributeText(
                f'//tr[contains(@class,"fd-table__row--compact")][{row}]//td[2]//input', 'xpath', 'value')
            score_desc = helperMethod.getElementAttributeText(
                f'//tr[contains(@class,"fd-table__row--compact")][{row}]//td[3]//textarea', 'xpath', 'value')
            row_data = Model_RatingScale()
            row_data.itemId="=ROW()-1"
            row_data.name=name if name else ""
            row_data.desc=rating_desc if rating_desc else ""
            row_data.score=score if score else ""
            row_data.label=score_label if score_label else ""
            row_data.score_desc = score_desc if score_desc else ""
            data.append(row_data)
        return data

    def compare_data(self, sap_data, sheet_data):
        cell_list = []
        green = cellFormat(backgroundColor=color(0, 1, 0))
        red = cellFormat(backgroundColor=color(1, 0, 0))
        attribute_names = ["name", 'desc', 'score', 'label', 'score_desc']
        sheet_dict = {(value.name, str(value.score)): value for value in sheet_data}
        for sap_value in sap_data:
            key = (sap_value.name, sap_value.score)
            if key in sheet_dict:
                sheet_value = sheet_dict[key]
                for col, attribute_name in enumerate(attribute_names, start=2):
                    if str(getattr(sap_value, attribute_name)) == str(getattr(sheet_value, attribute_name)):
                        cell_list.append((rowcol_to_a1(sheet_value.itemId + 1, col), green))
                    else:
                        cell_list.append((rowcol_to_a1(sheet_value.itemId+1, col), red))
                del sheet_dict[key]
        if sheet_dict:
            for value in sheet_dict.values():
                for col, attribute_name in enumerate(attribute_names, start =2 ):
                    cell_list.append((rowcol_to_a1(value.itemId+1, col), red))
        return cell_list

    def run(self):
        rating_scale_name, sheet_pending_data = self.controller.load_sheet_data()
        if sheet_pending_data:
            sap_data, unfound_names = self.scrap_sap(rating_scale_name)
            cell_list = self.compare_data(sap_data, sheet_pending_data)
            self.controller.sheet_formatting(cell_list)
            self.controller.change_status()
        else:
            print("No rating scale is pending")