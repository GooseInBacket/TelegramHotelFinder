# Telegram-bot для поиска отелей

## Setup

1. Получить API-KEY тут: ( _https://rapidapi.com/apidojo/api/hotels4_ )
2. Зарегистрировать своего бота и получить API-TOKEN: ( _https://core.telegram.org/bots/api_ )
3. Создать в проекте файл **.env** со следующим содержанием:

```
API_TOKEN=<YOU-API-TELEGRAM-TOKEN>
API_KEY=<YOU-API-RAPIDAPI-KEY>
```
4. Установить зависимости проекта
```commandline
pip install -r requirements.txt
```


## Запуск
- Запустить файл main.py открыв его или выполнить команду:
```commandline
python main.py
```


## Краткое описание проекта:
Бот предназначен для поиска отелей в указанном при создании запроса городе с указанием даты въезда и
выезда. Поиск осуществляется вызовом команд:
- **/lowprice** - поиск отелей по возрастанию цены ( **реализовано** ) :white_check_mark:
- **/highprice** - поиск отелей по убыванию цены ( **реализовано** ) :white_check_mark:
- **/bestdeal** - вывод отелей, наиболее подходящих по цене и расположению от центра. ( **в разработке** ) :negative_squared_cross_mark:
- **/hislory** -  вывод истории поиска отелей ( **в разработке** ) :negative_squared_cross_mark:
- **/help** - помощь по командам бота ( **реализовано** ) :white_check_mark:


## Описание команд
### 1. Команда /lowprice
После ввода команды у пользователя запрашивается:
 - Город, где будет проводиться поиск. 
 - Дата заезда в отель 
 - Дата выезда из отеля
 - Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
 - Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
   - При положительном ответе пользователь также вводит количество
необходимых фотографий (не больше заранее определённого
максимума)


### 2. Команда /highprice
После ввода команды у пользователя запрашивается:
 - Город, где будет проводиться поиск. 
 - Дата заезда в отель 
 - Дата выезда из отеля
 - Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
 - Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
   - При положительном ответе пользователь также вводит количество
необходимых фотографий (не больше заранее определённого
максимума)
 

### 3. Команда /bestdeal
После ввода команды у пользователя запрашивается:
 - Город, где будет проводиться поиск. 
 - Диапазон цен.
 - Дата заезда в отель 
 - Дата выезда из отеля
 - Диапазон расстояния, на котором находится отель от центра.
 - Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
 - Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
   - При положительном ответе пользователь также вводит количество
необходимых фотографий (не больше заранее определённого
максимума)


### 4. Команда /history
После ввода команды пользователю выводится история поиска отелей. Сама история
содержит:
- Команду, которую вводил пользователь. 
- Дату и время ввода команды. 
- Отели, которые были найдены.



