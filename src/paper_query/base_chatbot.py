"""
chatbot [model] [provider]

A common or garden CLI chatbot.
"""

import argparse

from paper_query.chatbots import BaseChatbot
from paper_query.ui import cli_chatbot


def main():
    parser = argparse.ArgumentParser(description="LangChain CLI Chatbot")
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o",
        help="Model name to use for the chatbot",
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="openai",
        help="Model provider to use for the chatbot",
    )
    args = parser.parse_args()

    # Initialize chatbot with paper and run chatbot
    chatbot = BaseChatbot(args.model, args.provider)
    cli_chatbot(chatbot)


if __name__ == "__main__":
    main()
