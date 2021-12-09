from typing import Union
from settings import CLEAR_HISTORY
from contextlib import closing
import sqlite3


def make_history(user_id: str) -> Union[str, list]:
    """
    Редактирует контент истории команд под корректный вид для сообщения
    :param user_id: Пользователь, чью истторию нужно вернуть
    :return:
    """
    with closing(sqlite3.connect('history.db')) as con:
        cursor = con.cursor()
        in_db = cursor.execute("SELECT * FROM users_data WHERE user_id=?", (user_id,)).fetchone()
        if in_db:
            data = cursor.execute(
                'SELECT * FROM users_data WHERE user_id={}'.format(user_id)).fetchall()
            return ['ℹ {} ({})ℹ\n\n{}'.format(*item[2:]) for item in data]
        else:
            return CLEAR_HISTORY


def add_to_history(user_id: str, content: list) -> None:
    """Добавляет запись истории в БД"""
    to_save = [create_content(user_id, content)]

    with closing(sqlite3.connect('history.db')) as con:
        cursor = con.cursor()
        cursor.executemany("""INSERT INTO users_data(
        user_id, 
        command, 
        msg_date, 
        data) VALUES(?, ?, ?, ?);""", to_save)
        con.commit()


def create_table():
    with closing(sqlite3.connect('history.db')) as con:
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users_data(
        id INT PRIMaRY KEY,
        user_id TEXT,
        command TEXT, 
        msg_date TEXT,
        data TEXT);
        """)


def create_string(string: str) -> str:
    """
    Форматирует строку с отелем в читабельный вид

    0 - название отеля
    1 - адрес
    3 - цена
    4 - ссылка

    :param string: строка с контентом
    :return: str
    """
    return f'🏨 {string[0]}\n|{string[1]}\n|{string[3]}\n|{string[4]}'


def create_content(user_id, content: list) -> tuple:
    """Формирует из контента тьюпл, который можно будет сохранить в БД"""
    command = content[0]
    msg_date = content[1]
    data = '\n\n'.join(['\n'.join([create_string(string)]) for string in content[2]])
    return user_id, command, msg_date, data
