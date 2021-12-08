import datetime
import json
import time

import requests

from bot_exceptions import *
from settings import KEY, NONE, MAX_RESULT
from loguru import logger
from requests import ConnectionError

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': KEY
}


def city_request(city: str) -> str:
    """
    Запрашивает "destinationId" по названию города

    :param city: название города (str)
    :return: str
    """
    url = "https://hotels4.p.rapidapi.com/locations/search"

    querystring = {"query": city.capitalize(),
                   "locale": 'ru_RU'
                   }
    while True:
        logger.info('Запрашиваю "destinationId" по городу "{}"'.format(city))
        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
            status_code = response.status_code
            if status_code == 200:
                entities = json.loads(response.text)["suggestions"][0]["entities"]
                for item in entities:
                    if city.lower() == item['name'].lower():
                        logger.info(f'"destinationId" удачно получен! {item["destinationId"]}')
                        return item['destinationId']
                else:
                    err = f'"destinationId" по {city} не найден'
                    logger.error(err)
                    raise NoCityErr(err)
            elif status_code == 429:
                logger.critical(f'API-KEY исчерпал кол-во запросов. Status code: {status_code}')
                raise ApiCloseErr
        except ConnectionError as err:
            logger.error(err)
            time.sleep(1)


def photo_request(hotel_id: str, amount: int = 4):
    """
    Запрашивает первую фотографию из отеля по id отеля.
    Возвращает переработанный JSON -> dict

    :param hotel_id: hotel_id
    :param amount: кол-во фотографий, которые необходимо вывести
    :return: Any
    """
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel_id}

    while True:
        logger.info('Запрашиваю фотографии отеля по id {}'.format(hotel_id))
        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
            status_code = response.status_code
            if status_code == 200:
                data = json.loads(response.text)['hotelImages']
                amount = len(data) if len(data) < amount else amount
                result = [data[i]['baseUrl'] for i in range(amount)]
                logger.success('Удачное получение фотографий')
                return result
            elif status_code == 429:
                logger.critical(f'API-KEY исчерпал кол-во запросов. Status code: {status_code}')
                raise ApiCloseErr
        except ConnectionError as err:
            logger.error(err)
            time.sleep(1)


@logger.catch()
def get_result(city: str,
               amount: int,
               check_in: datetime.date,
               check_out: datetime.date,
               price_min: str = '',
               price_max: str = '',
               distance_f_center: int = None,
               sort_order: str = 'PRICE',
               photo: bool = False,
               p_count: int = 0) -> list:
    """
    Выводит результаты для команды lowprice, highprice, bestdeal

    :param city: id города (str)
    :param amount: кол-во запросов на возвращение (int)
    :param check_in: старт диапазона в котором нужно найти результат
    :param check_out: конец диапазона в котором нужно найти результат
    :param price_min: минимальная цена за номер (str) (по-умолчанию = str()) для bestdeal
    :param price_max: максимальная цена за номер (str) (по-умолчанию = str()) для bestdeal
    :param distance_f_center: расстояние от центра (int) (по-умолчанию = None) для bestdeal
    :param sort_order: сортировка результатов (PRICE - по возрастанию,
                                               PRICE_HIGHEST_FIRST - по убыванию)
    :param photo: необходимо ли фото? (bool)
    :param p_count: сколько фото прикрепить нужно? (int) (по-умолчанию 0)
    :return: GeneratorType
    """
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": city,
                   "pageNumber": "1",
                   "pageSize": str(MAX_RESULT),
                   "check_in": check_in,
                   "check_out": check_out,
                   "adults1": "1",
                   "priceMin": price_min,
                   "priceMax": price_max,
                   "sortOrder": sort_order,
                   "locale": "ru_RU",
                   "currency": "RUB"}

    logger.info('Получение результата запроса по {}'.format(querystring))
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        results = json.loads(response.text)['data']['body']['searchResults']['results']

        status_code = response.status_code
        count = 0
        content_result = list()

        if status_code == 200:
            logger.info(f'Данные получены. Кол-во {len(results)}.Обрабатываю...')
            for item in results:
                if distance_f_center:
                    if correct_distance(item['landmarks'][0].get('distance')) <= distance_f_center:
                        if 'ratePlan' in item.keys():
                            count += 1
                            content_result.append(create_content(item, photo, p_count))
                elif 'ratePlan' in item.keys():
                    count += 1
                    content_result.append(create_content(item, photo, p_count))

                if count == amount:
                    return content_result
            return content_result

        elif status_code == 429:
            logger.critical(f'API-KEY исчерпал кол-во запросов. Status code: {status_code}')
            raise ApiCloseErr

    except ConnectionError as err:
        logger.error(err)
        raise ConnectFail


@logger.catch()
def create_content(item, photo: bool, p_count: int) -> tuple:
    """
    Создаёт блок контента исходя из полученных данных от пользователя
    :param item: объект с полезной информацией из API
    :param photo: есть ли необходимость в фото? (bool)
    :param p_count: если есть, то сколько? (int)
    :return: tuple
    """
    id_hotel = item['id']

    hotel_name = item['name']
    address = f"Адрес: {item['address'].get('streetAddress', NONE)}"
    distance = f"{item['landmarks'][0].get('distance')} от центра"
    price = f"Цена за ночь: {item['ratePlan']['price'].get('current', NONE)}"
    link = f'Ссылка: https://ru.hotels.com/ho{id_hotel}'

    if photo:
        photo_url = photo_request(id_hotel, p_count)
        return hotel_name, address, distance, price, link, photo_url
    else:
        return hotel_name, address, distance, price, link


@logger.catch()
def correct_distance(str_distance: str) -> float:
    """
    Корректирует контент 'дистанции от центра' во float для команды bestdeal
    :param str_distance: строка, которую нужно отредактировать во float
    :return: float
    """
    return float('.'.join(str_distance.split()[0].split(',')))
