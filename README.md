# scaled-cognition-takehome

# overview

For this project, I had not used the function calling API so I am not entirely sure what the best practices are for using it.  The example they give (the weather calling one with multiple functions) made it seem like you could chain sequential calls together rather than having to define the logic yourself (e.g. get the weather and from the weather get the image).  Apparently that is not the case, so I ended up including the functionality just as all one function in `ConversationHandler.process_input`.

All of the non-openai APIs are a part of `services.py` and have it setup so it should be easier to test them on their own.  I did this by having the functions pretty independent and just using a partial on them so that I pass the API key during the Services init, initially put everything in classes but then realized that might not be so great or require additional wrapping or instantiating so went with functions and partials.
I initially wrote some tests and they all pass but they mostly were to just get the data working before integrating it into the function calling.  I did not write tests for the function calling because I figured I would have to either mock or stub various parts and seemed like it would eat up a lot of time.

I put some effort into trying to catch various errors and where I thought would be the appropriate level to catch them e.g. catching higher up when I could try and generate a response from the function calling API rather than just failing and returning text.

Although I have not used that [Instructor](https://github.com/jxnl/instructor/) library, I have heard about it and makes me curious how they handle a bunch of the function calling stuff as seems like you need to keep a lot of the data in dicts for it to be used in storing the message, seems like there is a lot of structuring back and forth from dataclasses/pydantic models to dicts if so which seems like it might be a lot of overhead as data grows.

After reading the function calling docs, realized they have you just pass the results back into generate a response, I had written a way to have the model generate a response myself with something like

```python
system_content = craft_system_response(tool_response)
system_response = self.llm_handler.individual_response(system_content)
content = system_response.choices[0].message.content
self.llm_handler.add_assistant_message(content)
```

but I am guessing it is preferred to use the official way of doing it, seemed from my few tests thought that the responses were much more varied and interesting doing it this way so I left the basic part here and then the original methods are still in the code.




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

