"""
paper-query-v2 [model] [provider] [paper] [references]

RAG chatbot for querying a paper and all of its references. The paper is held in context,
references are stored in embeddings.
"""

import argparse

from paper_query.chatbots import PaperQueryPlusChatbot
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
        default="./assets/strainrelief_preprint.pdf",
        help="Path to the paper for the chatbot",
    )
    parser.add_argument(
        "--references",
        type=str,
        default="./assets/references",
        help="Path to the a references directory for use in RAG",
    )
    args = parser.parse_args()

    # Initialize chatbot with paper and run chatbot
    chatbot = PaperQueryPlusChatbot(args.model, args.provider, args.paper, args.references)
    cli_chatbot(chatbot)


if __name__ == "__main__":
    main()
