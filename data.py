import datetime
import math
import sys
from keyboard import DateInstance
from requests import get


def get_weather(city: str, forecast_type: DateInstance, api_key: str) -> dict:
    # TODO: this is simple mock, for testing only
    return {
        "main": {
            "temp": 33.5,
            "humidity": 12,
            "pressure": 5,
        },
        "wind": {
            "speed": 15,
        },
        "weather": [{"main": "Дуже жарко"}],
        "sys": {
            "sunrise": datetime.datetime.now().timestamp(),
            "sunset": datetime.datetime.now().timestamp(),
        },
    }

    base_url = "https://api.openweathermap.org/data/2.5/"
    units = "metric"

    if forecast_type == DateInstance.now:
        url = f"{base_url}weather?q={city}&appid={api_key}&units={units}"
    elif forecast_type == DateInstance.today:
        url = f"{base_url}forecast?q={city}&appid={api_key}&units={units}"
    elif forecast_type == DateInstance.week:
        url = f"{base_url}forecast/daily?q={city}&appid={api_key}&units={units}&cnt=7"

    return get(url).json()


code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Хмарно \U00002601",
    "Drizzle": "Дощ \U00002614",
}


def prepare_answer(city: str, data: dict) -> str:
    main = data.get("main", {})
    current_weather = math.floor(main.get("temp", 0))
    weather_description = data.get("weather", [{}])[0].get("main", "")
    wd = code_to_smile.get(weather_description, "Подивись у вікно \U00001F604")
    humidity = main.get("humidity", 0)
    pressure = main.get("pressure", 0)
    wind_speed = data.get("wind", {}).get("speed", 0)
    sunrise = datetime.datetime.fromtimestamp(data.get("sys", {}).get("sunrise", 0))
    sunset = datetime.datetime.fromtimestamp(data.get("sys", {}).get("sunset", 0))
    return f"""
        Погода в місті: {city}
        Температура: {current_weather}°C {wd}
        Вологість: {humidity}%
        Атмосферний тиск: {pressure}мм.рт.ст.
        Вітер: {wind_speed}km/h
        Схід сонця: {sunrise}
        Захід сонця: {sunset}
        Тривалість світлового дня: {sunset - sunrise}
    """
