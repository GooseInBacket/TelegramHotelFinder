import datetime

import telebot

from user import User
from settings import *
from loguru import logger
from botrequests.lowprice import low_price
from botrequests.highprice import high_price
from botrequests.bestdeal import best_deal
from botrequests.history import make_history, add_to_history
from telebot.types import ReplyKeyboardRemove, InputMediaPhoto
from telegram_bot_calendar import DetailedTelegramCalendar

bot = telebot.TeleBot(TOKEN)
users = User()


@bot.message_handler(commands=['start', 'help', 'lowprice', 'highprice', 'bestdeal', 'history'])
def command_handler(message) -> None:
    """
    Осуществляет перехват команд и создаёт первую реакцию на них
    :param message: объект сообщения

    :return: None
    """
    user_id = message.from_user.id
    msg_time = datetime.datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S')
    msg = message.text

    users.set_user(user_id, msg) if not users.is_user(user_id) else users.fresh(user_id, msg)

    text = msg[1:]

    if text == 'start':
        users.well_done(user_id)
        send_answer(user_id, START)

    elif text == 'help':
        users.well_done(user_id)
        send_answer(user_id, COMMAND_LIST)

    elif text == 'history':
        users.well_done(user_id)
        content = make_history(user_id)
        if isinstance(content, list):
            for content_block in content:
                send_answer(user_id, content_block)
        else:
            send_answer(user_id, content)

    elif text in ('lowprice', 'highprice', 'bestdeal'):
        users.set_message_time(user_id, msg_time)
        send_answer(user_id, GIVE_ME_CITY)

    logger.info(f'Обработка команды {text} для пользователя {user_id}')


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
    answer = None

    if user_command in ('/lowprice', '/highprice'):
        if text in ('да', 'нет'):
            if text == 'нет' and step == 5:
                send_answer(user_id, WAIT)
        elif text.isdigit():
            if int(text) in range(2, 11) and step == 6:
                send_answer(user_id, WAIT)
        if user_command == '/lowprice':
            answer = low_price(users, user_id, text)
        else:
            answer = high_price(users, user_id, text)

    elif user_command == '/bestdeal':
        if text in ('да', 'нет'):
            if text == 'нет' and step == 8:
                send_answer(user_id, WAIT)
        elif text.isdigit():
            if int(text) in range(2, 11) and step == 9:
                send_answer(user_id, WAIT)
        answer = best_deal(users, user_id, text)

    response_handler(user_id, answer)


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


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def callback_calendar_handler(call):
    """
    Осуществляет обработку календаря для запроса даты въезда и выезда
    :param call: объект события клавиш календаря

    :return: None
    """
    user_id = call.message.chat.id
    date = users.get_cal_date(user_id)
    msg_id = call.message.message_id
    command = users.get_user_command(user_id)
    answer = None

    result, key = DetailedTelegramCalendar(locale='ru', min_date=date).process(call.data)[:2]

    if not result and key:
        bot.edit_message_text("Выберете дату", user_id, msg_id, reply_markup=key)
    elif result:
        bot.edit_message_text(f"Вы выбрали {result}", user_id, msg_id)

    if isinstance(result, datetime.date):
        if command == '/lowprice':
            answer = low_price(users, user_id, str(result))

        elif command == '/highprice':
            answer = high_price(users, user_id, str(result))

        elif command == '/bestdeal':
            answer = best_deal(users, user_id, str(result))

        step = users.get_step(user_id)
        users.set_cal_date(user_id, result)
        if step == 3:
            send_answer(user_id, answer, date_table=True)
        else:
            send_answer(user_id, answer)


def send_answer(user_id: str, answer: str, k_board: bool = False, date_table: bool = False) -> None:
    """
    Обработчик отправки сообщений.
    Включает и выключает клавиатуру.
    Подключает и отключает календарь в сообщении

    :param user_id: id необходимого пользователя (str)
    :param answer: ответ для пользователя (str)
    :param k_board: необходимо ли вывести клавиатуру? (bool)
    :param date_table: нужно ли прикрепить календарь в сообщении? (bool)
    :return: None
    """

    if k_board:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Да', 'Нет')
        bot.send_message(user_id, answer, reply_markup=keyboard)

    elif date_table:
        calendar = DetailedTelegramCalendar(locale='ru', min_date=datetime.date.today()).build()[0]
        bot.send_message(user_id, answer, reply_markup=calendar)

    else:
        bot.send_message(user_id,
                         answer,
                         reply_markup=ReplyKeyboardRemove(),
                         disable_web_page_preview=True)


def create_photo_group(user_id: str, content: list) -> bool:
    """
    Создание и отправка группы фото пользователю
    :param user_id:
    :param content:
    :return:
    """
    caption = '\n'.join(content[:5])
    links = [InputMediaPhoto(link[:-10] + 's.jpg', caption=caption if i == 0 else '')
             for i, link in enumerate(content[-1])]
    try:
        bot.send_media_group(user_id, links)
        return True
    except Exception as err:
        logger.error(err)
        return False


def response_handler(user_id: str, msg: str) -> None:
    """
    Обработчик последнего шага команд lowprice, highprice, bestdeal

    - Оформляет текстовое сообщение
    - Оформляет фотографии
    - Задаёт старт для ивента с календарем

    :param user_id: id пользователя (str)
    :param msg: сообщение (str)
    :return: None
    """
    max_result = users.get_amount(user_id)
    command = users.get_user_command(user_id)
    msg_date = users.get_message_time(user_id)
    result_count = 0

    if isinstance(msg, list):
        for content_block in msg:
            if len(content_block) == 6:
                status_code = create_photo_group(user_id, content_block)
                result_count += status_code
            else:
                send_answer(user_id, '\n'.join(content_block))
                result_count += 1

            if result_count == max_result:
                break

        send_answer(user_id, RESULT.format(result_count))
        users.well_done(user_id)

        add_to_history(user_id, [command, msg_date, msg[:max_result]])

        logger.success(f'{user_id} получил готовый результат')

    elif msg == DATE_IN:
        send_answer(user_id, msg, date_table=True)

    else:
        cmd = users.get_user_command(user_id)
        step = users.get_step(user_id)
        if (cmd in ('/lowprice', '/highprice') and step == 5) or (cmd == '/bestdeal' and step == 8):
            send_answer(user_id, msg, k_board=True)
        else:
            send_answer(user_id, msg)


def listen() -> None:
    bot.polling(none_stop=True, interval=0)
