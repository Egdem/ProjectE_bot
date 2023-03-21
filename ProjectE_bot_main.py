import asyncio
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from message_and_func import start_bot_message, new_task_message, cool_view
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import time
import sqlite3
from db import BotDB

# Токен нашего бота
TOKEN = '5649691336:AAHx3ybBR3N8YryxV5CjgIqe67M_XMDCGzA'

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Хранилище состояний
storage = MemoryStorage()
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher(bot, storage=MemoryStorage())
# Подключаем базу данных
BotData = BotDB('database.db')


# Создаем класс для машины состояний
class item_types(StatesGroup):
    task = State()
    remove_task = State()


# Функция, обрабатывающая команду /start
@dp.message_handler(commands=["start"])
async def start(m: types.Message, res=False):
    # Данные о пользователе
    user_id = m.from_user.id
    user_full_name = m.from_user.full_name
    markup_inline = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Проверка существования пользователя (при False создается пользовательский id в БД)
    if (not BotData.user_exists(user_id)):
        BotData.add_user(user_id)

    # Все виды кнопок при вводе "/start"
    item_list = types.InlineKeyboardButton(text='/check_list', callback_data='/check_list')
    item_new_reminder = types.InlineKeyboardButton(text='/new_task', callback_data='/new_task')
    item_new_task = types.InlineKeyboardButton(text='/remove_task', callback_data='/remove_task')

    # Добавляем кнопки в клавиатуру
    markup_inline.add(item_list, item_new_task, item_new_reminder)
    await bot.send_message(m.chat.id, start_bot_message(user_full_name), reply_markup=markup_inline)


# Обработка команды new_task
@dp.message_handler(commands=["new_task"], state=None)
async def handle_text(m: types.Message):
    # Подключение машины состояний
    await item_types.task.set()
    await m.reply('Напишите в чат, новую задачу')


# Ловим овтвет от пользователя
@dp.message_handler(content_types=['text'], state=item_types.task)
async def add_task_in_db(m: types.Message, state: FSMContext):
    # Данные о пользователе
    user_id = m.from_user.id
    answer = m.text
    BotData.add_task(user_id, str(answer))
    await bot.send_message(m.chat.id, 'Задача добавлена')
    await state.finish()


# Обработка команды remove_task
@dp.message_handler(commands=["remove_task"], state=None)
async def handle_remove_text(m: types.Message):
    # Подключение машины состояний
    await item_types.remove_task.set()
    await m.reply('Напишите задачу, которую вы хотите удалить')


# Ловим овтвет от пользователя
@dp.message_handler(content_types=['text'], state=item_types.remove_task)
async def remove_task_in_db(m: types.Message, state: FSMContext):
    # Данные о пользователе
    user_id = m.from_user.id
    answer = m.text
    BotData.remove_task(user_id, str(answer))
    await bot.send_message(m.chat.id, 'Задача удалена')
    await state.finish()


# Обработка команды check_list
@dp.message_handler(commands=["check_list"])
async def handle_text(message: types.Message, res=False):
    # Данные о пользователе
    user_id = message.from_user.id
    ch_list = BotData.check_list(user_id)
    await bot.send_message(message.chat.id, 'Вот все Ваши задачи:')
    new_sp = []
    inline_del = types.InlineKeyboardButton('❌ Удалить ❌', callback_data='del_message')  # доделать конпку
    inline_state = types.InlineKeyboardMarkup().add(inline_del)
    for i in range(1, len(ch_list)):
        new_sp.append(ch_list[i][0])
    for i in range(len(new_sp)):
        await bot.send_message(message.chat.id, new_sp[i], reply_markup=inline_state)
    new_sp = []


@dp.callback_query_handler(lambda c: c.data == 'del_message')
async def process_callback_button1(callback_query: types.CallbackQuery):
    cb_mes = callback_query.message.text
    user_id = callback_query.from_user.id
    BotData.remove_task(user_id, str(cb_mes))
    await bot.send_message(callback_query.message.chat.id, '✅ Задача удалена')


# Обработка не предусмотренных команд и сообщений
@dp.message_handler(content_types=["text"])
async def handle_text(m: types.Message, res=False):
    await bot.send_message(m.chat.id, 'Для начала работы с ботом напишите команду /start')


# Запуск процесса поллинга новых апдейтов
if __name__ == "__main__":
    executor.start_polling(dp)
