import requests, json
from bs4 import BeautifulSoup

url = "https://divan.ru"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
#
# req = requests.get(url, headers=headers)
# src = req.text
#
# with open("index.html", "w", encoding="utf-8") as file:
#     file.write(src)
#
# with open("index.html", "r", encoding="utf-8") as file:
#     src = file.read()
#
# print(src)
#
# soup = BeautifulSoup(src, "lxml")
#
# categories = soup.find_all(class_="ImmXq oVF7p MenuLink")
# # print(categories)
#
# all_categories_dict = {}
# for item in categories:
#     category_name = item.text
#     category_href = f'{url}{item.get("href")}'
#
#     all_categories_dict[category_name] = category_href
#
# print(all_categories_dict)
#
# with open("all_categories_dict.json", "w", encoding="utf-8") as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)
# ---------------
# with open("all_categories_dict.json", "r", encoding="utf-8") as file:
#     all_categories_dict = json.load(file)
#
# # print(all_categories_dict)
# count = 1
# for category_name, category_href in all_categories_dict.items():
#
#     rep = [",", " ", "-", "'"]
#     for item in rep:
#         if item in category_name:
#             category_name = category_name.replace(item, "_")
#
#     req = requests.get(category_href, headers)
#     src = req.text
#
#     with open(f"data/{count}_{category_name}.html", "w", encoding="utf-8") as file:
#         file.write(src)
#     count += 1
# ---------


