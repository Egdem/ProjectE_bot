import time
from aiogram import Bot, Dispatcher, types, executor
import logging
import telebot
from message import start_bot_message
from telebot import types

TOKEN = '5649691336:AAHx3ybBR3N8YryxV5CjgIqe67M_XMDCGzA'

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)


# dp = Dispatcher(bot=bot)
'''#Основная клавиатура
reply_keyboard = [['/start','/new_task'],
                  ['/check_list','/new_reminder']]
'''

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    user_id = m.from_user.id
    user_full_name = m.from_user.full_name
    markup_inline = types.InlineKeyboardMarkup()
    item_start = types.InlineKeyboardButton(text='/start', callback_data='/start')
    markup_inline.add(item_start)
    bot.send_message(m.chat.id, start_bot_message(user_full_name),reply_markup=markup_inline)


'''# Функция, обрабатывающая команду /new_task
@bot.message_handler(commands=["new_task"])
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
