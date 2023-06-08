import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the headers
headers = requests.utils.default_headers()

headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
)

# list variables

title = []
images = []
titleLabels = []
descriptionTitle = []
stockSpecificInformation = []
stockOptions = []
options_key_values = []
options_value_values = []
stockDescription3 = []
stockDescription4 = []
optionDetails = {}

# homeUrl = "https://www.tc-v.com"
# urls = input("Enter url without pagination number: ")
# n = int(input("Enter a last pagination number : "))
# finalUrls = []
# for i in range(0, n):
#     page = requests.get(urls + "?pn=" + str(i))
#     print(page)

#     soup = BeautifulSoup(page.content, "html.parser")

#     # print(soup.prettify())

#     getLinksLists = soup.select(".car-item__pic-area")
#     for aTags in getLinksLists:
#         aLinks = aTags.find("a", href=True)
#         print(aLinks["href"])
#         # print(homeUrl + aLinks["href"])
urls = ["https://www.tc-v.com/used_car/bmw/1%20series/33693276/?isNew=1"]
for i in range(0, len(urls)):
    page = requests.get(urls[i], headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup.prettify())
    # left side data
    getMainDiv = soup.select(".car__detail-main-area")
    # print(getMainDiv)
    # Right side data
    getRightDiv = soup.select(".car__detail-right-area-wrap")
    # Images
    for getImages in getMainDiv:
        getImage = getImages.find_all("img", src=True)
        for image in getImage:
            images.append(image["src"])

    # labels
    for getLabels in getMainDiv:
        getLabel = getLabels.select(".car__info-nav-area > .car__info-nav-item")
        for label in getLabel:
            titleLabels.append(label.text)

    # Description data variable
    sections = []
    for getMainDescription in getMainDiv:
        getSections = getMainDescription.select("section")

        for section in getSections:
            # Description headings
            getDescriptionTitle = section.find("h2")

        # Car Specific information
        for section in getSections:
            # description
            getDescriptions = section.find("table")
        stockSpecificInformation.append(getDescriptions)
        # Car Options

        for section in getSections:
            # details description
            getDescriptionsDl = section.select("dl")
            for detail in getDescriptionsDl:
                dtKeys = detail.find_all("dt")
                ddValues = detail.find_all("dd")

                # Ensure both lists have the same length using zip
                key_value_pairs = zip(dtKeys * len(ddValues), ddValues)

                # Create a DataFrame from the key-value pairs
                df = pd.DataFrame(key_value_pairs, columns=["dtKey", "ddValue"])

                # Iterate over the rows of the DataFrame
                for index, row in df.iterrows():
                    key_val = row["dtKey"]
                    value_val = row["ddValue"]
                    # print(key_val, value_val)

                    options_key_values.append(key_val)
                    options_value_values.append(value_val)
    # print(options_key_values)
    # print(options_value_values)

    # Right Side detailed data
    for rightSideTitle in getRightDiv:
        title = rightSideTitle.select("h1")
        print(title)

    for rightSideExpect in getRightDiv:
        expectText = rightSideExpect.select(".car__detail-tag-wrap ul li")
        for expect in expectText:
            print(expect.text)

    # Scrape car title
    car_title = soup.find("h1", class_="car__detail-ttl").text.strip()

    # Scrape car price
    car_price = soup.find("div", class_="car__price-body").text.strip()

    # Create separate lists for each key in the data dictionary
    car_titles = [car_title]
    car_prices = [car_price]
    print(car_titles, car_prices)
