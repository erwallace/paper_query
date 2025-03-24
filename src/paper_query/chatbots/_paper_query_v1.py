import argparse

from langchain.chat_models import init_chat_model
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from paper_query.data import pypdf_loader

MODEL_PROVIDER = "openai"
MODEL_NAME = "gpt-4o"

# Initialize model
model = init_chat_model(MODEL_NAME, model_provider=MODEL_PROVIDER)

# Setup memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create prompt with paper context and memory
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Below is the full text of a research paper. ",
            "Reference this content when answering questions:\n\n{paper_text}",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

# Build chain
chain = (
    {
        "input": lambda x: x["input"],
        "paper_text": lambda x: x["paper_text"],
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | model
    | StrOutputParser()
)

# Using the chain with memory management
paper_text = pypdf_loader("./assets/strainrelief_preprint.pdf")


class Chatbot:
    def __init__(self, paper_path: str):
        """Initialize the chatbot with the paper text."""
        self.paper_text = pypdf_loader(paper_path)
        self.chat_history: list[BaseMessage] = []

    def process_input(self, user_input: str) -> str:
        """Process user input and stream AI response."""
        # Add user message to history before streaming
        self.chat_history.append(HumanMessage(content=user_input))

        # Stream the response
        response_chunks = []

        for chunk in chain.stream(
            {"input": user_input, "paper_text": self.paper_text, "chat_history": self.chat_history}
        ):
            response_chunks.append(chunk)
            yield chunk

        # After streaming is complete, collect the full response and add to history
        response = "".join(response_chunks)
        self.chat_history.extend([HumanMessage(content=user_input), response])
        return response


# Define a custom CLI runner since we're not using LangGraph's app structure
def run_cli_chatbot(chatbot: Chatbot):
    """Run the CLI chatbot interface."""
    print("Type 'exit', 'quit', or 'q' to end the conversation.")
    print("Enter your question about the paper:")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break

        print("\nAI: ", end="", flush=True)
        for chunk in chatbot.process_input(user_input):
            print(chunk, end="", flush=True)
            import time

            time.sleep(0.01)


def main():
    parser = argparse.ArgumentParser(description="LangChain CLI Chatbot")
    parser.add_argument(
        "--paper",
        type=str,
        default="./assets/strainrelief_preprint.pdf",
        help="Path to the PDF paper to query",
    )
    args = parser.parse_args()

    print()
    print(r"paper-query-v1: LangChain CLI Chatbot.")
    print(f"Using the {MODEL_NAME} model from {MODEL_PROVIDER}.")
    print()

    # Initialize chatbot with paper and run chatbot
    chatbot = Chatbot(args.paper)
    run_cli_chatbot(chatbot)


if __name__ == "__main__":
    main()
