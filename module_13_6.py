import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, \
                           InlineKeyboardMarkup, InlineKeyboardButton)

"""Используем функцию load_dotenv() для получения токена из файла .env, включенного в файл .gitignore"""
load_dotenv()
TOKEN = os.getenv("TOKEN")
"""создаем экземпляры классов Bot и Dispatcher с атрибутами bot и storage"""
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
"""создаем экземпляры кнопок reply клавиатуры и самого класса reply клавиатуры с добавлением кнопок в один ряд"""
b_count = KeyboardButton(text='Рассчитать')
b_info = KeyboardButton(text='Информация')
kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(b_count, b_info)
"""создаем экземпляры кнопок inline клавиатуры и самого класса  inline клавиатуры с добавлением кнопок в два ряда"""
b_in_count = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
b_in_formula = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_in = InlineKeyboardMarkup().add(b_in_count)
kb_in.add(b_in_formula)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='formulas')#пользователь нажал inline кнопку Формулы расчета
async def get_formulas(call):
    await call.message.answer('калории (ккал) = 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')

@dp.callback_query_handler(text='calories')#пользователь нажал inline кнопку Рассчитать норму калорий
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await UserState.age.set()  # ожидаем ввод возраста в атрибут UserState.age

@dp.message_handler(commands=['start'])# пользователь набрал команду /start
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью',reply_markup=kb)

@dp.message_handler(text='Рассчитать')#пользователь нажал reply кнопку Рассчитать
async def main_menu(message):
    await message.answer(text='Выберите опцию', reply_markup=kb_in)

@dp.message_handler(text='Информация')# пользователь нажал reply кнопку Информация
async def inform(message):
    await message.answer('Информация о боте')

@dp.message_handler(state=UserState.age)# пользователь ввел возраст
async def set_growth(message, state):
    await state.update_data(txt_age=message.text)# обновляем данные в состоянии age
    await message.answer("Введите свой рoст")
    await UserState.growth.set()#ожидаем ввод роста в аттрибут UserState.growth

@dp.message_handler(state=UserState.growth)# пользователь ввел рост
async def set_weight(message, state):
    await state.update_data(txt_growth=message.text)# обновляем данные в состоянии growth
    await message.answer("Введите свой вес")
    await UserState.weight.set()#ожидаем ввод веса в аттрибут UserState.weight

@dp.message_handler(state=UserState.weight)# пользователь ввел вес
async def set_calories(message, state):
    await state.update_data(txt_weight=message.text)# обновляем данные в состоянии weight
    data = await state.get_data()# присваиваем переменной словарь
    res = 10 * int(data['txt_weight']) + 6.25 * int(data['txt_growth']) - 5 * int(data['txt_age']) + 5#формула Миффлина-Сан Жеора
    await message.answer(f"Ваша норма калорий: {res}")
    await state.finish()#останавливаем машину состояний

@dp.message_handler()#произвольный набор символов пользователем
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)