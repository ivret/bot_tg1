import telebot
from bot_token import TOKEN
import queue
import threading
import time
from datetime import datetime
from googletrans import Translator
import asyncio

queue_m = {}
queue_time_chat = {}
translator = Translator()
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,f'''
Добрый день! начнем работу?
Доступные команды:
    /start - приветствие
    /help - помощь
    /get_info - информация о пользователе 
    /installation_time - установка времени удаления сообщений''')

def info(message):
    if message.text == 'имя':
        bot.send_message(message.chat.id,message.from_user.first_name)
    elif message.text == 'фамилия':
        bot.send_message(message.chat.id, message.from_user.last_name)
    elif message.text == 'имя пользователя':
        bot.send_message(message.chat.id, message.from_user.username)
    else:
        bot.send_message(message.chat.id, 'я такого не знаю')

@bot.message_handler(commands=['get_info'])
def get_info(message):
    send = bot.send_message(message.chat.id,""" 
    Что именно вы хотите узнать?
        имя - Ваше имя
        фамилия - ваша фамилия
        имя пользователя - ваш ник""")
    bot.register_next_step_handler(send,info)



@bot.message_handler(commands=['help'])
def help(message):
    send = bot.send_message(message.chat.id,'''
    По поводу неполадок пишите в тг - @vlloboda''')

def installation_time(message):
    if message.text == '2 сек':
        queue_time_chat[message.chat.id] =2
        bot.send_message(message.chat.id,"время установлено")
    elif message.text == '5 сек':
        queue_time_chat[message.chat.id] = 5
        bot.send_message(message.chat.id, "время установлено")
    elif message.text == '5 мин':
        queue_time_chat[message.chat.id] = 300
        bot.send_message(message.chat.id, "время установлено")
    elif message.text == '1 час':
        queue_time_chat[message.chat.id] = 3600
        bot.send_message(message.chat.id, "время установлено")
    else:
        bot.send_message(message.chat.id, 'я такого не знаю')

@bot.message_handler(commands=['installation_time'])
def get_time(message):
    send = bot.send_message(message.chat.id,"""
    Какое время установить для удаления сообщений?
        2 сек
        5 сек
        5 мин
        1 час""")
    bot.register_next_step_handler(send,installation_time)
async def translate_text(message):
    translator = Translator()
    # Асинхронный вызов перевода
    result = await translator.translate("что делать цуам", dest="en")
    print(result.text)  # Теперь .text доступен

def schedule_deletion(message):
    chat = message.chat.id
    word = message.message_id
    timestamp = datetime.now().timestamp()
    if chat not in queue_m:
        queue_m[chat] = {}
    queue_m[chat][word] = timestamp


def check_and_delete_old_messages():
    current_timestamp = datetime.now().timestamp()
    for chat_id in list(queue_m.keys()):
        if chat_id not in queue_time_chat:
            break
        time_del = queue_time_chat[chat_id]
        to_delete = []
        items = list(queue_m[chat_id].items())
        # Проверяем все сообщения в этом чате
        for msg_id, msg_timestamp in items:
            if current_timestamp - msg_timestamp >=  time_del:
                try:
                    bot.delete_message(chat_id, msg_id)
                    print(f"Удалено {msg_id}")
                    to_delete.append(msg_id)
                except Exception as e:
                    print(f"Ошибка при удалении {msg_id}: {e}")

        # Удаляем отмеченные сообщения (после итерации)
        for msg_id in to_delete:
            if msg_id in queue_m[chat_id]:
                del queue_m[chat_id][msg_id]

        # Если в чате не осталось сообщений — удаляем чат из очереди
        if not queue_m[chat_id]:  # Если словарь пуст
            del queue_m[chat_id]  # Удаляем ключ из основного словаря


def background_checker():
        while True:
            check_and_delete_old_messages()
            time.sleep(1)

thread = threading.Thread(target=background_checker, daemon=True)
thread.start()

@bot.message_handler(content_types=['text', 'photo', 'sticker'])
def echo(message):
    if message.chat.id not in queue_time_chat:
        return   # время не установлено — ничего не делаем

    schedule_deletion(message)

bot.infinity_polling()

















