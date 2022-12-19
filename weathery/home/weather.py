import re
from ctypes import Union
from curses import intrflush
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List
from urllib.parse import quote_plus

import numpy as np
import requests


@dataclass
class Weather:
    temperature: float
    wind: str
    day: int
    description: str = ""

    # @property
    # def temperature(self) -> int:
    #     numbers: List[str] = re.findall("[0-9]+", self.temperature_str)
    #     return int(numbers[0])


@dataclass
class Forecast:
    town: str
    forecast: Dict[str, Weather]
    today: Weather


class WeatherAPI:
    api: str = "https://goweather.herokuapp.com/weather/"
    open_meteo_api: str = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, town: str, longitude: float, latitude: float) -> None:
        self.town: str = town
        self.latitude = latitude
        self.longitude = longitude
        self.url: str = f"{self.api}/{quote_plus(town)}"
        self.now: datetime = datetime.now()

    def __day_num_to_name(self, day_number: int) -> str:
        day: datetime = self.now + timedelta(days=day_number)
        return day.strftime("%A")

    def get_forecast(self) -> Forecast:
        # https://open-meteo.com/en/docs#api-documentation
        # https://open-meteo.com/en/docs
        params: Dict[str, Any] = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "hourly": ["temperature_2m", "apparent_temperature", "precipitation"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset"],
            "timezone": "Europe/London",
            "past_days": 1,
        }
        results: dict = requests.get(url=self.open_meteo_api, params=params).json()

        forecast: Dict[str, Weather] = {}

        daily_data = results.get("daily", [])
        times = daily_data.get("time", [])
        temps_min = daily_data.get("temperature_2m_min", [])
        temps_max = daily_data.get("temperature_2m_max", [])

        temps_avg = np.average(np.array([temps_min, temps_max]), axis=0)
        today: Weather
        for index, day in enumerate(times):
            day_weather = Weather(
                temperature=round(temps_avg[index], 2), wind="", day=day
            )
            forecast[day] = day_weather
            if index == params.get("past_days"):
                today = day_weather

        return Forecast(town=self.town, forecast=forecast, today=today)
