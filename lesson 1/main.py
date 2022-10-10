import re
from tkinter import W
from bs4 import BeautifulSoup, BeautifulStoneSoup
import requests, lxml
import json 


# url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
headers= {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36"
}

# req = requests.get(url, headers = headers)
# src = req.text
# # print(src)

# with open("index.html", "w", encoding="utf-8-sig") as file:
#     file.write(src)

# with open("index.html", encoding="utf-8-sig") as file:
#     src = file.read()

# soup = BeautifulSoup(src, "lxml")
# all_products_hrefs = soup.find_all(class_="mzr-tc-group-item-href")

# all_categories_dict = {}

# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = "https://health-diet.ru" + item.get("href")
#     all_categories_dict[item_text] = item_href
#     print(f'{item_text}: {item_href}')

# with open ("dictionery.json", "w", encoding="utf-8-sig") as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open("dictionery.json", encoding="utf-8-sig") as file:
    all_categories = json.load(file)

count = 0
for category_name, category_href in all_categories.items():

    if count < 3:
        
        rep = [",", " ", "-","'"]
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, "_")
        # print(category_name)

        req = requests.get(category_href, headers = headers)
        src = req.text

        with open(f'data/{count}_{category_name}.html', 'w', encoding='utf-8-sig') as file:
            file.write(src)

        count += 1