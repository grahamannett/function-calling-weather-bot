# Could put this on the function itself as docs and grab
available_weather_specs = [
    {
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
    },
    {
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
    },
    {
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
    },
]

available_image_specs = [
    {
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
    },
]
