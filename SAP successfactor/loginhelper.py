from SeleniumHelperUtils import HelperMethod


class SAP:
    def __init__(self,driver):
        self.driver = driver
        self.helperMethod = HelperMethod(self.driver)

    def login(self):
        with open('SAP Credentials.txt', 'r') as textfile:
            lines = textfile.readlines()
            company_id, user_name, password = lines
        company_id_box = self.helperMethod.getElement('//input[@placeholder="Enter Company ID"]', 'xpath')
        self.fill_form_field(company_id, company_id_box)
        self.helperMethod.clickElement('continueToLoginBtn', 'id')
        user_name_box = self.helperMethod.getElement('j_username', 'id')
        self.fill_form_field(user_name, user_name_box)
        password_box = self.helperMethod.getElement('j_password', 'id')
        self.fill_form_field(password, password_box)
        self.helperMethod.clickElement('logOnFormSubmit', 'id')


    def get_scrub_id(self):
        url = self.driver.current_url
        return  url[url.find("_s.crb="):]

    def fill_form_field(self, keys, element):
        try:
            element.clear()
            element.send_keys(keys)
        except Exception as e:
            print(e)