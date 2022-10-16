import lxml
import requests
from bs4 import BeautifulSoup
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}
# # collect all festival links to JSON
fest_urls_list = []
fest_info_list = []

# for i in range(0, 192, 24):
    # url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=1%20Nov%202022&to_date=&where%5B%5D=2&maxprice=500&o={i}&bannertitle=May"
    #
    # req = requests.get(url=url, headers=headers)
    # print(req.text)
    # json_data = json.loads(req.text)
    # print(json_data)
    # html_response = json_data['html']
    #
    # with open(f'data/index_{i}.html', 'w', encoding='utf-8') as file:
    #     file.write(html_response)

    # with open(f'data/index_{i}.html', 'r', encoding='utf-8') as file:
    #     src = file.read()
    #
    # soup = BeautifulSoup(src, 'lxml')
    #
    # cards = soup.find_all('a', class_='card-details-link')
    #
    # for item in cards:
    #     fest_ulr = 'https://www.skiddle.com' + item.get('href')
    #     fest_urls_list.append(fest_ulr)
    #
    # with open(f'data/fest_ruls.json', 'w', encoding='utf-8') as file:
    #     json.dump(fest_urls_list, file, indent=4)

# collect fest info

with open(f'data/fest_urls_full.json', 'r', encoding='utf-8') as file:
    links = json.loads(file.read())

count = 0
for url in links:
    req = requests.get(url=url, headers=headers)

    # with open('fff.html', 'w', encoding='utf-8') as file:
    #     file.write(req.text)

    try:
        soup = BeautifulSoup(req.text, 'lxml')

        fest_name = soup.find(class_='MuiTypography-root MuiTypography-body1 css-r2lffm').text.strip()
        fest_address = json.loads(soup.find("script").text)['address']
        fest_info_block = soup.find(
            class_="MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation1 css-ckmrqz").find_all(
            class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 css-2re0kq')

        if len(fest_info_block) == 0:
            fest_date = ''
            fest_location = ''
            fest_price = ''

        if len(fest_info_block) == 2:
            fest_date = fest_info_block[0].find("span").text.strip()
            fest_location = fest_info_block[1].find("span").text.strip()
            fest_price = ''
        if len(fest_info_block) == 3:
            fest_date = fest_info_block[0].find("span").text.strip()
            fest_location = fest_info_block[1].find("span").text.strip()
            fest_price = fest_info_block[2].find("span").text.strip()


        # print('#' * 20)
        # print(fest_name)
        # print(fest_date)
        # print(fest_location)
        # print(fest_price)
        # print(fest_address)

        fest_info_list.append(
            {
                'fest_name': fest_name,
                'fest_date': fest_date,
                'fest_price': fest_price,
                'fest_location': fest_location,
                'fest_address': fest_address
            }
        )

    except Exception as ex:
        print(ex)
        print('some exception ')
        print(url)

with open(f'data/fest_info_list.json', 'w', encoding='utf-8') as file:
    json.dump(fest_info_list, file, indent=4)