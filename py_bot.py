import telebot

from user import User
from settings import *
from decouple import config
from types import GeneratorType
from botrequests.lowprice import low_price
from telebot.types import ReplyKeyboardRemove


bot = telebot.TeleBot(config('API_TOKEN'))
users = User()


@bot.message_handler(commands=['help', 'lowprice'])
def command_handler(message):
    user_id = message.from_user.id
    users.set_user(user_id, message.text)

    if message.text == '/help':
        users.well_done(user_id)
        send_answer(user_id, COMMAND_LIST)

    elif message.text == '/lowprice':
        send_answer(user_id, GIVE_ME_CITY)


@bot.message_handler(func=lambda message: users.get_user_command(message.from_user.id))
def message_handler(message) -> None:
    user_id = message.from_user.id
    user_command = users.get_user_command(user_id)

    if user_command:
        if user_command == '/lowprice':
            answer = low_price(users, message)
            low_price_cmd(user_id, answer)


@bot.message_handler(content_types=['text'])
def message_handler(message) -> None:
    user_id = message.from_user.id
    text = message.text.lower()
    send_answer(user_id, HI) if text == 'привет' else send_answer(user_id, DONT_UNDERSTAND)


def send_answer(user_id: str, answer: str, k_board: bool = False) -> None:
    """
    Обработчик отправки сообщений.
    Включает и выключает клавиатуру.

    :param user_id: id необходимого пользователя (str)
    :param answer: ответ для пользователя (str)
    :param k_board: необходимо ли вывести клавиатуру? (bool)
    :return: None
    """
    if k_board:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Да', 'Нет')
        bot.send_message(user_id, answer, reply_markup=keyboard)
    else:
        bot.send_message(user_id, answer, reply_markup=ReplyKeyboardRemove())


def low_price_cmd(user_id: str, msg: str) -> None:
    """
    Обработчик последнего шага команды lowprice
    - Оформляет текстовое сообщение
    - Оформляет фотографии

    :param user_id: id пользователя (str)
    :param msg: сообщение (str)
    :return: None
    """
    if isinstance(msg, GeneratorType):
        for i in range(users.get_amount(user_id)):
            try:
                content = next(msg)
                if users.get_photo(user_id):  # если нужно прикрепить фото
                    caption = '\n'.join(content[:4])
                    link = content[-1][:-10] + 'w.jpg'

                    bot.send_photo(user_id, link, caption=caption)

                else:
                    send_answer(user_id, '\n'.join(content[:4]))
            except StopIteration:
                send_answer(user_id, f'Всего найдено {i + 1} результатов')
                users.well_done(user_id)
                break
        users.well_done(user_id)
    else:
        if users.get_step(user_id) == 3:
            send_answer(user_id, msg, True)
        else:
            send_answer(user_id, msg)


def listen() -> None:
    bot.polling(none_stop=True, interval=0)
