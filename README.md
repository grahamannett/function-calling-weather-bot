# scaled-cognition-takehome Project

The project was init with pdm so it is possibly more complex than necessary but I find that it's better to just always use something like pdm to start a project rather than attempting to migrate as it can be a pain.

To setup, you can use `pip install -r requirements && pip install -e .` or `pdm install && pdm sync` should also work.

I have all the keys in an `.env` file but you can pass them in as environment variables or as arguments to the main.py file.

env file will look like:

```
OPENAI_API_KEY=sk-...
OPEN_WEATHER_API_KEY=9...
BING_API_KEY=f...
```

# Overview

For this project, I had not used the function calling API so I am not entirely sure what the best practices are for using it. The example they give (the weather calling one with multiple functions) made it seem like you could chain sequential function calls together rather than having to define the logic yourself (e.g. get the weather and from the weather get the image). Apparently that is not the case, so I ended up including the functionality just as one function in `ConversationHandler.process_input` but probably could rather make it return the image with the weather data and then have the image url be a part of the response.

All of the non-OpenAI services/APIs are a part of `services.py` and it is setup so it should be easier to test them on their own. I did this by having the functions pretty independent and just using a partial on them so that I pass the API key during the `Services.__init__`. I moved everything from originally being in classes when I realized that using class instances would likely result in a less ideal way to call the functions (calling the instances rather than just using a partial on the functions) and would make testing require more setup, but if there was more state or functionality related to these services it would make sense to move them back into classes.
I wrote some tests and they all pass but they mostly were to just get the APIs working before integrating it into the function calling. I did not write tests for the function calling because it seemed like the correct way to do it would require me to either mock or stub various parts of responses and seemed like that would eat up a lot of time.
In terms of the API's, I went with the deprecated API that lets you call by City/City+Country Code/City+State Code/Country Code rather than using the City ID to look up the lat+lon and then call the weather as that seemed slower and adding unnecessary complications but if it was a production system it would be advisable not to use the deprecated API.

I put some effort into trying to catch various errors and where I thought would be the appropriate level to catch them e.g. catching higher up when I could try and generate a response from the function calling API rather than just failing and returning text.

Although I have not used the [Instructor](https://github.com/jxnl/instructor/) library, I have heard about it and makes me curious how they handle a bunch of the function calling as seems like you need to keep a lot of the data in dicts for it to be used in storing the message (i.e. the `"content": tool_response`), seems like there is a lot of structuring back and forth from wrapped dataclasses/pydantic models to dicts and then to strings if so which might be a lot of overhead as data grows (unless they are just subclasses UserDicts?)

After implementing a bit and then re-reading the function calling docs, I realized they have you just pass the results back to generate a response (rather than calling the model independently asking it to generate a unique response with the given data). I had originally implemented a way to have the model generate a response myself with something like:

```python
system_content = craft_system_response(tool_response)
system_response = self.llm_handler.individual_response(system_content)
content = system_response.choices[0].message.content
self.llm_handler.add_assistant_message(content)
```

but I am guessing it is preferred/less error prone to use the official way of doing it (as the model may provide boilerplate like "Sure thing here is the response:\n"), but it seemed from my few comparisons that the crafted responses were much more varied and interesting so doing it this way may be actually more interesting and I left the basic idea here and then the original function is still in the code.


# docs and references
- bing image
  - https://github.com/MicrosoftDocs/bing-docs/blob/main/bing-docs/bing-image-search/how-to/get-images.md
  - sdk
    - first attempt using the sdk gave me a resource not found error, so switched to the REST API which is working
    - https://github.com/MicrosoftDocs/bing-docs/blob/main/bing-docs/bing-image-search/quickstarts/sdk/image-search-client-library-python.md
- openai
  - https://platform.openai.com/docs/api-reference/runs
  - https://platform.openai.com/docs/guides/function-calling
  - https://platform.openai.com/docs/assistants/tools/function-calling/quickstart
  - https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models
- openweather
  - https://openweathermap.org/api/one-call-api
- openweather icons
  - https://github.com/holyCowMp3/openweather-icons-to-emoji

