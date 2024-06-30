from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from enum import Enum


class DateInstance(str, Enum):
    now = "Зараз"
    today = "На сьогодні"
    week = "На тиждень"


class ForecastCallback(CallbackData, prefix="forecast"):
    when: DateInstance
    city: str


def forecast_menu(city: str):
    builder = InlineKeyboardBuilder()
    for date in DateInstance:
        callb_data = ForecastCallback(
            when=date,
            city=city,
        )
        builder.button(
            text=date.value,
            callback_data=callb_data,
        )
    # builder.adjust(3)
    return builder.as_markup()
