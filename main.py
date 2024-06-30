from os import getenv
import sys
import logging
import math
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from data import get_weather, prepare_answer
from keyboard import DateInstance, ForecastCallback, forecast_menu

import datetime
import asyncio
import requests
from dotenv import load_dotenv, dotenv_values

print(dotenv_values(".env"))
load_dotenv(".env")
API_KEY = getenv("API_KEY", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
print(BOT_TOKEN)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class City(StatesGroup):
    name = State()


@dp.message(Command("start"))
async def start_message(message: Message, state: FSMContext):
    await message.answer(
        "Привіт. Я бот котрий допоможе тобі дізнатися прогноз погоди в будь якому місті.\n"
        "Щоб дізнатися погоду, необхідно насамперед зазначити місто.\n"
        "Введіть назву міста: "
    )
    await state.set_state(City.name)


@dp.message(City.name)
async def process_name(message: Message, state: FSMContext):
    data = await state.update_data(name=message.text)
    await state.clear()
    await message.answer(
        text=f"Назва міста: {data.get('name')}",
        reply_markup=forecast_menu(data.get("name", "")),
    )


@dp.callback_query(ForecastCallback.filter())
async def forecast_processing(query: CallbackQuery, callback_data: ForecastCallback):
    weather = get_weather(
        city=callback_data.city,
        forecast_type=callback_data.when,
        api_key=API_KEY,
    )
    text = prepare_answer(city=callback_data.city, data=weather)
    await query.message.answer(f"{text}\nГарного дня!")


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
