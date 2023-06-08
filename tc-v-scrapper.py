import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time

# List of URLs to scrape
urls = [
    "https://www.tc-v.com/used_car/bmw/1%20series/33693276/?isNew=1",
    "https://www.tc-v.com/used_car/toyota/land%20cruiser%20prado/32929679/?isNew=1",
    "https://www.tc-v.com/used_car/toyota/land%20cruiser%20prado/32668631/?isNew=1",
    "https://www.tc-v.com/used_car/mazda/demio/32738225/?isNew=1",
    "https://www.tc-v.com/used_car/bmw/x1/33633147/?isNew=1",
    "https://www.tc-v.com/used_car/suzuki/alto/32236783/?isNew=1",
]

# Create an empty list to store the scraped data
all_data = []
images = []
stock_specific_information = []
title_labels = []
title_values = []
options_key_values = []
options_value_values = []
features_info = []
car_names = []
car_fob_price = []
car_estimated_price = []

# Iterate over each URL
for url in urls:
    # Send a GET request to the URL
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Scrape car title
    car_title = soup.find("h1", class_="car__detail-ttl").text.strip()
    car_names.append(car_title)

    # Scrape features under title
    cars_feature = soup.select(".car__detail-tag-item")
    for features in cars_feature:
        feature = features.text.strip()
        features_info.append(feature)

    # Scrape car price
    car_price = soup.find("div", class_="car__price-body").text.strip()
    car_fob_price.append(car_price)

    # Scrape car estimate total pricing
    # car_price_estimated = soup.find(
    #     "span", attrs={"data-car-target": "displayTotalPriceEl"}
    # )
    car_total_price = soup.find(
        "span", attrs={"data-car-target": "displayTotalPriceEl"}
    ).text.strip()

    print("Estimated", car_total_price)
    car_estimated_price.append(car_total_price)

    # Scrape car images

    image_elements = soup.find_all("div", class_="car__detail-main-area")

    for getImages in image_elements:
        getImage = getImages.find_all("img", src=True)
        for imageUrl in getImage:
            images.append(imageUrl["src"])

    # Scrape stock-specific information
    info_elements = soup.find_all("li", class_="detail__list-item")

    for info_element in info_elements:
        info_text = info_element.text.strip()

        stock_specific_information.append(info_text)

    # Scrape title labels and values
    title_elements = soup.find_all("th", class_="car__info-table-ttl")
    for title_element in title_elements:
        title_text = title_element.text.strip()
        title_labels.append(title_text)

    value_elements = soup.find_all("td", class_="car__info-table-body")
    for value_element in value_elements:
        value_text = value_element.text.strip()
        title_values.append(value_text)

    # Scrape car options
    options_elements = soup.find_all("dt", class_="option__item-ttl")
    for option_element in options_elements:
        option_text = option_element.text.strip()
        options_key_values.append(option_text)

    values_elements = soup.find_all("dd", class_="option__item")
    for value_element in values_elements:
        value_text = value_element.text.strip()
        options_value_values.append(value_text)

    # Remove square brackets and single quotes from the scraped data
    car_title = re.sub(r"[\[\]']", "", car_title)
    car_price = re.sub(r"[\[\]']", "", car_price)
    images = [re.sub(r"[\[\]']", "", image) for image in images]
    stock_specific_information = [
        re.sub(r"[\[\]']", "", info) for info in stock_specific_information
    ]
    title_labels = [re.sub(r"[\[\]']", "", label) for label in title_labels]
    title_values = [re.sub(r"[\[\]']", "", value) for value in title_values]
    options_key_values = [
        re.sub(r"[\[\]']", "", option) for option in options_key_values
    ]
    options_value_values = [
        re.sub(r"[\[\]']", "", option) for option in options_value_values
    ]

    # Create separate lists for each key in the data dictionary
    car_titles = [car_title]
    car_prices = [car_price]
    car_images = [" | ".join(images)]
    stock_specific_info_lists = {
        label: value * len(car_titles)
        for label, value in zip(title_labels, title_values)
    }
    car_option_lists = [" | ".join(options_value_values)]

    # Create a dictionary for the scraped data from the current URL
    data = {
        "Car Title": car_title,
        "Car Price": car_price,
        "Car Total Price": car_total_price,
        "Car Images": " | ".join(images),
        "Car Features": " | ".join(features_info),
        **stock_specific_info_lists,
        "Car Options": " | ".join(options_value_values),
    }

    # Append the data to the list of all data
    all_data.append(data)

    # Add a 1-minute delay between each URL scrape
    time.sleep(5)

# Create a DataFrame from the list of all data

df = pd.DataFrame(all_data)
print(df)
print("Got these many results:", df.shape)

# Save the DataFrame to a CSV file
# currentDateTime = datetime.now().strftime("%m-%d-%Y-%H-%M-%S-%p")
# df.to_csv(f"tc-v-{currentDateTime}.csv", index=False)
# print("Data has been scraped and saved to CSV file")

# Add a delay
time.sleep(5)
