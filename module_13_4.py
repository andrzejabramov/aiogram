import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands='start')# пользователь набрал команду /start
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью')

@dp.message_handler(text='Calories')# пользователь ввел текст 'Calories'
async def set_age(message):
    await message.answer("Введите свой возраст")
    await UserState.age.set()#ожидаем ввод возраста в атрибут UserState.age

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