import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from SeleniumHelperUtils import HelperMethod

class StreakScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)
        self.helperMethod = HelperMethod(self.driver)

    def navigator(self):
        # Create an ActionChains object to perform mouse actions
        action = ActionChains(self.driver)

        # Navigating to community menu
        community_menu = self.helperMethod.getElement('Community', 'LINK_TEXT')

        # Hovering over community menu
        action.move_to_element(community_menu).perform()

        # Clicking on streaks
        self.helperMethod.clickElement('//a[@href="/visit-streaks?ref=header_nav"]', 'XPATH')

    def show_more(self):
        items = len(self.helperMethod.getElements('//div[@class="my-5 flex flex-row items-center justify-center gap-3 px-2"]', 'XPATH'))
        for i in range(150//items+1):
            if len(self.helperMethod.getElements('//div[@class="my-5 flex flex-row items-center justify-center gap-3 px-2"]', 'XPATH')) <= 150:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(2)
            else:
                break


    def get_data(self):
        data = []
        for i in range(1, 151):
            name = self.helperMethod.getElementText(f'(//div[@class="text-16 font-semibold text-dark-gray"])[{i}]', 'XPATH')
            streak = self.helperMethod.getElementText(f'(//div[@class="text-14 font-normal text-light-gray"])[{i}]', 'XPATH').split()
            number = ''.join(n for n in streak if n.isdigit())
            data.append({
                'Name': name,
                'Streak': number
            })
        return data



    def run(self):
        #open the target url
        self.driver.get('https://www.producthunt.com/')
        # Navigate to streak page
        self.navigator()
        # Scroll to load 150 rows
        self.show_more()
        # Extracting data
        data= self.get_data()
        # Close the Webdriver
        self.driver.quit()
        # Saving data
        self.helperMethod.saveData(data, 'Task 4', 'xlsx')


# Run the scraper
scraper = StreakScraper()
scraper.run()
