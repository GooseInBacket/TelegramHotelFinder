from user import User
from settings import *
from bot_exceptions import *
from botrequests.api_request import city_request, get_result
from datetime import datetime
from typing import Union
from types import GeneratorType


def high_price(users: User,
               user_id: str,
               text: Union[str, datetime.date]) -> Union[str, GeneratorType]:
    """
    Обработчик команды highprice.

    1 этап. Приём от пользователя названия города и запрос кол-ва результатов
    2 этап. Приём от пользователя даты заезда из отеля, начиная с текущего дня.
    3 этап. Приём от пользователя даты выезда из отеля, начиная с текущего дня.
    4 этап. Приём кол-ва результатов и запрос необходимости фото.
    5 этап. Приём необходимости фото и их кол-ва
    6 этап. Подведение итогов запроса

    Город запрашивается на этапе запроса отслеживания команд

    :param users: объект пользователя
    :param user_id: объект сообщения от пользователя
    :param text: текст сообщения
    :return: str | generator
    """
    step = users.get_step(user_id)

    if step == 1:
        if city_data_validity(text):
            users.set_city(user_id, text.capitalize())
            users.step_done(user_id)
            return DATE_IN
        return ERR_NOT_STR

    elif step == 2:
        if validate(text):
            users.set_date_in(user_id, text)
            users.step_done(user_id)
            return DATE_OUT
        return ERR_DATE_FORMAT

    elif step == 3:
        if validate(text):
            users.set_date_out(user_id, text)
            users.step_done(user_id)
            return GIVE_ME_COUNT
        return ERR_DATE_FORMAT

    elif step == 4:
        if text.isdigit():
            if 0 < int(text) <= RANGE_RESULT:
                users.set_amount(user_id, int(text))
                users.step_done(user_id)
                return NEED_PHOTO
            return ERR_RANGE
        return ERR_NOT_INT

    elif step == 5:
        if text in ('да', 'нет'):
            users.set_photo(user_id, text == 'да')
            if text == 'да':
                users.step_done(user_id)
                return HOW_MUCH
            return last_step(users, user_id, text)
        return ERR_WRONG_ANSWER

    elif step == 6:
        if text.isdigit():
            if int(text) in range(2, 11):
                return last_step(users, user_id, int(text))
            return ERR_RANGE
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


def validate(date_text: str) -> bool:
    """
    проверка корректного ввода даты
    :param date_text: текст даты (str)
    :return: bool
    """
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def last_step(users: User, user_id: str, ph_count: int = 0) -> Union[str, list]:
    """
    Выполнение последнего шага в команде highprice.
    Осуществляет группировку всех полученных данных.
    Возвращает результат запроса с сервера.

    :param users: объект с пользователями
    :param user_id: id необходимого пользователя
    :param ph_count: сколько нужно фото?
    :return: str | GeneratorType
    """
    try:
        city = city_request(users.get_city(user_id))
        amount = users.get_amount(user_id)
        photo = users.get_photo(user_id)
        date_in = users.get_date_in(user_id)
        date_out = users.get_date_out(user_id)

        return get_result(city, amount, date_in, date_out,
                          sort_order='PRICE_HIGHEST_FIRST', photo=photo, p_count=ph_count)

    except ApiCloseErr:
        users.well_done(user_id)
        return ERR_API

    except NoCityErr:
        last_command = users.get_user_command(user_id)
        users.well_done(user_id)
        return ERR_NO_CITY.format(users.get_city(user_id), last_command)

    except ConnectFail:
        last_command = users.get_user_command(user_id)
        users.well_done(user_id)
        return ERR_CONN + last_command
