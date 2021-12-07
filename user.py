import datetime


class User:
    """
    Класс пользователей чата. Хранит в себе всех пользователей чата,
    которые начали выполнять команды.

    Methods:
         |  get_user_command(user_id) - возвращает текущую выполняющуюся команду у юзера
         |  get_step(user_id) - возвращает текущий шаг выполнения команды
         |  get_city(user_id) - возвращает город, который указал пользователь
         |  get_amount(user_id) - возвращает кол-во результатов, которые необходимо вернуть пользова-
         |  телю
         |  get_photo(user_id) - возвращает ответ пользователя на вопрос "нужно ли ему фото"
         |  get_date_in(user_id) - возвращает дату въезда
         |  get_date_out(user_id) - возвращает дату выезда
         |  get_cal_date(user_id) - возвращает специальную дату для календаря телеграмма
         |  get_low_price(user_id) - возвращает нижний диапазон цен
         |  get_high_price(user_id) - возвращает верхний диапазон цен
         |  get_distance(user_id) - возвращает дистанцию от центра
         |  get_message_time - возвращает время, когда была запрошена команда
         |  get_history - возвращает историю команд пользователя
         |  set_message_time - задать время, когда пришла команда
         |  set_date_in(user_id, date) - задать дату въезда
         |  set_date_out(user_id, date) - задать дату выезда
         |  set_cal_date(user_id, date) - задать специальную дату для календаря телеграмма
         |  set_low_price(user_id, price) - задать нижний диапазон цен
         |  set_high_price(user_id, price) - задать верхний диапазон цен
         |  set_distance(user_id, distance) - задать дистанцию от центра
         |  set_city(user_id, city) - задать город, который необходим пользователю
         |  set_amount(user_id, amount) - задать кол-во результатов
         |  set_photo(user_id, photo) - задать необходимость фото
         |  remove_user(user_id) - удалить пользователя из хранилища
         |  well_done(user_id) - полное, удачное отправление результата пользователю
         |  step_done(user_id) - полное, удачное выполнение шага команды
         |  add_to_history(user_id) - добавляет запись в историю
         |  is_user(user_id) - этот пользователь есть в списке текущих пользователей?
         |  fresh(user_id) - обновить данные для пользователя
    Atr:
        | __users - хранит в себе всех пользователей чата
    """

    def __init__(self):
        self.__users = dict()

    def get_user_command(self, user_id: str):
        result = self.__users.get(user_id)
        if result:
            return result['command']
        return result

    def get_step(self, user_id: str):
        return self.__users[user_id].get('step')

    def get_city(self, user_id: str):
        return self.__users[user_id].get('city')

    def get_amount(self, user_id: str):
        return self.__users[user_id].get('amount')

    def get_photo(self, user_id: str):
        return self.__users[user_id].get('photo')

    def get_date_in(self, user_id: str):
        return self.__users[user_id].get('date_in')

    def get_date_out(self, user_id: str):
        return self.__users[user_id].get('date_out')

    def get_cal_date(self, user_id: str):
        return self.__users[user_id].get('cal_date')

    def get_low_price(self, user_id: str):
        return self.__users[user_id].get('low_price')

    def get_high_price(self, user_id: str):
        return self.__users[user_id].get('high_price')

    def get_distance(self, user_id: str):
        return self.__users[user_id].get('distance')

    def get_message_time(self, user_id: str):
        return self.__users[user_id].get('message_time')

    def get_history(self, user_id: str):
        return self.__users[user_id].get('history')

    def set_message_time(self, user_id: str, time: datetime):
        self.__users[user_id]['message_time'] = time

    def set_date_in(self, user_id: str, date):
        self.__users[user_id]['date_in'] = date

    def set_date_out(self, user_id: str, date):
        self.__users[user_id]['date_out'] = date

    def set_cal_date(self, user_id: str, date):
        self.__users[user_id]['cal_date'] = date

    def set_low_price(self, user_id: str, price: int):
        self.__users[user_id]['low_price'] = price

    def set_high_price(self, user_id: str, price: int):
        self.__users[user_id]['high_price'] = price

    def set_distance(self, user_id: str, distance: float):
        self.__users[user_id]['distance'] = distance

    def set_user(self, user_id: str, current_command: str):
        self.__users[user_id] = {'command': current_command,
                                 'step': 1,
                                 'cal_date': datetime.date.today(),
                                 'history': list()}

    def step_done(self, user_id: str):
        self.__users[user_id]['step'] += 1

    def set_city(self, user_id: str, city: str):
        self.__users[user_id]['city'] = city

    def set_amount(self, user_id: str, value: int):
        self.__users[user_id]['amount'] = value

    def set_photo(self, user_id: str, value: str):
        self.__users[user_id]['photo'] = value

    def remove_user(self, user_id: str):
        del self.__users[user_id]

    def well_done(self, user_id: str):
        self.__users[user_id]['command'] = None
        self.__users[user_id]['step'] = 1

    def add_to_history(self, user_id: str, item):
        self.__users[user_id].get('history').append(item)

    def is_user(self, user_id: str):
        return user_id in self.__users.keys()

    def fresh(self, user_id: str, current_command: str):
        self.__users[user_id]['command'] = current_command
        self.__users[user_id]['step'] = 1
        self.__users[user_id]['cal_date'] = datetime.date.today()
