"""
paper-query-v1 [model] [provider] [paper]

A chatbot for querying a single paper. The entire paper is held in context.
"""

import argparse

from paper_query import assets_dir
from paper_query.chatbots import PaperQueryChatbot
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
    parser.add_argument(
        "--paper",
        type=str,
        default=str(assets_dir / "strainrelief_preprint.pdf"),
        help="Path to the paper for the chatbot",
    )
    args = parser.parse_args()

    # Initialize chatbot with paper and run chatbot
    chatbot = PaperQueryChatbot(args.model, args.provider, args.paper)
    # chatbot = BaseChatbot(MODEL_NAME, MODEL_PROVIDER)
    cli_chatbot(chatbot)


if __name__ == "__main__":
    main()
