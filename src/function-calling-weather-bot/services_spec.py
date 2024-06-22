# Could put this on the function itself as docs and grab
from function_calling_weather_bot import console
from function_calling_weather_bot.utils import _get_api, _get_weather, Tool


BASE_WEATHER_API = "https://api.openweathermap.org"
BASE_BING_API = "https://api.bing.microsoft.com/v7.0"

"""
    Retrieves the weather information for a given city.
"""
@Tool.spec({
    "type": "function",
    "function": {
        "name": "get_weather_from_city_name",
        "description": "Get the current weather in a given city",
        "parameters": {
            "type": "object",
            "properties": {
                "city_name": {
                    "type": "string",
                    "description": "The city e.g. Boise",
                },
            },
            "required": ["location"],
        },
    },
})
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


"""
    Retrieves the weather information for a given city and country.
"""
@Tool.spec({
    "type": "function",
    "function": {
        "name": "get_weather_from_city_name_and_country",
        "description": "Get the current weather in a given city and country",
        "parameters": {
            "type": "object",
            "properties": {
                "city_name": {
                    "type": "string",
                    "description": "The city e.g. Boise",
                },
                "country": {
                    "type": "string",
                    "description": "The country as ISO 3166 country code e.g. US",
                },
            },
            "required": ["city_name", "country"],
        },
    },
})
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
    return _get_weather(location=f"{city_name},{country}", api_key=api_key, weather_url=BASE_WEATHER_API)


"""
    Retrieves the weather information for a given city, state code, and country code.
"""
@Tool.spec({
    "type": "function",
    "function": {
        "name": "get_weather_from_city_name_and_state_code_and_country_code",
        "description": "Get the current weather in a given city, state code, and country code",
        "parameters": {
            "type": "object",
            "properties": {
                "city_name": {
                    "type": "string",
                    "description": "The city e.g. Boise",
                },
                "state_code": {
                    "type": "string",
                    "description": "The state code as ISO 3166 state code e.g. ID",
                },
                "country_code": {
                    "type": "string",
                    "description": "The country code as ISO 3166 country code e.g. US",
                },
            },
            "required": ["city_name", "state_code", "country_code"],
        },
    },
})
def get_weather_from_city_name_and_state_code_and_country_code(
    city_name: str, state_code: str, country_code: str, api_key: str
):
    # api.openweathermap.org/data/2.5/weather?q={city name},{state code},{country code}&appid={API key}
    return _get_weather(f"{city_name},{state_code},{country_code}", api_key, weather_url=BASE_WEATHER_API)


"""
    Retrieves weather-related images based on the provided query using the Bing Image Search API.
"""
@Tool.spec({
    "type": "function",
    "function": {
        "name": "get_weather_image",
        "description": "Get the image related to a given weather condition and location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The weather condition and location e.g. 'sunny in Boise, US'",
                },
                "api_key": {
                    "type": "string",
                    "description": "The API key for accessing the image search API",
                },
            },
            "required": ["location", "api_key"],
        },
    },
})
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
