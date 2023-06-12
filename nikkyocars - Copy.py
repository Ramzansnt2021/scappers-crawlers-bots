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
stock_features_list = []
data = {}
all_data = []
# URLs of the web pages to scrape
urls = [
    "https://www.nikkyocars.com/m/stock/stock-view.asp?lang=en&code=308741",
    "https://www.nikkyocars.com/m/stock/stock-view.asp?lang=en&code=303583",
]

# Site URL
site_url = "https://www.nikkyocars.com"

for url in urls:
    # response
    response = requests.get(url, headers=headers, timeout=5)
    print(response)

    # Add a delay
    time.sleep(6)

    page = BeautifulSoup(response.content, "html.parser")

    # Stock Title
    car_title = page.find("div", attrs={"id": "big_div"}).find_all("h1")

    for stock_name in car_title:
        stock_title = stock_name.find("b").text.strip()
        stock_names.append(stock_title)

    # Stock ID
    car_sku = (
        page.find("table", attrs={"id": "vehicle_tbl"})
        .find_all("tr")[0]
        .find("td")
        .text.strip()
    )
    stock_model_code.append(car_sku)

    # Prices
    left_div_elements = page.find_all("div", attrs={"id": "left_div"})
    for fob_prices in left_div_elements:
        fob_price = (
            fob_prices.find("span", attrs={"id": "top_FOB"})
            .find("span", class_="top_price")
            .text.strip()
        )
        fob_currency = (
            fob_prices.find("span", attrs={"id": "top_FOB"})
            .find("span", class_="currency")
            .text.strip()
        )
        fob = fob_currency + ":" + fob_price
        stock_price.append(fob)

    for original_prices in left_div_elements:
        original_price = (
            original_prices.find("span", attrs={"id": "top_CandF"})
            .find("span", class_="top_price")
            .text.strip()
        )
        original_currency = (
            original_prices.find("span", attrs={"id": "top_FOB"})
            .find("span", class_="currency")
            .text.strip()
        )
        based_price = original_currency + ":" + original_price
        stock_total_price.append(based_price)

    # Stock Images
    car_images = page.find("div", attrs={"class", "carousel-inner"}).find_all("img")
    for images in car_images:
        stock_image = images["src"]
        stock_images.append(site_url + stock_image)

    # Vehicle Specification
    specification = page.find("table", attrs={"id": "vehicle_tbl"}).find_all("tr")
    for specs in specification:
        th_text = specs.find("th").text.strip()
        td_text = specs.find("td").text.strip()
        data[th_text] = td_text

    # Car Options
    options = page.find("table", attrs={"id": "options_tbl"}).find_all("tr")
    for opt in options:
        td_text = opt.find_all("td", class_="text-info options_txt")
        if len(td_text) >= 2:
            key = td_text[0].get_text(strip=True)
            value = td_text[1].get_text(strip=True)
            features = key + value
            stock_features_list.append(features)

    data.update(
        {
            "Car Name": stock_names[-1],
            "Car Model Code": stock_model_code[-1],
            "Car FOB Price": stock_price[-1],
            "Car Stock Total Price": stock_total_price[-1],
            "Car Images": " | ".join(stock_images),
            "Stock Options": " | ".join(stock_features_list),
            "Stock URLs": url,
        }
    )
    print(data)
    all_data.append(data)
    # Reset lists and dictionary for next iteration
    stock_names = []
    stock_model_code = []
    stock_price = []
    stock_total_price = []
    stock_images = []
    stock_features_list = []
    data = {}

# Create DataFrame
df = pd.DataFrame(all_data)
print(df)
print("Got these many results:", df.shape[0])
# currentDateTime = datetime.now().strftime("%m-%d-%Y-%H-%M-%S-%p")
# csv_filename = f"nikkyocars_dataSet-{currentDateTime}.csv"
# df.to_csv(csv_filename, index=False)

# print("Data saved to", csv_filename)
