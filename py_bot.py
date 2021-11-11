import telebot

TOKEN = '2117954320:AAFYlULULdCNneSqk9O3K-DeJiiZp8HwYdQ'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_message(message) -> None:
    msg = message.text.lower()
    if msg == '/hello-world':
        bot.send_message(message.from_user.id, 'Привет, мир!')
    elif msg == 'привет':
        bot.send_message(message.from_user.id, 'Привет, чем я могу тебе помочь?')
    elif msg == '/help':
        bot.send_message(message.from_user.id, 'Напиши "Привет"')
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю. Напиши "/help"')
    print(f'[NM] {message.from_user.id}', message.text, sep=' >>> ')


def listen() -> None:
    """
    Старт прослушки чата
    """
    bot.polling(none_stop=True, interval=0)
