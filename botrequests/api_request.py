import json
import requests

from decouple import config
from types import GeneratorType

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': config('API_KEY')
}


def city_request(city: str, locale: str = 'ru_RU') -> GeneratorType:
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

    response = requests.request("GET", url, headers=headers, params=querystring)
    entities = json.loads(response.text)["suggestions"][0]["entities"]

    for item in entities:
        if city == item['name']:
            yield item['destinationId']


def photo_request(hotel_id: str) -> dict:
    """
    Запрашивает первую фотографию из отеля по id отеля.
    Возвращает переработанный JSON -> dict

    :param hotel_id: hotel_id
    :return: dict()
    """
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel_id}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return json.loads(response.text)['hotelImages'][0]['baseUrl']


def get_result(city: str, amount: int, time, photo: bool = False) -> GeneratorType:
    """
    Выводит результаты для команды lowprice

    :param city: id города (str)
    :param amount: кол-во запросов на возвращение (int)
    :param time: время для поиска отелей на текуцщий момент (datetime)
    :param photo: необходимо ли фото? (bool)
    :return: GeneratorType
    """
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": city,
                   "pageNumber": "1",
                   "pageSize": "10",
                   "checkIn": time,
                   "checkOut": time,
                   "adults1": "1",
                   "sortOrder": "PRICE",
                   "locale": "ru_RU",
                   "currency": "RUB"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    results = json.loads(response.text)['data']['body']['searchResults']['results']

    for i, item in enumerate(results):
        # если сгенерировано больше необходимого
        if i + 1 > amount:
            break

        if 'ratePlan' in item.keys():
            hotel_name = item['name']
            address = f"Адрес: {item['address']['streetAddress']}"
            distance = f"{item['landmarks'][0]['distance']} от центра"
            price = f"Цена за ночь: {item['ratePlan']['price']['current']}"

            if photo:
                id_hotel = item['id']
                photo_url = photo_request(id_hotel)
                yield [hotel_name, address, distance, price, photo_url]

            else:
                yield [hotel_name, address, distance, price]
