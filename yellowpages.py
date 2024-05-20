from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

website = "https://yellowpages.com"
niche = "construction"
location = "Yakima, WA"
# keep browser open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# instantiates Chrome web driver, passing along options
driver = webdriver.Chrome(options=chrome_options)

driver.get(website)

# initial input to search
niche_input = driver.find_element(By.ID, value='query')
location_input = driver.find_element(By.ID, value='location')
submit_button = driver.find_element(By.CSS_SELECTOR, value="#search-form button")

# search for values passed
niche_input.send_keys(niche)
location_input.clear()
location_input.send_keys(location)
submit_button.click()

# the start of results
search_results_all = driver.find_element(By.CSS_SELECTOR, value='.search-results.organic')
results_list = search_results_all.find_elements(By.CLASS_NAME, value="result")
for item in results_list:
    business_name = item.find_element(By.CLASS_NAME, value="business-name")
    print(business_name.text)

    try:
        business_website = item.find_element(By.CLASS_NAME, value='track-visit-website')
        print(business_website.get_attribute('href'))
    except NoSuchElementException:
        print('* no website')

    try:
        business_telephone = item.find_element(By.CSS_SELECTOR, value='.phones.phone.primary')
        print(business_telephone.text)
    except NoSuchElementException:
        print('* no telephone listed')

    try:
        b_street_address = item.find_element(By.CLASS_NAME, value='street-address').text
        b_locality = item.find_element(By.CLASS_NAME, value='locality').text
        business_address = b_street_address + " " + b_locality
        print(business_address)
    except NoSuchElementException:
        print('* no address listed')
next_page = driver.find_element(By.CSS_SELECTOR, value='a.next.ajax-page')
next_page.click()
driver.quit()
