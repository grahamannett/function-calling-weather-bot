import argparse
from os import getenv

from function_calling_weather_bot.conversation_handler import ConversationHandler


def main(args: argparse.Namespace):
    print("using OpenAI API key:", args.openai_api_key)
    convo_handler = ConversationHandler(
        weather_api_key=args.open_weather_api_key,
        bing_api_key=args.bing_api_key,
        openai_api_key=args.openai_api_key,
    )

    convo_handler.run()


def get_args():
    parser = argparse.ArgumentParser(description="Chatbot🫂")

    parser.add_argument(
        "--bing-api-key",
        help="Bing Image Search API key",
        default=getenv("BING_API_KEY"),
    )
    parser.add_argument(
        "--openai-api-key",
        help="OpenAI API key",
        default=getenv("OPENAI_API_KEY"),
    )

    parser.add_argument(
        "--open-weather-api-key",
        help="Open Weather API key",
        default=getenv("OPEN_WEATHER_API_KEY"),
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    main(args)
