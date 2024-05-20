from os import getenv
import argparse
from scaled_cognition_takehome.conversation_handler import ConversationHandler


def main(args: argparse.Namespace):
    convo_handler = ConversationHandler(
        weather_api_key=args.weather_api_key,
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
        "--weather-api-key",
        help="Open Weather API key",
        default=getenv("OPEN_WEATHER_API_KEY"),
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    main(args)
