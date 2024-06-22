import json
import random
from dataclasses import asdict

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall

from function_calling_weather_bot import console
from function_calling_weather_bot.services import Services, WeatherData
from function_calling_weather_bot.utils import retry

CONVO_END = ["exit", "quit", "stop"]


BASE_MESSAGE = {
    "role": "system",
    "content": "You are a helpful assistant for a user who wants to know the weather. You can provide the current weather in a location and an image.",
}


def craft_system_response(tool_response):
    return [
        {
            "role": "system",
            "content": f"Provide only the generated response, no additional info and combine the following information to create an interesting response for the user using the weather description, temperature and location.  We will also provide an image of the weather. {tool_response}",
        }
    ]


class LLMHandler:
    def __init__(self, api_key: str, model_id: str = "gpt-4o"):
        self._api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.model_id = model_id
        self.messages = [BASE_MESSAGE]

    def add_assistant_message(self, content: str) -> None:
        """
        Adds a message from the assistant to the conversation.

        Args:
            content (str): The content of the message.

        Returns:
            None
        """
        self.messages.append({"role": "assistant", "content": content})

    def add_tool_call_to_messages(
        self,
        tool_call: ChatCompletionMessageToolCall,
        tool_response: dict | str,
    ) -> None:
        """
        Adds a tool call and its response to the list of messages.

        Args:
            tool_call (ToolCall): The tool call object.
            tool_response (dict | str): The response from the tool call.

        Returns:
            None
        """
        if isinstance(tool_response, WeatherData):
            tool_response = asdict(tool_response)

        if isinstance(tool_response, dict):
            tool_response = json.dumps(tool_response)
        self.messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": tool_call.function.name,
                "content": tool_response,
            }
        )

    def add_user_input(self, user_input: str) -> None:
        """
        Adds the user's input to the conversation.

        Args:
            user_input (str): The user's input.

        Returns:
            None
        """
        self.messages.append({"role": "user", "content": user_input})

    @retry(max_retries=3)
    def get_response_with_tool(self, messages: list[dict] = None) -> ChatCompletion:
        """
        Retrieves a response using the chat completion API trying to use tools.

        Returns:
            ChatCompletion: The response generated by the chat completion API.
        """
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages or self.messages,
            tools=Services.available_weather_specs,
            tool_choice="auto",
        )
        return response

    @retry(max_retries=3)
    def individual_response(self, messages: list[dict] = None) -> ChatCompletion:
        """
        Generates an individual response using the OpenAI Chat API.

        Args:
            messages (list[dict], optional): A list of message objects representing the conversation.
                Each message object should have a 'role' ('system', 'user', or 'assistant') and 'content' (the message content).
                Defaults to None, in which case the method uses the stored messages.

        Returns:
            ChatCompletion: The generated response from the Chat API.
        """
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages or self.messages,
        )
        return response


class ConversationHandler:
    def __init__(
        self,
        weather_api_key: str = None,
        openai_api_key: str = None,
        bing_api_key: str = None,
    ):
        # initialize external apis
        self.weather_api_key = weather_api_key
        self.openai_api_key = openai_api_key
        self.bing_api_key = bing_api_key
        self.random_image = True
        self.services = Services(weather_api_key=weather_api_key, bing_api_key=bing_api_key)
        self.llm_handler = LLMHandler(openai_api_key)

    def _error_with_tool(self, tool_call: ChatCompletionMessageToolCall) -> str:
        """
        Handles an error with a tool call and returns the content of the system response.

        Args:
            tool_call (ChatCompletionMessageToolCall): The tool call that resulted in an error.

        Returns:
            str: The content of the system response.

        """
        message_content = f"Couldn't get the weather for that location using {tool_call.function.name}."
        messages = [{"role": "system", "content": message_content}]

        system_response = self.llm_handler.individual_response(messages)
        content = system_response.choices[0].message.content
        self.llm_handler.add_assistant_message(content)
        return content

    def get_image_for_weather(self, weather_data: WeatherData) -> str:
        """
        Retrieves an image URL for the given weather data.

        Args:
            weather_data (WeatherData): The weather data object containing information about the weather.

        Returns:
            str: The URL of the image representing the weather.
        """
        query = f"{weather_data.description} in {weather_data.location}, {weather_data.country_code}"
        try:
            image_response = self.services.bing_funcs["get_weather_image"](query=query)
            images = image_response["images"]
            image = random.choice(images) if self.random_image else image_response[0]
            image = image.get("image_url", image.get("thumbnail_url"))
        except Exception:
            image = "Error getting the image."
        return image

    def process_input(self, user_input: str) -> str:
        """
        Processes the user input and generates a response.

        Args:
            user_input (str): The input provided by the user.

        Returns:
            str: The generated response.
        """
        self.llm_handler.add_user_input(user_input)
        response: ChatCompletion = self.llm_handler.get_response_with_tool()

        append_after = []
        if tool_calls := response.choices[0].message.tool_calls:
            # need to add this message no matter what if using tools and crafting the response
            self.llm_handler.messages.append(response.choices[0].message)
            for tool_call in tool_calls:
                tool_kwargs = json.loads(tool_call.function.arguments)
                try:
                    tool_response = self.services.weather_funcs[tool_call.function.name](**tool_kwargs)
                except Exception:
                    return self._error_with_tool(tool_call)

                # add the tool call to messages and then these are combined at end
                self.llm_handler.add_tool_call_to_messages(tool_call, tool_response)

                if isinstance(tool_response, WeatherData):
                    image_url = self.get_image_for_weather(tool_response)
                    append_after.append(image_url)

        # this is similar to second response in their example
        response: ChatCompletion = self.llm_handler.get_response_with_tool()
        content = response.choices[0].message.content
        self.llm_handler.add_assistant_message(content)

        # add the images after, allowing multiple images if multiple tool calls.
        # could potentially combine the image getting and the tool call into one function
        for image_url in append_after:
            content += f"\n {image_url}"
        return content

    def run(self):
        """
        Runs the conversation loop.

        This method starts the conversation loop and prompts the user for input.
        It continues to process the user's input until the conversation is ended
        by typing the value stored in the `CONVO_END` constant.

        Returns:
            None
        """
        console.info(f"Conversation started. Type {CONVO_END} to stop.")

        while True:
            user_input = console.ask("[magenta]You[/magenta] ")
            if user_input.lower() in CONVO_END:
                console.info("Conversation ended")
                break

            response = self.process_input(user_input)
            console.print(f"Bot: {response}")