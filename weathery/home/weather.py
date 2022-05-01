from curses import intrflush
from datetime import datetime, timedelta
import json
from dataclasses import dataclass
from typing import Dict, List
from urllib.parse import quote_plus

import requests
import re


@dataclass
class Weather:
    temperature_str: str
    wind: str
    day: int
    description: str = ""

    @property
    def temperature(self) -> int:
        numbers: List[str] = re.findall("[0-9]+", self.temperature_str)
        return int(numbers[0])


@dataclass
class Forecast:
    town: str
    forecast: Dict[str, Weather]


class WeatherAPI:
    api: str = "https://goweather.herokuapp.com/weather/"

    def __init__(self, town: str) -> None:
        self.town: str = town
        self.url: str = f"{self.api}/{quote_plus(town)}"
        self.now: datetime = datetime.now()

    def __day_num_to_name(self, day_number: int) -> str:
        day: datetime = self.now + timedelta(days=day_number)
        return day.strftime("%A")

    def get_forecast(self) -> Forecast:
        weather: dict = requests.get(self.url).json()
        forecast: Dict[str, Weather] = {}
        day = 0
        forecast[self.__day_num_to_name(day)] = Weather(
            temperature_str=weather.get("temperature", ""),
            wind=weather.get("wind", ""),
            description=weather.get("description", ""),
            day=day,
        )

        for forecast_day in weather.get("forecast", []):
            day = forecast_day.get("day")
            forecast[self.__day_num_to_name(int(day))] = Weather(
                temperature_str=forecast_day.get("temperature", ""),
                wind=forecast_day.get("wind", ""),
                description=forecast_day.get("description", ""),
                day=day,
            )

        return Forecast(town=self.town, forecast=forecast)
