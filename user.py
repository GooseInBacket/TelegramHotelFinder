class User:
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
        | UNKNOW - диапазон цен (bestdeal)
        | UNKNOW - диапазон расстояний (bestdeal)

        :param user_id: id пользователя (str)
        :param current_command: текущая к выполнению команда (str)
        :return: None
        """
        self.__users[user_id] = {'command': current_command,
                                 'step': 1}

    def remove_user(self, user_id: str):
        del self.__users[user_id]

    def well_done(self, user_id: str):
        self.__users[user_id]['command'] = None
        self.__users[user_id]['step'] = 1

    def step_done(self, user_id: str):
        self.__users[user_id]['step'] += 1

    def set_city(self, user_id: str, city: str):
        self.__users[user_id]['city'] = city

    def set_amount(self, user_id: str, value: str):
        self.__users[user_id]['amount'] = value

    def set_photo(self, user_id: str, value: str):
        self.__users[user_id]['photo'] = value
