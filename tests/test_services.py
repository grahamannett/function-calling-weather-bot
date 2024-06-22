import os

import unittest

from function_calling_weather_bot.services import (
    get_weather_from_city_name,
    get_weather_image,
    Services,
)


class TestServices(unittest.TestCase):
    def test_services(self):
        weather_api_key = os.getenv("OPEN_WEATHER_API_KEY")
        bing_api_key = os.getenv("BING_API_KEY")
        services = Services(
            weather_api_key=weather_api_key,
            bing_api_key=bing_api_key,
        )

        weather_func = services.weather_funcs["get_weather_from_city_name"]
        weather = weather_func("Boise")
        assert weather.location == "Boise"


class TestWeather(unittest.TestCase):
    def test_weather_from_city(self):
        weather_api_key = os.getenv("OPEN_WEATHER_API_KEY")
        weather = get_weather_from_city_name("Boise", weather_api_key)
        assert weather.location == "Boise"


class TestBing(unittest.TestCase):
    def test_image_search(self):
        bing_api_key = os.getenv("BING_API_KEY")
        image_data = get_weather_image("clear weather in Boise, US", bing_api_key)
        assert len(image_data["images"]) > 0
