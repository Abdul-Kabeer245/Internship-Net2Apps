from Task2 import RatingScaleScraper
from Task3 import RatingScaleValidation
from Task4 import RatingScaleAutomation
from Task6 import NominationsSetupScraper
from Task7 import NominationSetupAutomation
from  Task8 import NominationSetupValidation
from Task10 import GroupFiltersScraper
from Task11 import GroupFiltersAutomation
from Task12 import GroupFiltersValidation
from selenium import webdriver
from loginhelper import SAP

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('https://hcm41preview.sapsf.com/')
loginHelper = SAP(driver)
loginHelper.login()
scrub_id = loginHelper.get_scrub_id()

task_no = int(input("Enter task no:"))
while task_no != 0:
    if task_no == 2:
        print("Initializing RatingScaleScraper Object")
        obj = RatingScaleScraper(driver)
        driver.get(
            'https://hcm41preview.sapsf.com/acme?fbacme_o=admin&pess_old_admin=true&ap_param_action=form_rating_scale&itrModule=talent&' + scrub_id)
        print("Running Task2")
        obj.run()

    if task_no == 3:
        print("Initializing RatingScaleValidation")
        obj = RatingScaleValidation(driver)
        driver.get(
            'https://hcm41preview.sapsf.com/acme?fbacme_o=admin&pess_old_admin=true&ap_param_action=form_rating_scale&itrModule=talent&' + scrub_id)
        print("Running Task3")
        obj.run()

    if task_no == 4:
        print("Initializing RatingScaleAutomation")
        obj = RatingScaleAutomation(driver)
        driver.get(
            'https://hcm41preview.sapsf.com/acme?fbacme_o=admin&pess_old_admin=true&ap_param_action=form_rating_scale&itrModule=talent&' + scrub_id)
        print("Running Task4")
        obj.run()

    if task_no ==6:
        print("Initializing NominationsSetupScraper")
        driver.get('https://hcm41preview.sapsf.com/acme?fbacme_o=admin&pess_old_admin=true&ap_param_action=nominations_setup&itrModule=talent&' + scrub_id)
        obj = NominationsSetupScraper(driver)
        print("Running Task6")
        obj.run()

    if task_no == 7:
        print("Initializing NominationSetupAutomation ")
        obj = NominationSetupAutomation(driver)
        driver.get('https://hcm41preview.sapsf.com/acme?fbacme_o=admin&pess_old_admin=true&ap_param_action=nominations_setup&itrModule=talent&' + scrub_id)
        print("Running Task7")
        obj.run()

    if task_no == 8:
        print("Initializing NominationSetupValidation")
        obj = NominationSetupValidation(driver)
        driver.get('https://hcm41preview.sapsf.com/acme?fbacme_o=admin&pess_old_admin=true&ap_param_action=nominations_setup&itrModule=talent&' + scrub_id)
        print("Running Task8")
        obj.run()

    if task_no == 10:
        print("Initializing GroupFilterScraper")
        obj = GroupFiltersScraper(driver)
        driver.get('https://hcm41preview.sapsf.com/xi/ui/businessconfig/pages/adminConfiguration.xhtml?&' + scrub_id)
        print("Running Task10")
        obj.run()

    if task_no == 11:
        print("Initializing GroupFilterAutomation")
        obj = GroupFiltersAutomation(driver)
        driver.get('https://hcm41preview.sapsf.com/xi/ui/businessconfig/pages/adminConfiguration.xhtml?&' + scrub_id)
        print("Running Task11")
        obj.run()

    if task_no == 12:
        print("Initializing GroupFilterValidation")
        obj = GroupFiltersValidation(driver)
        driver.get('https://hcm41preview.sapsf.com/xi/ui/businessconfig/pages/adminConfiguration.xhtml?&' + scrub_id)
        print("Running Task12")
        obj.run()

    task_no = int(input("Enter task no or Enter 0 to exit:"))
