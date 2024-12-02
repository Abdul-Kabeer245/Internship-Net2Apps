import os.path

from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import openpyxl, csv
from selenium.webdriver.common.by import By



class HelperMethod:
    def __init__(self, driver):
        self.driver = driver

    def _get_by(self, locatorType):
        locatorTypes ={
            'ID': By.ID,
            'XPATH': By.XPATH,
            'CSS_SELECTOR': By.CSS_SELECTOR,
            'LINK_TEXT': By.LINK_TEXT,
            'PARTIAL_LINK_TEXT': By.PARTIAL_LINK_TEXT,
            'CLASS_NAME': By.CLASS_NAME,
            'NAME': By.NAME,
            'TAG_NAME': By.TAG_NAME
        }
        return locatorTypes.get(locatorType.upper())


    def getElement(self, locator, locatorType):
        try:
            locatortype = self._get_by(locatorType)
            if locatorType:
                element = self.driver.find_element(locatortype, locator)
                return element
            else:
                print(f'Invalid locatortype {locatorType}')
                return False
        except Exception as e:
            print(e)
            return False

    def getElementText(self, locator, locatorType):
        element = self.getElement(locator, locatorType)
        if element and element.text:
            return element.text
        elif element:
            print('Element has no text')
            return False
        else:
            return False

    def getElementAttributeText(self, locator, locatorType, attribute):
        element = self.getElement(locator, locatorType)
        if element:
                attribute_value =  element.get_attribute(attribute)
                if attribute_value:
                    return attribute_value
                else:
                    print('Element has no such attribute')
                    return False
        else:
            return False

    def clickElement(self, locator, locatorType):
        element = self.getElement(locator, locatorType)
        if element:
            try:
                element.click()
            except Exception as e:
                print(e)


    def getElements(self, locator, locatorType):
        try:
            locatorType = self._get_by(locatorType)
            if locatorType:
                element = self.driver.find_elements(locatorType, locator)
                return element
            else:
                print('Invalid locatortype')
                return False
        except NoSuchElementException:
            print('No such elements')
            return False
        except WebDriverException as e:
            print(f'Web driver exception occured: {e}')
            return False

    def getListofElementText(self, locator, locatorType):
        elements = self.getElements(locator, locatorType)
        if elements:
            elements_text = []
            for element in elements:
                text = element.text
                if text:
                    elements_text.append(text)
                else:
                    print('Elements has no text')
                    return False
            return elements_text
        else:
            return False


    def getListofElementAttributeText(self, locator, locatorType, attribute):
        elements = self.getElements(locator, locatorType)
        if elements :
            elements_attribute = []
            for element in elements:
                element_attribute = element.get_attribute(attribute)
                if element_attribute:
                    elements_attribute.append(element_attribute)
                else:
                    print('ELement has no such attribute')
                    return False
            return elements_attribute
        else:
            return False

    def isElementPresent(self,locator, locatorType):
        return self.getElement(locator, locatorType) is not False

    def waitforElementTobeVisible(self, locator, locatorType):
        try:
            locatortype = self._get_by(locatorType)
            if locatortype:
                WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((locatortype, locator)))
                return True
            else:
                print(f'Invalid locatorType: {locatorType}')
        except NoSuchElementException:
            return False

    def scrollToViewElement(self, locator, locatorType):
        element = self.getElement(locator, locatorType)
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def waitforElementTobeClickable(self, locator, locatorType):
        try:
            locatortype = self._get_by(locatorType)
            if locatortype:
                WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((locatortype, locator)))
                return True
            else:
                print(f'Invalid locatorType: {locatorType}')
        except NoSuchElementException:
            return False
        except Exception as e:
            print(e)
            return False

    def waitforElementTobeInvisible(self, locator, locatorType):
        try:
            locatortype = self._get_by(locatorType)
            if locatortype:
                WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located((locatortype, locator)))
                return True
            else:
                print(f'Invalid locatorType: {locatorType}')
        except Exception as e:
            print(e)
            return False

    def waitforAlert(self):
        try:
            return WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        except:
            return False

    def saveData(self, data,filename = 'Temporary file', extension='csv'):
        if not isinstance(data, list):
            raise TypeError("The 'data' parameter must be of type list")

        if not all(isinstance(item, dict) for item in data):
            raise TypeError("List must contain dictionaries")

        if not data:
            raise ValueError("List is empty. Cannot save file")

        filepath = os.path.abspath(f'{filename}.{extension}')

        if extension.lower() == 'csv':
            with open(filename + '.csv', 'w', encoding='utf-8', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

        elif extension.lower() == 'xlsx':
            # Creating a workbook
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(list(data[0].keys()))
            # Writing and saving data
            for item in data:
                ws.append(list(item.values()))
            wb.save(filename + '.xlsx')

        else:
            print("Unsupported file extension, Please use 'csv' or 'xlsx'.")

        return filepath