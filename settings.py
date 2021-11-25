COMMAND = ['/help', '/lowprice', '/highprice', '/bestdeal', '/history']
LEGEND = [' — вывод самых дешёвых отелей в городе ⬇',
          ' — вывод самых дорогих отелей в городе ⬆',
          ' — вывод отелей, наиболее подходящих по цене и расположению от центра ✅',
          ' — вывод истории поиска отелей 📋']

COMMAND_LIST = 'ℹ Список команд:\n' + '\n'.join([f'{cmd}{lgd}' for cmd, lgd in zip(COMMAND[1:],
                                                                                   LEGEND)])

DONT_UNDERSTAND = '🤷 Не понимаю Вас. Напишите /help'
HI = '👋 Привет! Введите /help, чтобы продолжить.'
START = '👋 Приветствую! Я помогу найти вам самые лучшие цены на отели в Вашем городе.\n' \
        'Чтобы начать работу наберите /help и вам откроются все доступные команды'
WAIT = '🔎 Ищем отели по вашему запрос...'

# КОДЫ УДАЧНЫХ ПОПЫТОК
GIVE_ME_CITY = 'ℹ Введите интересующий вас город\n(Например: Москва, Санкт-Петербург, Иваново)'
GIVE_ME_COUNT = 'ℹ Введите кол-во которое необходимо выввести в результат\n(Целое число. Пример: 10)'
NEED_PHOTO = 'ℹ Нужно ли прикрепить фотографии?\n(Ответ "Да" или "Нет")'
HOW_MUCH = 'ℹ Сколько бы вы хотели получить фотографий для каждого отеля? (от 2 до 10)'

# КОДЫ ОШИБОК
ERR_NOT_INT = '🚫 Это не число.\n🔁 Повторите попытку'
ERR_NOT_STR = '🚫 Город введён не корректно.\n🔁 Повторите попытку'
ERR_BAD_REQ = '🚫 Ошибка запроса. При выполнении запроса вы допустили ошибку в каком-то пункте\n' \
              '🔁 Попробуйте заново: '
ERR_WRONG_ANSWER = '🚫 Необходимо ввести "Да" или "НЕТ"\n🔁 Повторите попытку'
ERR_RANGE = '🚫 Вы не соблюли диапазон.\n🔁 Повторите попытку'
