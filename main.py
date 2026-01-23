import telebot
from bot_token import TOKEN
import queue
import threading
import time
from datetime import datetime
from googletrans import Translator
import asyncio
from telebot import types
queue_m = {}
queue_time_chat = {}
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

async def translate_text(message):
        translator = Translator()
        # Асинхронный вызов перевода
        result = await translator.translate(message.text, dest="en")
        bot.send_message(message.chat.id,result.text)# Теперь .text доступен

@bot.message_handler(content_types=['text'])
def echo(message):
    asyncio.run(translate_text(message))

bot.infinity_polling()

















