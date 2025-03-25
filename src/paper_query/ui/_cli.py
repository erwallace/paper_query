from paper_query.chatbots import BaseChatbot


def cli_chatbot(chatbot: BaseChatbot):
    """Run the CLI chatbot interface."""
    print(r"paper-query-v1: LangChain CLI Chatbot.")
    print(f"Using the {chatbot.model_name} model from {chatbot.model_provider}.")
    print("Type 'exit', 'quit', or 'q' to end the conversation.")
    print("Enter your question about the paper:")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit", "q"]:
            print("\nGoodbye!\n")
            break

        print("\nAI: ", end="", flush=True)
        for chunk in chatbot.stream_response(user_input):
            print(chunk, end="", flush=True)
            import time

            time.sleep(0.01)
        print()
