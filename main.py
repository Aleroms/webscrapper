# this code is used in yellowpages-py for loop of results
# business_name = item.find_element(By.CLASS_NAME, value="business-name")
#     print(business_name.text)
#
#     try:
#         business_website = item.find_element(By.CLASS_NAME, value='track-visit-website')
#         print(business_website.get_attribute('href'))
#     except NoSuchElementException:
#         print('* no website')
#
#     try:
#         business_telephone = item.find_element(By.CSS_SELECTOR, value='.phones.phone.primary')
#         print(business_telephone.text)
#     except NoSuchElementException:
#         print('* no telephone listed')
#
#     try:
#         business_address = item.find_element(By.CLASS_NAME, value='street-address').text + \
#                            item.find_element(By.CLASS_NAME, value='locality').text
#         print(business_address)
#     except NoSuchElementException:
#         print('* no address listed')