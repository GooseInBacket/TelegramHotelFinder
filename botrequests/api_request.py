import datetime
import json
import time

import requests

from Exeptions import *
from settings import MAX_RESULT
from settings import KEY, NONE
from loguru import logger
from requests import ConnectionError

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': KEY
}


@logger.catch()
def city_request(city: str, locale: str = 'ru_RU') -> str:
    """
    Запрашивает destinationId по названию города

    :param city: название города (str)
    :param locale: в какой локации. По-умолчанию Россия (str)
    :return: GeneratorType
    """
    url = "https://hotels4.p.rapidapi.com/locations/search"

    querystring = {"query": city.capitalize(),
                   "locale": locale
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


@logger.catch()
def photo_request(hotel_id: str, amount: int = 4):
    """
    Запрашивает первую фотографию из отеля по id отеля.
    Возвращает переработанный JSON -> dict

    :param hotel_id: hotel_id
    :param amount: кол-во фотографий, которые необходимо вывести
    :return: dict()
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
                result = (data[i]['baseUrl'] for i in range(amount))
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
               sort_order: str = 'PRICE',
               photo: bool = False,
               p_count: int = 0) -> list:
    """
    Выводит результаты для команды lowprice, highprice

    :param city: id города (str)
    :param amount: кол-во запросов на возвращение (int)
    :param check_in: старт диапазона в котором нужно найти результат
    :param check_out: конец диапазона в котором нужно найти результат
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
                   "sortOrder": sort_order,
                   "locale": "ru_RU",
                   "currency": "RUB"}

    logger.info('Получение результата запроса по {}'.format(querystring))
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)

        results = json.loads(response.text)['data']['body']['searchResults']['results']

        status_code = response.status_code
        content_result = list()
        if status_code == 200:
            logger.info(f'Данные получены. Кол-во {len(results)}.Обрабатываю...')
            for item in results[:amount + 5]:
                if 'ratePlan' in item.keys():
                    hotel_name = item['name']
                    address = f"Адрес: {item['address'].get('streetAddress', NONE)}"
                    distance = f"{item['landmarks'][0].get('distance', NONE)} от центра"
                    price = f"Цена за ночь: {item['ratePlan']['price'].get('current', NONE)}"

                    if photo:
                        id_hotel = item['id']
                        photo_url = photo_request(id_hotel, p_count)
                        content_block = (hotel_name, address, distance, price, photo_url)
                    else:
                        content_block = (hotel_name, address, distance, price)

                    content_result.append(content_block)
            return content_result

        elif status_code == 429:
            logger.critical(f'API-KEY исчерпал кол-во запросов. Status code: {status_code}')
            raise ApiCloseErr

    except ConnectionError as err:
        logger.error(err)
        raise ConnectFail
