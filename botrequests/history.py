from typing import Union
from settings import CLEAR_HISTORY


def make_history(content: str) -> Union[list, str]:
    """
    Редактирует контент истории команд под корректный вид для сообщения
    :param content: контент истории команд
    :return: Union[list, str]
    """
    result = list()
    if content:
        for item in content:
            command = item[0]
            msg_date = item[1]
            data = '\n\n'.join(['\n'.join([create_string(string)]) for string in item[2]])

            result.append(f'ℹ {command} ({msg_date})ℹ\n\n{data}')
        return result
    return CLEAR_HISTORY


def create_string(string: str) -> str:
    """
    Форматирует строку с отелем в читабельный вид
    :param string: строка с контентом
    :return: str
    """
    return f'🏨 {string[0]}\n|{string[1]}\n|{string[3]}\n|{string[4]}'
