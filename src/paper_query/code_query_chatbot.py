"""
code-query [model] [provider] [paper] [code]

RAG chatbot for querying a code repository. Code is stored in embeddings.
"""

import argparse
from pathlib import Path

from paper_query.chatbots import CodeQueryChatbot
from paper_query.ui import cli_chatbot

assets_dir = Path(__file__).resolve().parents[2] / "assets"


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
    parser.add_argument(
        "--code",
        type=str,
        default="https://github.com/prescient-design/StrainRelief.git",
        help="URL for the GutHub repository for the chatbot",
    )
    args = parser.parse_args()

    # Initialize chatbot with paper and run chatbot
    chatbot = CodeQueryChatbot(args.model, args.provider, args.paper, args.code)
    cli_chatbot(chatbot)


if __name__ == "__main__":
    main()
