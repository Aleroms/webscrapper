from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re


class YellowPagesScraper:
    def __init__(self):
        self.website = "https://yellowpages.com"
        self.driver = webdriver.Chrome()
        self.driver.get(self.website)

    def scrape(self, niche, location):
        # Initial input to search
        niche_input = self.driver.find_element(By.ID, value='query')
        location_input = self.driver.find_element(By.ID, value='location')
        submit_button = self.driver.find_element(By.CSS_SELECTOR, value="#search-form button")

        # Search for values passed
        niche_input.send_keys(niche)
        location_input.clear()
        location_input.send_keys(location)
        submit_button.click()

        # The start of results

        while self.has_more_results():
            search_results_all = self.driver.find_element(By.CSS_SELECTOR, value='.search-results.organic')
            results_list = search_results_all.find_elements(By.CLASS_NAME, value="result")
            self.results(results_list)
            print("afters-")
            try:
                next_page = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.next.ajax-page'))
                )
                next_page.click()
            except ElementClickInterceptedException:
                # Scroll to the element and click using JavaScript
                self.driver.execute_script("arguments[0].scrollIntoView(true);", next_page)
                self.driver.execute_script("arguments[0].click();", next_page)
            except TimeoutException:
                print('Next page button not found or not clickable')
            time.sleep(2)

        print("quitting...")
        self.driver.quit()

    def has_more_results(self):
        count_raw = self.driver.find_element(By.CSS_SELECTOR, value="span.showing-count").text
        match = re.search(r'(\d+)-(\d+) of (\d+)', count_raw)
        # print(match.group(1) + ' ' + match.group(2) + ' ' + match.group(3))
        if match:
            # Extract the second and third captured groups
            current_end = int(match.group(2))
            total_results = int(match.group(3))
            return current_end < total_results
        else:
            # If the pattern does not match, return False
            return False

    def results(self, results_list):
        for i in range(len(results_list)):
            # Refresh the search results list to avoid stale element reference
            search_results_all = self.driver.find_element(By.CSS_SELECTOR, value='.search-results.organic')
            results_list = search_results_all.find_elements(By.CLASS_NAME, value="result")

            item = results_list[i]

            # Store the current URL
            current_url = self.driver.current_url

            # Click on the business name to go to the details page
            business_name = item.find_element(By.CLASS_NAME, value="business-name")
            print(business_name.text)
            try:
                business_name.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", business_name)
                self.driver.execute_script("arguments[0].click();", business_name)

            # Extract information from the details page
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'main-content')))

                # Add a short delay to ensure the page loads properly before proceeding
                time.sleep(2)

                business_website = self.get_website()
                print(business_website)

                business_telephone = self.get_telephone()
                print(business_telephone)

                business_address = self.get_address()
                print(business_address)

                business_email = self.get_email()
                print(business_email)

            except TimeoutException:
                print('Details page did not load properly')

            # Navigate back to the original search results page
            self.driver.get(current_url)
            # Add a short delay to ensure the page loads properly before proceeding
            time.sleep(2)

    def get_website(self):
        link = 'no website'
        try:
            # website
            bw = self.driver.find_element(By.CSS_SELECTOR, value='.website-link.dockable')
            link = bw.get_attribute('href')
        except NoSuchElementException:
            pass
        return link

    def get_telephone(self):
        telephone = 'no telephone'
        try:
            # telephone
            bt = self.driver.find_element(By.CLASS_NAME, value='phone')
            telephone = bt.text
        except NoSuchElementException:
            pass
        return telephone

    def get_address(self):
        address = 'no address'
        try:
            # address
            ba = self.driver.find_element(By.CLASS_NAME, value='address').text
            address = ba
        except NoSuchElementException:
            pass
        return address

    def get_email(self):
        email = 'no email'
        try:
            # email
            be = self.driver.find_element(By.CLASS_NAME, value='email-business')
            email = be.get_attribute('href')
        except NoSuchElementException:
            pass
        return email


test = YellowPagesScraper()
test.scrape("construction", "Yakima, WA")
