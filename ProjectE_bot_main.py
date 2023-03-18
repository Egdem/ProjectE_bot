import asyncio
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from message import start_bot_message,new_task_message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import time
import sqlite3
from db import BotDB

#Токен нашего бота
TOKEN = '5649691336:AAHx3ybBR3N8YryxV5CjgIqe67M_XMDCGzA'


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

#Хранилище состояний
storage = MemoryStorage()
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher(bot, storage)
# Подключаем базу данных
BotData = BotDB('database.db')


#Создаем класс для машины состояний
class item_types(StatesGroup):
    task = State()
    reminder = State()

# Функция, обрабатывающая команду /start
@dp.message_handler(commands=["start"])
async def start(m: types.Message, res=False):
    #Данные о пользователе

    user_id = m.from_user.id
    user_full_name = m.from_user.full_name
    markup_inline = types.ReplyKeyboardMarkup(resize_keyboard=True)

    #Проверка существования пользователя (при False создается пользовательский id в БД)
    if(not BotData.user_exists(user_id)):
        BotData.add_user(user_id)


    #Все виды кнопок при вводе "/start"
    item_list = types.InlineKeyboardButton(text='/check_list', callback_data='/check_list')
    item_new_reminder = types.InlineKeyboardButton(text='/new_task',callback_data='/new_task')
    item_new_task = types.InlineKeyboardButton(text='/new_reminder', callback_data='/new_reminder')

    #Добавляем кнопки в клавиатуру
    markup_inline.add(item_list,item_new_task,item_new_reminder)

    await bot.send_message(m.chat.id, start_bot_message(user_full_name), reply_markup=markup_inline)


# Обработка команды new_task
@dp.message_handler(commands=["new_task"], state=None)
async def handle_text(m: types.Message):

    # Подключение машины состояний
    await item_types.task.set()
    await m.reply('Напишите в чат, новую задачу')

#Ловим овтвет от пользователя
@dp.message_handler(state=item_types.task)

async def add_task_in_db(m: types.Message, state: FSMContext):
    # Данные о пользователе
    user_id = m.from_user.id
    answer = m.text
    await state.update_data(task=answer)
    user_data= await state.get_data()
    BotData.add_task(user_id, str(user_data))
    await m.reply(f'Задача {str(m.text)} добавлена')
    await state.finish()

@dp.message_handler(state = item_types.task)
async def add_task_in_db(m: types.Message, state = FSMContext):
    # Данные о пользователе
    user_id = m.from_user.id
    answer = m.text
    await state.update_data(task = answer)
    await item_types.task.set()
    data = await state.get_data()
    BotData.add_task(data)
    await m.reply('Вы успешно зарегистрированы')
    await state.reset_state()

# Обработка команды check_list
@dp.message_handler(commands=["check_list"])
async def handle_text(m: types.Message, res=False):

    # Данные о пользователе
    user_id = m.from_user.id

    await bot.send_message(m.chat.id, 'Вот все Ваши задачи: {}'.format(str(BotData.check_list(user_id))))

'''
@dp.message_handler(content_types=["text"])
async def handle_text(m: types.Message, res=False):
    await bot.send_message(m.chat.id, 'Для начала работы с ботом напишите команду /start')
'''
# Запуск процесса поллинга новых апдейтов
if __name__ == "__main__":
    executor.start_polling(dp)