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
all_data = []
data = {}

# URLs of the web page to scrape
urls = [
    "https://autocj.co.jp/usedcar?stock=R00165564",
    "https://autocj.co.jp/usedcar?stock=R00155019",
    "https://autocj.co.jp/usedcar?stock=R00150024",
]
# Site url
site_url = "https://autocj.co.jp"
for url in urls:
    # response
    response = requests.get(url, headers=headers, timeout=5)
    print(response)

    # Add a delay
    time.sleep(6)

    page = BeautifulSoup(response.content, "html.parser")
    # print(page.prettify())

    # stock title name
    try:
        car_title = page.find_all("div", class_="car_title").find("h1").text.strip()
        car_title = car_title.replace("\xa0", " ")  # Remove the 'Â' character
    except:
        car_title = None

    # car SKU
    try:
        car_sku = page.find("h3", class_="h3_carpage").text.strip()
        stock_model_code.append(car_sku)
    except:
        car_sku = "None"

    # Scrape car images
    image_elements = page.find_all("div", attrs={"id": "photo"})
    for getImages in image_elements:
        getImage = getImages.find_all("img", src=True)
        for imageUrl in getImage:
            stock_images.append(site_url + imageUrl["src"])

    # Car Price
    car_price = page.find("div", class_="pricelist")

    # FOB Price
    try:
        car_fob_price = car_price.find_all("dd")
        fob_price = car_fob_price[1].text.strip()
        # print(fob_price)
        stock_price.append(fob_price)
    except:
        car_fob_price = None

    # Original Price
    try:
        original_price = car_fob_price[0].text.strip()
        # print(original_price)
        stock_total_price.append(original_price)
    except:
        original_price = None

    # Feature List
    car_feature_list = page.find_all("div", class_="voption")
    for feature_list in car_feature_list:
        feature_detail = feature_list.find_all("tr")
        for features in feature_detail:
            feature = features.find("td").text
            stock_features_list.append(feature)

    # Car Specification title labels and values
    # Find the <div> element with class "vinfo"
    vinfo_element = page.find("div", class_="vinfo")

    # Find all <dt> and <dd> elements within the <div class="vinfo">
    dt_elements = vinfo_element.find_all("dt")
    dd_elements = vinfo_element.find_all("dd")

    # Create lists to store the extracted data
    keys = []
    values = []

    # Iterate over the <dt> and <dd> elements and extract the data
    for dt, dd in zip(dt_elements, dd_elements):
        dt_text = dt.text.strip()
        dd_text = dd.text.strip()
        keys.append(dt_text)
        values.append(dd_text)

    data = {
        "Car Name": car_title,
        "Car Model Code": "".join(stock_model_code),
        "Car FOB Price": "".join(stock_price),
        "Car Stock Total Price": "".join(stock_total_price),
        "Car Images": " | ".join(stock_images),
        "Car Features List": " | ".join(stock_features_list),
        "Stock URLs": url,
    }
    data.update(dict(zip(keys, values)))
    print(data)
    # Append the data to the list of all data
    all_data.append(data)

# Filter Data into DataFrame
df = pd.DataFrame(all_data)
# print(df.shape)
print("Got these many results:", df.shape)
csv_filename = "autocj_co_jp_data.csv"
df.to_csv(csv_filename, index=False)

print("Data saved to", csv_filename)
