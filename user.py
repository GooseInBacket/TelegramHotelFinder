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
        """
        Создаёт в словаре одного из пользователей,
        которые в текущий момент работают с ботом

        Значения индексовв данных пользователя:
        | command - текущая команда
        | step - текущий шаг (по-умолчанию 1)
        | city - город (для команд lowprice highprice bestdeal)
        | amount - кол-во результатов (для команд lowprice highprice bestdeal)
        | photo - нужны ли фотографии? (для команд lowprice highprice bestdeal)
        | date_in - дата заезда (для команд lowprice highprice bestdeal)
        | date_out - дата выезда (для команд lowprice highprice bestdeal)
        | UNKNOW - диапазон цен (bestdeal)
        | UNKNOW - диапазон расстояний (bestdeal)

        :param user_id: id пользователя (str)
        :param current_command: текущая к выполнению команда (str)
        :return: None
        """
        self.__users[user_id] = {'command': current_command,
                                 'step': 1,
                                 'cal_date': datetime.date.today()}

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
