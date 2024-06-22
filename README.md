# Weather Photo Bot Project/Takehome

Note: After finishing, changed to using the @Tool.spec decorator to make the function calling/spec easier to define and use but did not test it.

## Setup

This project was initialized with PDM, which provides a robust package management system. To set up the project, you have two options:

1. Using pip:
   - `pip install -r requirements && pip install -e .`
2. Using PDM:
   - `pdm install && pdm sync`

**External dependencies:** The main external dependencies are `requests`, `openai`, and `rich`. Rich is used for colorized console output, enhancing readability during development.

## Environment Setup

Store your API keys in a `.env` file or pass them as environment variables. The required keys are:

```bash
OPENAI_API_KEY=sk-...
OPEN_WEATHER_API_KEY=9...
BING_API_KEY=f...
```

You can source the `.env` file using `source .env` or set the environment variables directly in your terminal.

## Project Structure

The project follows a standard Python package structure:

- `src/`: Contains the main source code
- `tests/`: Includes test files
- `main.py`: Entry point of the application
- `pyproject.toml`: Project configuration file
- `README.md`: This file, providing project overview and setup instructions

## Overview

### API Integration

This project integrates multiple APIs to create a weather photo bot:

1. **OpenAI API**: Used for natural language processing and function calling.
2. **OpenWeather API**: Provides weather data for specified locations.
3. **Bing Image Search API**: Retrieves relevant images based on weather conditions.

### Implementation Details

- The `ConversationHandler.process_input` method combines the functionality of weather data retrieval and image search into a single function call.
- Non-OpenAI services are implemented in `services.py`, designed for easy testing and modularity.
- The project uses the deprecated OpenWeather API that allows city name lookup, chosen for simplicity in this demonstration. For production use, it's advisable to use the current API with geocoding.

### Error Handling

Effort has been made to catch various errors at appropriate levels, especially in the function calling API to generate responses even in case of partial failures.

### Testing

Basic tests have been implemented for the API services. However, comprehensive tests for the function calling feature were not included due to time constraints and the complexity of mocking responses.

## Potential Further Improvements

1. Consider using the [Instructor](https://github.com/jxnl/instructor/) library for more efficient function calling and data handling.
2. Implement more varied and interesting response generation by crafting custom system prompts.
3. Expand test coverage, especially for the function calling features.
4. Migrate to the current OpenWeather API with geocoding for production use.


# Docs/References
- bing image
  - https://github.com/MicrosoftDocs/bing-docs/blob/main/bing-docs/bing-image-search/how-to/get-images.md
  - https://github.com/MicrosoftDocs/bing-docs/blob/main/bing-docs/bing-image-search/quickstarts/sdk/image-search-client-library-python.md
    - SDK gave me resource not found error, -> using REST API instead
- openai
  - https://platform.openai.com/docs/api-reference/runs
  - https://platform.openai.com/docs/guides/function-calling
  - https://platform.openai.com/docs/assistants/tools/function-calling/quickstart
  - https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models
- openweather
  - https://openweathermap.org/api/one-call-api
- openweather icons
  - https://github.com/holyCowMp3/openweather-icons-to-emoji



# Original Info

```
Weather Photo Bot
Scaled Cognition Engineering Take-Home Specification
Please implement a simple chatbot that can respond to utterances semantically similar to: Show me what the weather in Vancouver looks like right now.
To respond, the chatbot will:
1. Get the current weather in Vancouver (or whichever location is specified).
2. Run an image search corresponding to that weather (e.g. cloudy day in Vancouver) 3. Deliver a response to the user, including at least one URL of the images matching that weather.
Example Transcript
(You do not need to match the exact utterances.)
Hi! How can I help you today?
What does the weather look like today in Cambridge, MA?
Of course; I’ve pulled that up for you: https://example.com
How about the weather in Seoul?
I’ve found that as well: https://example.com
… (continuing until the user kills the program with a KeyboardInterrupt)
Guidelines
● Your implementation should make use of the following:
  ○ OpenAI Function Calling API
  ○ Bing Image Search API
  ○ OpenWeatherMap weather and geocoding APIs (free under 1000 requests/day)
● Name the entry point of your application main.py. It should be runnable as python main.py. The command-line interface should be simple and intuitive.
● Provide all API keys as command-line parameters. Don’t hard-code and leak API keys!
● List any external packages you choose to use in a requirements.txt file. ● Display meaningful messages in case of errors.
● Use good coding practices, and be prepared to discuss decisions you made about your design and implementation. Include a README with an overview of your implementation and decision-making.
● We are interested in the proficiency, cleanliness, and creativity of your approach. This is of course a contrived environment, but the goal is to write something as close to production code as possible.
```