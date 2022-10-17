import json, lxml, requests
from bs4 import BeautifulSoup

with open("all_categories_dict.json", "r", encoding="utf-8") as file:
    all_cats_dict = json.load(file)

for cat_name, cat_href in all_cats_dict.items():
    cat_name = cat_name.replace(' ', "_")

    # указываем выше какого значения нас интересуют скидки
    wanted_discount = 5

    # создать src опросив сервер
    url_s = cat_href
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    req = requests.get(url_s, headers=headers)
    src = req.text
    # конец формирования src с реального сервера

    soup = BeautifulSoup(src, "lxml")
    pages = soup.find_all(class_="ImmXq R9QDJ hi0qF PaginationLink")
    page_counts = int(pages[len(pages) - 2].text)

    url = f"{cat_href}/page-"

    # переборка страницы любой категории, поиск всех товаров со скидкой >= wanted_discount

    # создаем словарь, в который будем сохранять найденные товары со скидкой, далее запишем его в JSON
    wanted_products_dict = {}
    founded_products = 0  # счетчик-айдишник для нумерации товаров в JSON (не смог найти решение как в словарь добавить
    # другой словарь без него)
    pages_fact_checked = 0  # количество реально проверенных страниц

    # запускаем цикл парсинга страниц и сбора данных в словарь
    for i in range(1, page_counts+1):
    # for i in range(1, 3):
        print(f'Парсинг страницы #{i}')
        req = requests.get(f"{url}{i}", headers=headers)
        src = req.text
        # вставить сюда код обработки 1 страницы
        soup = BeautifulSoup(src, "lxml")

        # находим в супе блоки с классом WdR1o, в настоящее время это блок карточки 1 товара
        products = soup.find_all(class_="WdR1o")

        # перебираем получившиеся товары, для каждого товара определяем, есть ли на него скидка
        # и что её размер больше той, что мы ищем задаётся в параметре wanted_discount

        for prod in products:
            if prod.find(class_="edke8 zR619 iSCbX nk2ei") is not None:
                discount_raw = prod.find(class_="edke8 zR619 iSCbX nk2ei").text
                discount = int(discount_raw[:len(discount_raw) - 1])
                if discount >= wanted_discount:
                    founded_products += 1
                    wanted_prod = {}
                    wanted_prod["product_name"] = prod.find(class_="ImmXq qUioe b8BqN ProductName").text
                    wanted_prod["product_href"] = f'https://divan.ru{prod.find(class_="ImmXq XGLam").get("href")}'
                    wanted_prod["product_new_price"] = prod.find(class_="Zq2dF F9ye5 LPzgl").text
                    wanted_prod["product_old_price"] = prod.find(class_="Zq2dF h1mna F9ye5 cUYnH").text
                    wanted_prod["product_discount"] = prod.find(class_="m2tc2").text
                    # print(wanted_prod)
                    wanted_products_dict[f'{founded_products}'] = wanted_prod
                    # print(wanted_products_dict)

        #   конец вставки кода обработки src 1 страницы
        i += 1
        pages_fact_checked += 1

    # Закончили собирать данные в словарик для JSON
    # смотрим, что получилось в словаре:
    print(f"Конец работы парсера, всего найдено товаров: {founded_products}, страниц обработано: {pages_fact_checked}")
    print("Словарь с найденными товарами:")
    print(wanted_products_dict)

    with open(f"divan_products/{cat_name}.json", "w", encoding="utf-8") as file:
        json.dump(wanted_products_dict, file, indent=4, ensure_ascii=False)
