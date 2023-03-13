import time
from aiogram import Bot, Dispatcher, types, executor
import logging
import telebot
from message import start_bot_message,new_task_message
from telebot import types

TOKEN = '5649691336:AAHx3ybBR3N8YryxV5CjgIqe67M_XMDCGzA'

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

'''#Основная клавиатура
reply_keyboard = [['/start','/new_task'],
                  ['/check_list','/new_reminder']]
'''


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    user_id = m.from_user.id
    user_full_name = m.from_user.full_name
    markup_inline = types.ReplyKeyboardMarkup()
    #Все виды кнопок при вводе "/start"
    item_list = types.InlineKeyboardButton(text='Список дел', callback_data='/chek_list')
    item_new_reminder = types.InlineKeyboardButton(text='Новая задача', callback_data='/new_task')
    item_new_task = types.InlineKeyboardButton(text='Новое напоминание', callback_data='/new_reminder')

    markup_inline.add(item_list,item_new_task,item_new_reminder)
    bot.send_message(m.chat.id, start_bot_message(user_full_name), reply_markup=markup_inline)

'''
# Функция, обрабатывающая команду /new_task
@bot.message_handler(commands=["new_task"])
def new_task(m, res=False):
    bot.send_message(m.chat.id, new_task_message, reply_markup=markup_inline)


'''
'''
# Функция, обрабатывающая команду /new_reminder
@bot.message_handler(commands=["new_reminder"])
# Функция, обрабатывающая команду /chek_list
@bot.message_handler(commands=["check_list"])'''


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Для начала работы с ботом напишите команду /start')


# Запускаем бота
bot.polling(none_stop=True, interval=0)
