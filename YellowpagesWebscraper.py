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
        self.data = []

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

        while self.has_more_results():
            search_results_all = self.driver.find_element(By.CSS_SELECTOR, value='.search-results.organic')
            results_list = search_results_all.find_elements(By.CLASS_NAME, value="result")
            self.results(results_list)

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

        self.driver.quit()
        return self.data

    def has_more_results(self):
        try:
            count_raw = self.driver.find_element(By.CSS_SELECTOR, value="span.showing-count").text
            print(count_raw)
            match = re.search(r'(\d+)-(\d+) of (\d+)', count_raw)
        except NoSuchElementException:
            return False

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
            # Avoids stale element reference
            try:
                search_results_all = self.driver.find_element(By.CSS_SELECTOR, value='.search-results.organic')
                results_list = search_results_all.find_elements(By.CLASS_NAME, value="result")
            except NoSuchElementException:
                print("could not find .search-results.organic")
                break

            item = results_list[i]

            # Store the current URL
            current_url = self.driver.current_url

            # Click on the business name to go to the details page
            business_link = item.find_element(By.CLASS_NAME, value="business-name")
            business_name = business_link.text
            try:
                business_link.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", business_link)
                self.driver.execute_script("arguments[0].click();", business_link)

            # Extract information from the details page
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'main-content')))
                time.sleep(2)

                business_website = self.get_website()
                business_telephone = self.get_telephone()
                business_address = self.get_address()
                business_email = self.get_email()

            except TimeoutException:
                print('Details page did not load properly')

            self.data.append({
                "name": business_name,
                "email": business_email,
                "phone": business_telephone,
                "address": business_address,
                "website": business_website
            })

            # Navigate back to the original search results page
            self.driver.get(current_url)
            time.sleep(2)

    def get_website(self):
        try:
            bw = self.driver.find_element(By.CSS_SELECTOR, value='.website-link.dockable')
            link = bw.get_attribute('href')
        except NoSuchElementException:
            link = 'no website'
        return link

    def get_telephone(self):
        try:
            bt = self.driver.find_element(By.CLASS_NAME, value='phone')
            telephone = bt.text
        except NoSuchElementException:
            telephone = 'no telephone'
        return telephone

    def get_address(self):
        try:
            ba = self.driver.find_element(By.CLASS_NAME, value='address').text
            address = ba
        except NoSuchElementException:
            address = 'no address'
        return address

    def get_email(self):
        try:
            be = self.driver.find_element(By.CLASS_NAME, value='email-business')
            email = be.get_attribute('href')
        except NoSuchElementException:
            email = 'no email'
        return email

# test case
# test = YellowPagesScraper()
# test_data = test.scrape("construction", "Yakima, WA")
