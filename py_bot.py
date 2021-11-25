import telebot

from user import User
from settings import *
from decouple import config
from types import GeneratorType
from botrequests.lowprice import low_price
from telebot.types import ReplyKeyboardRemove, InputMediaPhoto

bot = telebot.TeleBot(config('API_TOKEN'))
users = User()


@bot.message_handler(commands=['start', 'help', 'lowprice'])
def command_handler(message) -> None:
    """
    Осуществляет перехват команд и создаёт первую реакцию на них
    :param message: объект сообщения

    :return: None
    """
    user_id = message.from_user.id
    users.set_user(user_id, message.text)
    text = message.text[1:]

    if text == 'start':
        users.well_done(user_id)
        send_answer(user_id, START)

    elif text == 'help':
        users.well_done(user_id)
        send_answer(user_id, COMMAND_LIST)

    elif text == 'lowprice':
        send_answer(user_id, GIVE_ME_CITY)


@bot.message_handler(func=lambda message: users.get_user_command(message.from_user.id))
def message_handler(message) -> None:
    """
    Осуществляет перехват сообщений от тех пользователей, которые уже
    осуществили запрос какой-либо команды
    :param message: объект сообщения

    :return: None
    """
    user_id = message.from_user.id
    user_command = users.get_user_command(user_id)
    text = message.text.lower()
    step = users.get_step(user_id)

    if user_command:
        if user_command == '/lowprice':
            if text in ('да', 'нет'):
                if text == 'нет' and step == 3:
                    send_answer(user_id, WAIT)
            elif text.isdigit():
                if int(text) in range(2, 11) and step == 4:
                    send_answer(user_id, WAIT)
            answer = low_price(users, message)
            low_price_cmd(user_id, answer)


@bot.message_handler(content_types=['text'])
def message_handler(message) -> None:
    """
    Осуществляет перехват любых сообщений от пользователей, если они не делали
    запрос на команды или уже получили результат от какой-либо команды
    :param message: объект сообщения

    :return: None
    """
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
    result_count = 0
    if isinstance(msg, GeneratorType):
        for i in range(users.get_amount(user_id)):
            try:
                result_count = i + 1
                content = next(msg)
                if users.get_photo(user_id):  # если нужно прикрепить фото
                    caption = '\n'.join(content[:4])
                    links = [InputMediaPhoto(link[:-10] + 'w.jpg', caption) for link in content[-1]]
                    bot.send_media_group(user_id, links)
                else:
                    send_answer(user_id, '\n'.join(content[:4]))
            except StopIteration:
                users.well_done(user_id)
                break
        send_answer(user_id, f'🔎 Всего найдено результатов: {result_count}\n'
                             f'ℹ Чтобы воспользоваться другими командами напишите: /help')
        users.well_done(user_id)
    else:
        if users.get_step(user_id) == 3:
            send_answer(user_id, msg, True)
        else:
            send_answer(user_id, msg)


def listen() -> None:
    bot.polling(none_stop=True, interval=0)
