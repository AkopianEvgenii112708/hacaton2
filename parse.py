from bs4 import BeautifulSoup
import requests
import datetime
import csv
from decorators import benchmark

count = 0
def get_html(url: str) -> str:
    '''
    Получает html код определенного сайта
    '''
    response = requests.get(url)
    return response.text

def get_data(html:str) -> None:
    '''
    Парсер - получает все данные с сайта
    '''
    soup = BeautifulSoup(html, 'html.parser')
    catalog = soup.find('div', class_='catalog-list')
    if not catalog:
        return False
    cars = catalog.find_all('a', class_='catalog-list-item')
    for car in cars:
        title = car.find('span', class_='catalog-item-caption').text.strip()

        description = car.find('span', class_='catalog-item-descr').text.strip()
        if not description:
            description = 'Нет пробега'

        price = car.find('span', class_='catalog-item-price').text

        try:
            image = car.find('img', class_='catalog-item-cover-img').get('src')
        except:
            image = 'Нет картинки!'

        data = {
            'title': title,
            'description': description,
            'price': price,
            'img': image
        }
        write_to_csv(data)
    return True
        # print(f'{title}, mileage: {mileage}, price: {price} image: {image}\n')

def write_to_csv(data: dict) -> None:
    '''
    Функция для записи данных в csv файл
    '''
    global count
    with open('cars.csv', 'a') as file:
        fieldname = ['#','Марка','Описание','Цена','Фото']
        writer = csv.DictWriter(file, fieldname)
        count += 1
        writer.writerow({
            '#': count,
            'Марка': data.get('title'),
            'Описание': data.get('description'),
            'Цена': data.get('price'),
            'Фото': data.get('img'),
        })
        
def prepare_csv() -> None:
    '''
    Подготавливает csv файл
    '''
    with open('cars.csv', 'w') as file:
        fieldname = ['#','Марка','Описание','Цена','Фото']
        writer = csv.DictWriter(file, fieldname)
        writer.writerow({
            '#': '#',
            'Марка': 'Марка',
            'Описание': 'Описание',
            'Цена': 'Цена',
            'Фото': 'Фото' 
        })


def main():
    i = 1
    prepare_csv()
    while True:
        BASE_URL = f'https://cars.kg/offers/{i}'
        html = get_html(BASE_URL)
        is_res = get_data(html)

        if not is_res:
            break
        print(f'Страница:{i}')
        i += 1

main()