from pandas.core.arrays.categorical import recode_for_categories

from models import Model_RatingScale, Model_NominationSetup, Model_NominationSetup_Checkbox, Model_GroupFilters_Standard_Element, Model_GroupFilters_HRIS_ELement, Model_GroupFilters_FilterType
from gspread.utils import ValueInputOption, rowcol_to_a1
import gspread
from google.oauth2.service_account import Credentials
from gspread_formatting import *


class Controller_RatingScale:
    def __init__(self):
        scopes = ['https://www.googleapis.com/auth/spreadsheets',
                  'https://www.googleapis.com/auth/drive']
        link = 'https://docs.google.com/spreadsheets/d/1BwBSVdiMOyyuIEU3sOzSKxvTH9-Mu3USOAry4mLLKFU/edit?usp=sharing'

        creds = Credentials.from_service_account_file(r'D:\Net2Apps\Credentials.json', scopes=scopes)
        client = gspread.authorize(creds)
        workbook = client.open_by_url(link)
        self.worksheet = workbook.worksheet("Rating Scale")

    def fill_sheet_header(self, header):
        self.worksheet.update([header], 'A1')

    def fill_sheet_data(self, data):
        cell_list = []
        for index, obj in enumerate(data, start = 2):
            cell_list.append(gspread.Cell(index, 1, obj.itemId))
            cell_list.append(gspread.Cell(index, 2, obj.name))
            cell_list.append(gspread.Cell(index, 3, obj.desc))
            cell_list.append(gspread.Cell(index, 4, obj.score))
            cell_list.append(gspread.Cell(index, 5, obj.label))
            cell_list.append(gspread.Cell(index, 6, obj.score_desc))
        self.worksheet.update_cells(cell_list, value_input_option=ValueInputOption.user_entered)

    def reset_sheet(self):
        self.worksheet.clear()

    def fill_rating_scale_name(self, names):
        self.worksheet.update(names, 'H2')
        dropdown_validation = DataValidationRule(BooleanCondition('ONE_OF_LIST', ['Pending', "Processed"]), showCustomUi=True)
        set_data_validation_for_cell_range(self.worksheet, f'I2:I{len(names) + 1}', dropdown_validation)
        self.change_status()

    def load_sheet_data(self):
        all_records = self.worksheet.get_all_records()
        pending_rating_scale_name = [record.get('Rating Scale Name') for record in all_records if
                                     record.get('Status') == "Pending"]
        pending_rating_scale_records = [record for record in all_records if
                                        record.get("Name") in pending_rating_scale_name]
        pending_data = []
        for record in pending_rating_scale_records:
            obj = Model_RatingScale()
            obj.itemId = record.get("ItemId")
            obj.name = record.get('Name')
            obj.desc = record.get('Description')
            obj.score = record.get('Score')
            obj.label = record.get('Label')
            obj.score_desc = record.get("Score Description")
            pending_data.append(obj)
        return pending_rating_scale_name, pending_data

    def sheet_formatting(self, cell_list):
        if cell_list:
            format_cell_ranges(self.worksheet, cell_list)
        else:
            print("cell list is empty")

    def change_status(self):
        values = self.worksheet.col_values(8)
        self.worksheet.update([["Processed"]]*(len(values)-1), 'I2')

class Controller_NominationSetup:
    def __init__(self):
        scopes = ['https://www.googleapis.com/auth/spreadsheets',
                  'https://www.googleapis.com/auth/drive']
        link = 'https://docs.google.com/spreadsheets/d/1BwBSVdiMOyyuIEU3sOzSKxvTH9-Mu3USOAry4mLLKFU/edit?usp=sharing'
        creds = Credentials.from_service_account_file(r'D:\Net2Apps\Credentials.json', scopes=scopes)
        client = gspread.authorize(creds)
        workbook = client.open_by_url(link)
        self.worksheet = workbook.worksheet("Nomination Setup")

    def reset_sheet(self):
        self.worksheet.clear()

    def fill_sheet_header(self, header):
        self.worksheet.update([header], 'A1')

    def fill_history_date(self, date):
        self.worksheet.update([[date]], 'G2', value_input_option=ValueInputOption.user_entered)

    def fill_checkboxes_data(self, data):
        cells_list = []
        for index, value in enumerate(data, start=2):
            cells_list.append(gspread.Cell(index, 5,value.label))
            cells_list.append(gspread.Cell(index, 6, value.value))
        self.worksheet.update_cells(cells_list, value_input_option=ValueInputOption.user_entered)
        checkbox_validation = DataValidationRule(BooleanCondition('BOOLEAN', ('TRUE', 'FALSE')), showCustomUi=True)
        set_data_validation_for_cell_range(self.worksheet, f'F2:F{len(data) + 1}', checkbox_validation)

    def fill_sheet_data(self, data, all_options):
        dropdown_validation = DataValidationRule(BooleanCondition('ONE_OF_LIST', all_options),showCustomUi=True )
        set_data_validation_for_cell_range(self.worksheet, f'C2:C{len(data)+1}', dropdown_validation)
        cells_list = []
        for index, value in enumerate(data, start=2):
            cells_list.append(gspread.Cell(index, 1, value.itemId))
            cells_list.append(gspread.Cell(index, 2, value.name))
            cells_list.append(gspread.Cell(index, 3, value.selected_option))
        self.worksheet.update_cells(cells_list, value_input_option=ValueInputOption.user_entered)

    def scrap_sheet(self):
        all_records = self.worksheet.get_all_records()
        date = all_records[0].get("History Date")
        checkboxes = []
        for i in all_records:
            if i.get('Checkbox Label') != '':
                obj = Model_NominationSetup_Checkbox()
                obj.label = i.get('Checkbox Label').strip()
                obj.value = i.get("Checkbox Value")
                checkboxes.append(obj)
        data = []
        for record in all_records:
            obj = Model_NominationSetup()
            obj.itemId = record.get('ItemId')
            obj.name = record.get('Name')
            obj.selected_option = record.get('Form Template')
            data.append(obj)
        return data, date, checkboxes

    def sheet_formatting(self, cell_list):
        if cell_list:
            format_cell_ranges(self.worksheet, cell_list)
        else:
            print("cell list is empty")

class Controller_GroupFilter:
    def __init__(self):
        scopes = ['https://www.googleapis.com/auth/spreadsheets',
                  'https://www.googleapis.com/auth/drive']
        link = 'https://docs.google.com/spreadsheets/d/1BwBSVdiMOyyuIEU3sOzSKxvTH9-Mu3USOAry4mLLKFU/edit?usp=sharing'
        creds = Credentials.from_service_account_file(r'D:\Net2Apps\Credentials.json', scopes=scopes)
        client = gspread.authorize(creds)
        workbook = client.open_by_url(link)
        self.worksheet = workbook.worksheet("Dynamic Group Filters")

    def reset_sheet(self):
        self.worksheet.clear()

    def fill_sheet_header(self, header):
        self.worksheet.update([header], 'A1')

    def fill_sheet_processing_section(self, names):
        names_list = []
        for name in names:
            names_list.append([name])
        self.worksheet.update(names_list, 'P2')
        dropdown_validation = DataValidationRule(BooleanCondition('ONE_OF_LIST', ['Pending', "Processed"]), showCustomUi=True)
        set_data_validation_for_cell_range(self.worksheet, f'Q2:Q{len(names) + 1}', dropdown_validation)
        self.change_status()

    def fill_filter_type_section(self, data):
        cell_list = []
        for index, value in enumerate(data, start =2):
            cell_list.append(gspread.Cell(index, 1, value.itemId))
            cell_list.append(gspread.Cell(index, 2, value.selected_value))
            cell_list.append(gspread.Cell(index, 3, value.permission))
        self.worksheet.update_cells(cell_list, value_input_option=ValueInputOption.user_entered)

    def fill_standard_element_section(self, data, all_options):
        cell_list = []
        dropdown_validation = DataValidationRule(BooleanCondition('ONE_OF_LIST', all_options), showCustomUi=True)
        set_data_validation_for_cell_range(self.worksheet, f'G2:G{len(data) + 1}', dropdown_validation)
        for index, value in enumerate(data, start = 2):
            cell_list.append(gspread.Cell(index, 5, value.itemId))
            cell_list.append(gspread.Cell(index, 6, value.filter_type))
            cell_list.append(gspread.Cell(index, 7, value.selected_value))
        self.worksheet.update_cells(cell_list, value_input_option=ValueInputOption.user_entered)

    def fill_HRIS_element_section(self, data):
        cell_list = []
        for index, value in enumerate(data, start = 2):
            cell_list.append(gspread.Cell(index, 9, value.itemId))
            cell_list.append(gspread.Cell(index, 10, value.filter_type))
            cell_list.append(gspread.Cell(index, 11, value.element_reference))
            cell_list.append(gspread.Cell(index, 12, value.effective_date))
            cell_list.append(gspread.Cell(index, 13, value.field_id))
            cell_list.append(gspread.Cell(index, 14, value.reference_field))
        self.worksheet.update_cells(cell_list, value_input_option=ValueInputOption.user_entered)

    def load_sheet_data(self):
        all_records = self.worksheet.get_all_records()
        pending_filter_name = [record.get('Filter Type Processing Section') for record in all_records if
                                     record.get('Processing Status') == "Pending"]
        filter_types = []
        standard_element = []
        HRIS_element = []
        for record in all_records:
            item_id = record.get('ItemId')
            filter_type = record.get('Filter Type')
            permission_group_filter = record.get('Permission Group Filter')
            item_id_standard_element = record.get('ItemId Standard Element')
            standard_element_filter_type = record.get('Filter Type Standard Element')
            standard_element_selected_value = record.get('Standard Element')
            item_id_HRIS_element = record.get('ItemId Hris Element')
            HRIS_element_filter_type = record.get('Fitler Type Hris Element')
            HRIS_element_reference = record.get('HRIS Element Reference')
            extend_days = record.get('Extend By N Days')
            HRIS_field_id = record.get('HRIS Field ID')
            reference_field = record.get('Reference Field')
            if filter_type in pending_filter_name:
                filter_type_obj = Model_GroupFilters_FilterType()
                filter_type_obj.itemId = item_id
                filter_type_obj.selected_value = filter_type
                filter_type_obj.permission = permission_group_filter
                filter_types.append(filter_type_obj)
            if standard_element_filter_type in pending_filter_name:
                obj = Model_GroupFilters_Standard_Element()
                obj.itemId = item_id_standard_element
                obj.filter_type = standard_element_filter_type
                obj.selected_value = standard_element_selected_value
                standard_element.append(obj)
            if HRIS_element_filter_type in pending_filter_name:
                HRIS_obj = Model_GroupFilters_HRIS_ELement()
                HRIS_obj.itemId = item_id_HRIS_element
                HRIS_obj.filter_type = HRIS_element_filter_type
                HRIS_obj.element_reference = HRIS_element_reference
                HRIS_obj.effective_date = extend_days
                HRIS_obj.field_id = HRIS_field_id
                HRIS_obj.reference_field = reference_field
                HRIS_element.append(HRIS_obj)
        return filter_types, standard_element, HRIS_element

    def change_status(self):
        values = self.worksheet.col_values(16)
        self.worksheet.update([["Processed"]]*(len(values)-1), 'Q2')

    def sheet_formatting(self, cell_list):
        if cell_list:
            format_cell_ranges(self.worksheet, cell_list)
        else:
            print("cell list is empty")