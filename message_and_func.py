from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


def start_bot_message(user_full_name):
    return f'Привет, {user_full_name}! Я бот ProjectE.\n\nProjectE – это чат-бот\n\nБот может:\n├ установить напоминание\n└добавить новую задачу'


new_task_message = 'Введите название новой задачи'


def count_buis(sp):
    count = 0
    for i in range(1, len(sp)):
        count += 1
    return count


def cool_view(sp, chat_id, bot):
    new_sp = []
    for i in range(1, len(sp)):
        new_sp.append(sp[i][0])
    for i in range(len(new_sp)):
        return bot.send_message(chat_id, new_sp[i])
