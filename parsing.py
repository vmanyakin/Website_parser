import requests
from bs4 import BeautifulSoup
import csv


CSV = 'drom_kia.csv'
HOST = 'https://auto.drom.ru'
URL = 'https://auto.drom.ru/kia/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}


def get_html(url, params=''):
    response = requests.get(url, headers=HEADERS, params=params)
    return response

def error(x):
    c = ''
    for i in x:
        if i in '\xa0':
            c += '.'
        else:
            c += i
    return c


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='css-1psewqh')
    cards = []
    for item in items:
        cards.append(
            {
                'title': item.find('div', class_='css-wsa6w').find('span').get_text(strip=True),
                'power_full': item.find('div', class_='css-3xai0o').get_text(strip=True),
                'price': error(item.find('div', class_='css-1dv8s3l').get_text(strip=True)),
                'link_product': item.get('href')
            }
        )
    return cards


def save_doc(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Название продукта', 'Мощность', 'Цена', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['power_full'], item['price'], item['link_product']])


def parser():
    num_pages = int(input('Количество страниц для парсинга: ').strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, num_pages+1):
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
        print('Парсинг закончен')
    else:
        print('Error')


parser()
