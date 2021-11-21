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
        if text.isalpha():
            users.set_city(user_id, city_request(text.capitalize()))
            users.step_done(user_id)
            return GIVE_ME_COUNT
        else:
            return ERR_NOT_STR

    elif step == 2:
        if text.isdigit():
            if 0 < int(text) < 11:
                users.set_amount(user_id, int(text))
                users.step_done(user_id)
                return NEED_PHOTO
            return ERR_LOW_VALUE
        else:
            return ERR_NOT_INT

    elif step == 3:
        if text in ('да', 'нет'):
            users.set_photo(user_id, text == 'да')
        else:
            return ERR_WRONG_ANSWER

        try:
            city = users.get_city(user_id)
            amount = users.get_amount(user_id)
            photo = users.get_photo(user_id)
            time = datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d')

            return get_result(next(city), amount, time, photo)
        except StopIteration as error:
            print(f'[ERROR] {error}: Ошибка запроса')
            return ERR_BAD_REQ
