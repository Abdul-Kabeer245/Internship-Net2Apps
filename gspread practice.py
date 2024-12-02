import csv, openpyxl
import gspread
from google.oauth2.service_account import Credentials

# Defining scopes for sheets and drive
scopes = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']

creds = Credentials.from_service_account_file('Credentials.json', scopes = scopes)

client = gspread.authorize(creds)

# Task 1
workbook = client.open("All tasks")

worksheet = workbook.sheet1
worksheet.update_title("Task 1")
worksheet.update_tab_color('#f4a2b1')
with open('Task 1.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    values = list(reader)

worksheet.update(range_name='A1', values=values)
num_column = len(values[0])
header_range = f'A1:{chr(65+num_column-1)}1'
worksheet.format(header_range, {
    "backgroundColor": {
      "red": 0.0,
      "green": 0.0,
      "blue": 0.0
    },
    "horizontalAlignment": "CENTER",
    "textFormat": {
      "foregroundColor": {
        "red": 1.0,
        "green": 1.0,
        "blue": 1.0
      },
      "fontSize": 12,
      "bold": True
    }
})

# Task 2
worksheet_list = map(lambda x: x.title, workbook.worksheets())
new_worksheet_name = "Task 2"
if new_worksheet_name in worksheet_list:
    worksheet = workbook.worksheet(new_worksheet_name)
else:
    workbook.add_worksheet(new_worksheet_name, rows=100, cols=26)

worksheet = workbook.worksheet(new_worksheet_name)
worksheet.update_tab_color('#34c7d1')
with open('Task 2.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    values = list(reader)

worksheet.update(range_name='A1', values=values)
num_column = len(values[0])
header_range = f'A1:{chr(65+num_column-1)}1'
worksheet.format(header_range, {
    "backgroundColor": {
      "red": 0.0,
      "green": 0.0,
      "blue": 0.0
    },
    "horizontalAlignment": "CENTER",
    "textFormat": {
      "foregroundColor": {
        "red": 1.0,
        "green": 1.0,
        "blue": 1.0
      },
      "fontSize": 12,
      "bold": True
    }
})

# Task 3
worksheet_list = map(lambda x: x.title, workbook.worksheets())
new_worksheet_name = "Task 3"
if new_worksheet_name in worksheet_list:
    worksheet = workbook.worksheet(new_worksheet_name)
else:
    workbook.add_worksheet(new_worksheet_name, rows=100, cols=26)

worksheet = workbook.worksheet(new_worksheet_name)
worksheet.update_tab_color('#34c7d1')
#getting values
book = openpyxl.load_workbook('Task 3.xlsx')
sheet = book['Sheet']
values = list(sheet.values)

worksheet.update(range_name='A1', values=values)
num_column = len(values[0])
header_range = f'A1:{chr(65+num_column-1)}1'
worksheet.format(header_range, {
    "backgroundColor": {
      "red": 0.0,
      "green": 0.0,
      "blue": 0.0
    },
    "horizontalAlignment": "CENTER",
    "textFormat": {
      "foregroundColor": {
        "red": 1.0,
        "green": 1.0,
        "blue": 1.0
      },
      "fontSize": 12,
      "bold": True
    }
})


# Task 4
worksheet_list = map(lambda x: x.title, workbook.worksheets())
new_worksheet_name = "Task 4"
if new_worksheet_name in worksheet_list:
    worksheet = workbook.worksheet(new_worksheet_name)
else:
    workbook.add_worksheet(new_worksheet_name, rows=100, cols=26)

worksheet = workbook.worksheet(new_worksheet_name)
worksheet.update_tab_color('#e3d8b9')

#getting values
book = openpyxl.load_workbook('Task 4.xlsx')
sheet = book['Sheet']
values = list(sheet.values)

worksheet.update(range_name='A1', values=values)
num_column = len(values[0])
header_range = f'A1:{chr(65+num_column-1)}1'
worksheet.format(header_range, {
    "backgroundColor": {
      "red": 0.0,
      "green": 0.0,
      "blue": 0.0
    },
    "horizontalAlignment": "CENTER",
    "textFormat": {
      "foregroundColor": {
        "red": 1.0,
        "green": 1.0,
        "blue": 1.0
      },
      "fontSize": 12,
      "bold": True
    }
})

# Task 2
worksheet_list = map(lambda x: x.title, workbook.worksheets())
new_worksheet_name = "Task 5"
if new_worksheet_name in worksheet_list:
    worksheet = workbook.worksheet(new_worksheet_name)
else:
    workbook.add_worksheet(new_worksheet_name, rows=100, cols=26)

worksheet = workbook.worksheet(new_worksheet_name)
worksheet.update_tab_color('#9f7a2e')
with open('Task 5.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    values = list(reader)

worksheet.update(range_name='A1', values=values)
num_column = len(values[0])
header_range = f'A1:{chr(65+num_column-1)}1'
worksheet.format(header_range, {
    "backgroundColor": {
      "red": 0.0,
      "green": 0.0,
      "blue": 0.0
    },
    "horizontalAlignment": "CENTER",
    "textFormat": {
      "foregroundColor": {
        "red": 1.0,
        "green": 1.0,
        "blue": 1.0
      },
      "fontSize": 12,
      "bold": True
    }
})


