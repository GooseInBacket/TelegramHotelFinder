from py_bot import listen
from loguru import logger
from botrequests.history import create_table

if __name__ == '__main__':
    logger.add('debug.log', format='{time} {level} {message}', level='DEBUG', encoding='UTF-8')
    logger.info('Бот активирован!')
    create_table()
    listen()
