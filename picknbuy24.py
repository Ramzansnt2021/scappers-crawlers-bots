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
all_data = []

# URLs of the web page to scrape
urls = [
    "https://www.picknbuy24.com/detail/?refno=0105000408",
    "https://www.picknbuy24.com/detail/?refno=0120959189",
    "https://www.picknbuy24.com/detail/?refno=0105000431",
]

for url in urls:
    # response
    response = requests.get(url, headers=headers, timeout=5)
    print(response)

    # Add a delay
    time.sleep(6)

    page = BeautifulSoup(response.content, "html.parser")
    # print(page.prettify())

    # Stock page elements

    inquiry_elements = page.select("#inquiry")

    # stock title name
    try:
        for car_title in inquiry_elements:
            title = car_title.find("h1").text.strip()
            title = title.replace("\n ", "")  # Remove the 'Â' character
            stock_names.append(title)
    except:
        car_title = None

    # car SKU
    try:
        car_sku = page.find("div", attrs={"id": "refno"}).text.strip()
        car_sku = car_sku.replace("\n", "")
        stock_model_code.append(car_sku)
    except:
        car_sku = "None"

    # Scrape car images
    image_elements = page.find_all("figure", attrs={"id": "photo"})
    for getImages in image_elements:
        getImage = getImages.find_all("img", src=True)
        for imageUrl in getImage:
            stock_images.append(imageUrl["src"])

    # Car Price
    car_price = page.find_all("div", class_="carPrice")
    # FOB Price
    try:
        for car_fob_price in car_price:
            fob_price = car_fob_price.find(
                "span", attrs={"id": "fobPrice"}
            ).text.strip()
            fob_price = "$" + fob_price
            # print("$" + fob_price)
        stock_price.append(fob_price)
    except:
        car_fob_price = None

    # Original Price
    try:
        for car_original_price in car_price:
            original_price = car_original_price.find(
                "span", attrs={"id": "oriPrice"}
            ).text.strip()

            original_price = "$" + original_price
            # print(original_price)
            stock_total_price.append(original_price)
    except:
        car_original_price = None

    # Extract additional data from HTML
    div_feature = page.find("div", class_="feature")
    if div_feature:
        table = div_feature.find("table")
        if table:
            rows = table.find_all("tr")
            for row in rows:
                columns = row.find_all("td")
                for i, column in enumerate(columns):
                    if i not in data:
                        data["Features", i] = []
                    data["Features", i].append(column.get_text().strip())

    # Car Specification title labels and values
    # Find the <div> element with class "optionBlock"
    optionBlock = page.find("div", class_="optionBlock").find_all("dl")
    # print(optionBlock)
    # Find all <dt> and <dd> elements within the <div class="optionBlock">
    for dl_elements in optionBlock:
        dt_text = dl_elements.find("dt").text.strip()
        data[dt_text] = [dd.text.strip() for dd in dl_elements.find_all("dd")]

    # Highlighted Features
    # Feature List
    car_feature_list = page.find_all("div", class_="specBlock")
    for feature_list in car_feature_list:
        ul_elements = feature_list.find_all("ul")
        for li_elements in ul_elements:
            feature = li_elements.find_all("li")
            for li in feature:
                ttl_spec = li.find("div", attrs={"class": "ttlSpec"}).text.strip()
                spec = li.find("div", attrs={"class": "spec"}).text.strip()
                data[ttl_spec] = spec

    data.update(
        {
            "Car Name": stock_names[-1].replace(" ", ""),
            "Car Model Code": stock_model_code[-1],
            "Car FOB Price": stock_price[-1],
            "Car Stock Total Price": stock_total_price[-1],
            # "Car Images": " | ".join(stock_images),
            "Car Highlighted List": " | ".join(stock_highlights_list),
            "Stock URLs": url,
        }
    )

    # Append the data to the list of all data
    all_data.append(data)

print(all_data)
# Filter Data into DataFrame
df = pd.DataFrame(all_data)
# print(df.shape)
print("Got these many results:", df.shape)
currentDateTime = datetime.now().strftime("%m-%d-%Y-%H-%M-%S-%p")
csv_filename = f"picknbuy24_dataSet-{currentDateTime}.csv"
df.to_csv(csv_filename, index=False)

print("Data saved to", csv_filename)
