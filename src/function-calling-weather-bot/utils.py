import json
import time
from dataclasses import dataclass
from functools import wraps
from typing import Sequence

import requests

from function_calling_weather_bot import ICONS


def get_api(url: str, params: dict, headers: dict = None) -> dict:
    """
    Call either API with the given endpoint and parameters.
    can be wrapped with @retry
    """

    # dont print the kwargs ever as contains API key
    requests_kwargs = {
        "url": url,
        "params": params,
        **({"headers": headers} if headers else {}),
    }

    response = requests.get(**requests_kwargs)
    response.raise_for_status()
    return response.json()


def get_weather(location: str, api_key: str, weather_url: str):
    """
    Get the weather data for a specific location.

    Args:
        location (str): The location to get the weather for.
        api_key (str): The API key for accessing the weather data.

    Raises:
        Exception: If there is an error getting the weather data.

    Returns:
        WeatherData: An object containing the weather information for the location.
    """
    endpoint = weather_url + "/data/2.5/weather"
    params = {"q": location, "appid": api_key}
    response = get_api(url=endpoint, params=params)

    if not response or response["cod"] != 200 or len(response) == 0:
        raise Exception("Error getting weather data")

    return WeatherData(
        description=response["weather"][0]["description"],
        location=response["name"],
        country_code=response["sys"]["country"],
        icon=ICONS.get(response["weather"][0]["icon"], ""),
        temperature=response["main"]["temp"],
    )


@dataclass
class WeatherData:
    """
    Represents weather data for a specific location.
    Probably not helpful to use as saving messages to openai needs dict format

    Attributes:
        description (str): The description of the weather.
        location (str): The location of the weather data.
        country_code (str): The country code of the location.
        icon (str): The icon representing the weather.
        temperature (float): The temperature in Celsius.
    """

    description: str
    location: str
    country_code: str
    icon: str
    temperature: float


def retry(
    max_retries: int = 3,
    delay: int = 1,
    backoff: int = 2,
    exceptions: Sequence[Exception] = (Exception,),
) -> callable:
    """
    Decorator function that allows retrying the decorated function in case of exceptions.

    Args:
        max_retries (int): The maximum number of retries.
        delay (int): The initial delay (in seconds) between retries.
        backoff (int): The backoff factor for increasing the delay between retries.
        exceptions (Sequence[Exception]): The exceptions to catch and retry on.

    Returns:
        callable: The decorated function.

    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_count = 0
            while retry_count < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        raise e
                    sleep_time = delay * (backoff ** (retry_count - 1))
                    time.sleep(sleep_time)

        return wrapper

    return decorator


class Tool:
    specs = {}  # Class-level dictionary to store specs

    @classmethod
    def spec(cls, spec: str | dict) -> callable:
        if isinstance(spec, dict):
            spec = json.dumps(spec, indent=2)

        def decorator(func: callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            # Store the spec with function's name as key
            wrapper._tool_spec = spec
            cls.specs[func.__name__] = spec
            return wrapper

        return decorator

    @classmethod
    def get_all_specs(cls):
        return cls.specs
