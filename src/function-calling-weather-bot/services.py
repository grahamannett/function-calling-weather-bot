from functools import partial

from function_calling_weather_bot import services_spec, utils


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
            "get_weather_from_city_name": partial(utils.get_weather_from_city_name, api_key=api_key),
            "get_weather_from_city_name_and_country": partial(
                utils.get_weather_from_city_name_and_country, api_key=api_key
            ),
            "get_weather_from_city_name_and_state_code_and_country_code": partial(
                utils.get_weather_from_city_name_and_state_code_and_country_code, api_key=api_key
            ),
        }

    def setup_bing_funcs(self, api_key: str):
        """
        Set up image-related functions.

        Args:
            api_key (str): The API key for accessing the image search service.
        """
        self.bing_funcs = {
            "get_weather_image": partial(utils.get_weather_image, api_key=api_key),
        }
