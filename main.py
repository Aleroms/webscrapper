import pandas
from YellowpagesWebscraper import YellowPagesScraper

test = YellowPagesScraper()
niche = "construction"
city = "Yakima"
state = "WA"
location = f"{city}, {state}"

# scrape data
test_data = test.scrape("construction", "Yakima, WA")

# test_data = [
#     {
#         "name": "business_name.text",
#         "email": "business_email",
#         "phone": "business_telephone",
#         "address": "business_address",
#         "website": "business_website"
#     },
#     {
#         "name": "business_name.text",
#         "email": "business_email",
#         "phone": "business_telephone",
#         "address": "business_address",
#         "website": "business_website"
#     }
# ]

# write to csv
df = pandas.DataFrame(test_data)
df.to_csv(f'{niche}-{city}{state}.csv', index=False)

# confirm success
print("data saved successfully")
