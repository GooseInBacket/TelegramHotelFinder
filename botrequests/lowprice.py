from settings import *
from botrequests.api_request import city_request, get_result
from datetime import datetime
from typing import Union
from types import GeneratorType


def low_price(users, message) -> Union[str, GeneratorType]:
    """
    Обработчик команды lowprice.

    1 этап. Приём от пользователя названия города и запрос кол-ва результатов
    2 этап. Приём кол-ва результатов и запрос необходимости фото.
    3 этап. Приём необходимости фото и подведение результатов запроса

    Город запрашивается на этапе запроса отслеживания команд

    :param users: объект пользователя
    :param message: объект сообщения от пользователя
    :return: str | generator
    """
    user_id = message.from_user.id
    step = users.get_step(user_id)
    text: str = message.text.lower()

    if step == 1:
        if city_data_validity(text):
            users.set_city(user_id, city_request(text.capitalize()))
            users.step_done(user_id)
            return GIVE_ME_COUNT
        return ERR_NOT_STR

    elif step == 2:
        if text.isdigit():
            if 0 < int(text) < 11:
                users.set_amount(user_id, int(text))
                users.step_done(user_id)
                return NEED_PHOTO
            return ERR_RANGE
        return ERR_NOT_INT

    elif step == 3:
        if text in ('да', 'нет'):
            users.set_photo(user_id, text == 'да')
            if text == 'да':
                users.step_done(user_id)
                return HOW_MUCH
            return last_step(users, user_id, message)
        return ERR_WRONG_ANSWER

    elif step == 4:
        if text.isdigit():
            if int(text) in range(2, 11):
                return last_step(users, user_id, message, int(text))
            raise ERR_RANGE
        return ERR_NOT_INT


def city_data_validity(city: str) -> bool:
    """
    Проверка города на корректный ввод
    :param city: Название города (str)

    :return: bool
    """
    if '-' in city:
        return ''.join(city.split('-')).isalpha()
    elif ' ' in city:
        return ''.join(city.split()).isalpha()
    else:
        return city.isalpha()


def last_step(users, user_id: str, message, ph_count: int = 0) -> Union[str, GeneratorType]:
    """
    Выполнение последнего шага в команде lowprice.
    Осуществляет группировку всех полученных данных.
    Возвращает результат запроса с сервера.

    :param users: объект с пользователями
    :param user_id: id необходимого пользователя
    :param message: объект сообщения
    :param ph_count: сколько нужно фото?
    :return: str | GeneratorType
    """
    try:
        city = users.get_city(user_id)
        amount = users.get_amount(user_id)
        photo = users.get_photo(user_id)
        time = datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d')

        return get_result(next(city), amount, time, photo, ph_count)
    except StopIteration:
        last_command = users.get_user_command(user_id)
        users.well_done(user_id)

        print(f'[ERROR]: Ошибка запроса. В переменной city - пустое значение')
        print(users.get_city(user_id), users.get_step(user_id), sep='\n')

        return ERR_BAD_REQ + last_command
