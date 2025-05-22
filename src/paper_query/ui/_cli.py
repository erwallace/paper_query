import sys
import time

from loguru import logger

from paper_query.chatbots import BaseChatbot

# Configure logger to use INFO level
logger.remove()
logger.add(sys.stderr, level="INFO")


def cli_chatbot(chatbot: BaseChatbot):
    """Run the CLI chatbot interface."""
    logger.info(r"paper-query-v1: LangChain CLI Chatbot.")
    logger.info("Type 'exit', 'quit', or 'q' to end the conversation.")
    logger.info("Enter your question about the paper:")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit", "q"]:
            print("\nGoodbye!\n")
            break

        print("\nAI: ", end="", flush=True)
        for chunk in chatbot.stream_response(user_input):
            print(chunk, end="", flush=True)
            time.sleep(0.01)
        print()
