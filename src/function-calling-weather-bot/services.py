from dataclasses import dataclass
from functools import partial

import requests

from function_calling_weather_bot import console, services_spec, ICONS

BASE_WEATHER_API = "https://api.openweathermap.org"
BASE_BING_API = "https://api.bing.microsoft.com/v7.0"


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


def _get_api(url: str, params: dict, headers: dict = None) -> dict:
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


def _get_weather(location: str, api_key: str):
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
    endpoint = BASE_WEATHER_API + "/data/2.5/weather"
    params = {"q": location, "appid": api_key}
    response = _get_api(url=endpoint, params=params)

    if not response or response["cod"] != 200 or len(response) == 0:
        raise Exception("Error getting weather data")

    return WeatherData(
        description=response["weather"][0]["description"],
        location=response["name"],
        country_code=response["sys"]["country"],
        icon=ICONS.get(response["weather"][0]["icon"], ""),
        temperature=response["main"]["temp"],
    )


def get_weather_from_city_name(city_name: str, api_key: str):
    """
    Retrieves weather information for a given city name.

    Args:
        city_name (str): The name of the city.
        api_key (str): The API key for accessing the weather data.

    Returns:
        dict: A dictionary containing the weather information for the specified city.
    """
    return _get_weather(location=city_name, api_key=api_key)


def get_weather_from_city_name_and_country(city_name: str, country: str, api_key: str):
    """
    Retrieves the weather information for a given city and country.

    Args:
        city_name (str): The name of the city.
        country (str): The country code.
        api_key (str): The API key for accessing the weather data.

    Returns:
        dict: A dictionary containing the weather information.

    """
    return _get_weather(location=f"{city_name},{country}", api_key=api_key)


def get_weather_from_city_name_and_state_code_and_country_code(
    city_name: str, state_code: str, country_code: str, api_key: str
):
    # api.openweathermap.org/data/2.5/weather?q={city name},{state code},{country code}&appid={API key}
    return _get_weather(f"{city_name},{state_code},{country_code}", api_key)


def get_weather_image(query: str, api_key: str):
    """
    Retrieves weather-related images based on the provided query using the Bing Image Search API.

    Args:
        query (str): The query should be in the format of "{weather condition} in {city}, {country code}".
        api_key (str): The API key for accessing the Bing Image Search API.

    Returns:
        dict: A dictionary containing a list of image URLs and thumbnail URLs.

    Raises:
        Exception: If there is an error getting the image data.
        Exception: If no images are found.

    Example:
        >>> query = "sunny weather in Los Angeles, US"
        >>> api_key = "your_api_key"
        >>> get_weather_image(query, api_key)
        {
            "images": [
                {
                    "image_url": "https://example.com/image1.jpg",
                    "thumbnail_url": "https://example.com/thumbnail1.jpg"
                },
                ...
            ]
        }
    """

    endpoint = BASE_BING_API + "/images/search"
    params = {"q": query, "imageType": "photo"}
    header = {"Ocp-Apim-Subscription-Key": api_key}
    response = _get_api(url=endpoint, params=params, headers=header)

    if not response:
        raise Exception("Error getting image data")

    if len(response_values := response.get("value", [])) == 0:
        raise Exception("No images found")

    image_data = {"images": []}
    for value in response_values:
        image_url = value.get("contentUrl", None)
        thumbnail_url = value.get("thumbnailUrl", None)
        if not image_url and not thumbnail_url:
            console.error("Image URL or Thumbnail URL is None")
            continue

        image_data["images"].append(
            {
                "image_url": image_url,
                "thumbnail_url": thumbnail_url,
            }
        )

    return image_data


class Services:
    """
    A class that provides various services related to weather and images.

    Args:
        weather_api_key (str): The API key for accessing the weather service.
        bing_api_key (str): The API key for accessing the image search service.

    Raises:
        ValueError: If `weather_api_key` or `bing_api_key` is not provided.

    Attributes:
        weather_funcs (dict): A dictionary of weather-related functions.
        bing_funcs (dict): A dictionary of image-related functions.
        available_tools (dict): A dictionary of all available tools, including weather and image functions.
    """

    available_image_specs = services_spec.available_image_specs
    available_weather_specs = services_spec.available_weather_specs

    available_services_specs = available_weather_specs + available_image_specs

    def __init__(self, weather_api_key: str, bing_api_key: str):
        if not weather_api_key:
            raise ValueError("Weather API key is required. Use kwarg or set OPEN_WEATHER_API_KEY")
        if not bing_api_key:
            raise ValueError("Bing API key is required. Use kwarg or set BING_API_KEY")

        self.setup_weather_funcs(weather_api_key)
        self.setup_bing_funcs(bing_api_key)

        self.available_tools = {
            **self.weather_funcs,
            **self.bing_funcs,
        }

    def setup_weather_funcs(self, api_key: str):
        """
        Set up weather-related functions.

        Args:
            api_key (str): The API key for accessing the weather service.
        """
        self.weather_funcs = {
            "get_weather_from_city_name": partial(get_weather_from_city_name, api_key=api_key),
            "get_weather_from_city_name_and_country": partial(get_weather_from_city_name_and_country, api_key=api_key),
            "get_weather_from_city_name_and_state_code_and_country_code": partial(
                get_weather_from_city_name_and_state_code_and_country_code, api_key=api_key
            ),
        }

    def setup_bing_funcs(self, api_key: str):
        """
        Set up image-related functions.

        Args:
            api_key (str): The API key for accessing the image search service.
        """
        self.bing_funcs = {
            "get_weather_image": partial(get_weather_image, api_key=api_key),
        }
