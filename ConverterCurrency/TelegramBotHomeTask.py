# pip3 install pyTelegramBotAPI
# pip3 install requests
# Бот возвращает цену на определённое количество валюты (евро, доллар или рубль).
# При написании бота необходимо использовать библиотеку pytelegrambotapi.
# Человек должен отправить сообщение боту в виде <имя валюты, цену которой он хочет узнать> <имя валюты, в которой надо узнать цену 
# первой валюты> <количество первой валюты>.
# При вводе команды /start или /help пользователю выводятся инструкции по применению бота.
# При вводе команды /values должна выводиться информация о всех доступных валютах в читаемом виде.
# Для получения курса валют необходимо использовать API и отправлять к нему запросы с помощью библиотеки Requests.
# Для парсинга полученных ответов использовать библиотеку JSON.
# При ошибке пользователя (например, введена неправильная или несуществующая валюта или неправильно введено число) вызывать собственно 
# написанное исключение APIException с текстом пояснения ошибки.
# Текст любой ошибки с указанием типа ошибки должен отправляться пользователю в сообщения.
# Для отправки запросов к API описать класс со статическим методом get_price(), который принимает три аргумента и возвращает нужную сумму 
# в валюте:
# - имя валюты, цену на которую надо узнать, — base;
# - имя валюты, цену в которой надо узнать, — quote; 
# - количество переводимой валюты — amount.
# Токен Telegram-бота хранить в специальном конфиге (можно использовать .py файл).
# Все классы спрятать в файле extensions.py.


import telebot
from config import keys, TOKEN
from utils import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)

# r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR')
# print(r.content)

# # Обрабатываются все сообщения.
# @bot.message_handler()
# def handle_start_help(message: telebot.types.Message):
#     bot.send_message(message.chat.id, f'Hello, {message.chat.first_name}')

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующием формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \n \
Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise APIException('Слишком много параметров!')
        elif len(values) < 3:
            raise APIException('Слишком мало параметров!')
            
        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
            
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)
    
# Чтобы запустить бота, нужно воспользоваться методом polling.
bot.polling()

