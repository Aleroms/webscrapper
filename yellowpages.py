from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



def getWebsite():
    link = 'no website'
    try:
        # website
        bw = driver.find_element(By.CSS_SELECTOR, value='.website-link.dockable')
        link = bw.get_attribute('href')
    except NoSuchElementException:
        pass
    return link


def getTelephone():
    telephone = 'no telephone'
    try:
        # telephone
        bt = driver.find_element(By.CLASS_NAME, value='phone')
        telephone = bt.text
    except NoSuchElementException:
        pass
    return telephone


def getAddress():
    address = 'no address'
    try:
        # address
        ba = driver.find_element(By.CLASS_NAME, value='address').text
        address = ba
    except NoSuchElementException:
        pass
    return address


def getEmail():
    email = 'no email'
    try:
        # email
        be = driver.find_element(By.CLASS_NAME, value='email-business')
        email = be.get_attribute('href')
    except NoSuchElementException:
        pass
    return email


website = "https://yellowpages.com"
niche = "construction"
location = "Yakima, WA"

# Keep browser open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Instantiates Chrome web driver, passing along options
driver = webdriver.Chrome(options=chrome_options)

driver.get(website)

# Initial input to search
niche_input = driver.find_element(By.ID, value='query')
location_input = driver.find_element(By.ID, value='location')
submit_button = driver.find_element(By.CSS_SELECTOR, value="#search-form button")

# Search for values passed
niche_input.send_keys(niche)
location_input.clear()
location_input.send_keys(location)
submit_button.click()

# The start of results
search_results_all = driver.find_element(By.CSS_SELECTOR, value='.search-results.organic')
results_list = search_results_all.find_elements(By.CLASS_NAME, value="result")

for i in range(len(results_list)):
    # Refresh the search results list to avoid stale element reference
    search_results_all = driver.find_element(By.CSS_SELECTOR, value='.search-results.organic')
    results_list = search_results_all.find_elements(By.CLASS_NAME, value="result")

    item = results_list[i]

    # Store the current URL
    current_url = driver.current_url

    # Click on the business name to go to the details page
    business_name = item.find_element(By.CLASS_NAME, value="business-name")
    print(business_name.text)
    try:
        business_name.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].scrollIntoView(true);", business_name)
        driver.execute_script("arguments[0].click();", business_name)

    # Extract information from the details page
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'main-content')))

        # Add a short delay to ensure the page loads properly before proceeding
        time.sleep(2)

        business_website = getWebsite()
        print(business_website)

        business_telephone = getTelephone()
        print(business_telephone)

        business_address = getAddress()
        print(business_address)

        business_email = getEmail()
        print(business_email)

    except TimeoutException:
        print('Details page did not load properly')

    # Navigate back to the original search results page
    driver.get(current_url)
    # Add a short delay to ensure the page loads properly before proceeding
    time.sleep(2)

try:
    next_page = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.next.ajax-page'))
    )
    next_page.click()
except ElementClickInterceptedException:
    # Scroll to the element and click using JavaScript
    driver.execute_script("arguments[0].scrollIntoView(true);", next_page)
    driver.execute_script("arguments[0].click();", next_page)
except TimeoutException:
    print('Next page button not found or not clickable')

driver.quit()
