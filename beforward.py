import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time

# Define the headers
headers = requests.utils.default_headers()

headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
)

# defining lists and variable
stock_names = []
stock_model_code = []
stock_price = []
stock_total_price = []
stock_images = []
stock_features = []
stock_specifications = []
stock_features_list = []
stock_highlights_list = []

data = {}

# URL of the web page to scrape
url = "https://www.beforward.jp/daihatsu/terios-kid/bk627823/id/3132253/"

# response
response = requests.get(url, headers=headers, timeout=5)
print(response)

# Add a delay
time.sleep(60)

page = BeautifulSoup(response.content, "html.parser")
# print(page.prettify())

# stock title name
try:
    car_title = page.find_all("h1")[1].text
    stock_names.append(car_title)
except:
    car_title = "None"

# car SKU
try:
    car_sku = page.find("div", class_="detail-specs-text").text.strip()
    stock_model_code.append(car_sku)
except:
    car_sku = "None"

# Scrape car images
image_elements = page.find_all("div", class_="list-detail-left")

for getImages in image_elements:
    getImage = getImages.find_all("img", src=True)
    for imageUrl in getImage:
        stock_images.append(imageUrl["src"])


# Car Price
# car_price_section = page.find_all("div", class_="price-col-vehicle-link-area")
# print(car_price_section)
car_price = page.select(".vehicle-price").find("span").text.strip()
print(car_price)
# stock_price.append(car_price)
# car_total_price = page.find_all("p", class_="total-price")
# print(car_total_price)
# for total_price in car_total_price:
#     total = total_price.find("span").text.strip()
#     print(total)
# stock_total_price.append(car_total_price)

# Car Feature title labels and values
car_feature_title = []
title_elements = page.find_all("td", class_="specs-pickup-text")
for title_element in title_elements:
    title_text = title_element.text.strip()
    car_feature_title.append(title_text)

car_feature_value = []
value_elements = page.find_all("td", class_="pickup-specification-text")
for value_element in value_elements:
    value_text = value_element.text.strip()
    car_feature_value.append(value_text)

# Car Specification title labels and values
car_specification_title = []
car_specification_value = []
car_specification = page.find_all("table", class_="specification")
for title_elements in car_specification:
    title_element = title_elements.find("th", class_="gray").text.strip()
    car_specification_title.append(title_element)

for value_element in car_specification:
    title_element = title_elements.find("td").text.strip()
    car_specification_value.append(title_element)

# Feature List
car_feature_list = page.find_all("div", class_="remarks")
for feature_list in car_feature_list:
    feature_detail = feature_list.find_all("ul")
    for features in feature_detail:
        feature = features.find("li").text
        stock_features_list.append(feature)

# Car Specifications
car_specification_title = [label for label in car_specification_title]
car_specification_value = [value for value in car_specification_value]

stock_specific_info_lists = {
    label: value * len(stock_names)
    for label, value in zip(car_specification_title, car_specification_value)
}


data = {
    "Car Name": stock_names,
    "Car Model Code": stock_model_code,
    "Car Stock Price": stock_price,
    "Car Total Price": stock_total_price,
    # "Car Images": stock_images,
    **stock_specific_info_lists,
    "Car Features List": stock_features_list,
}
print(data)
# df = pd.DataFrame(data)
# print(df)
# print("Got these many results:", df.shape)
