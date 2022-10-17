import json
import time
import requests
from bs4 import BeautifulSoup
import datetime
import csv
import asyncio
import aiohttp

books_data = []
curr_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

async def get_page_data(session, page):
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    url = f'https://www.labirint.ru/genres/1006/?available=1&paperbooks=1&display=table&page={page}'

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, "lxml")
        books_info = soup.find("tbody", class_='products-table__body').find_all("tr")

        for bi in books_info:
            book_data = bi.find_all("td")
            try:
                bname = book_data[0].find("a").text.strip()
            except:
                bname = 'Нет названия'
            try:
                bauthor = book_data[1].find_all("a")
                bauthor = ", ".join([ath.text for ath in bauthor])
            except:
                bauthor = 'Нет автора'
            try:
                bpublisher = book_data[2].find("a").text.strip()
            except:
                bpublisher = 'Нет издателя'
            try:
                bprice = int(book_data[3].find("span", class_="price-val").find("span").text.replace(" ", ""))
            except:
                bprice = 'Нет цены'
            try:
                bprice_old = int(book_data[3].find("span", class_="price-gray").text.replace(" ", ""))
            except:
                bprice_old = 'Нет цены'
            try:
                bdiscount = round((bprice_old - bprice) * 100 / bprice_old)
            except:
                bdiscount = 'Нет скидки'
            try:
                bavailable = book_data[5].find("div").text.strip()
            except:
                bavailable = 'Нет в наличии'

            books_data.append({
                "Наименование": bname,
                "Автор": bauthor,
                "Издатель": bpublisher,
                "Цена": bprice,
                "Цена без скидки": bprice_old,
                "Скидка": bdiscount,
                "Наличие": bavailable
            })

        print(f'page number {page} is done')

async def gather_data():
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    url = 'https://www.labirint.ru/genres/1006/?available=1&paperbooks=1&display=table'

    async with aiohttp.ClientSession() as session:
        req = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await req.text(), 'lxml')
        pages_count = int(soup.find("div", class_="pagination-numbers__right").find_all("a")[-1].text)

        tasks = []
        session1 = []

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)

        for book in books_data:
            with open(f"labirint_{curr_time}.csv", "a", encoding='utf-8') as file:
                writer = csv.writer(file, lineterminator='\n')
                writer.writerow(
                    (
                        book['Наименование'],
                        book['Автор'],
                        book['Издатель'],
                        book['Цена'],
                        book['Цена без скидки'],
                        book['Скидка'],
                        book['Наличие']
                    )
                )


def main():
    asyncio.run(gather_data())


if __name__ == "__main__":
    main()