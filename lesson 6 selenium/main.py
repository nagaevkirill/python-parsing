import time

import requests
from headers import headers
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_data():
    url = 'https://tury.ru/hotel/most_luxe.php'
    req = requests.get(url=url, headers=headers)

    with open(f'file.html', 'w', encoding='utf-8') as file:
        file.write(req.text)


def get_data_selenium():
    url = 'https://www.divan.ru/category/krovati-korpusnye/page-4'

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url=url)
        time.sleep(2)

        print(driver.page_source)

        with open('sss.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)
        print('some errors')
    finally:
        driver.close()
        driver.quit()


def main():
    get_data_selenium()


if __name__ == '__main__':
    main()
