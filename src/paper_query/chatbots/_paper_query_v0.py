"""From LangChain: Build a Chatbot tutorial (see tutorials/langchain_chatbot_v3.ipynb)

Run from the command line via: paper-query-v0 [job=pirate]
"""

import argparse
import os
from collections.abc import Sequence
from typing import Annotated

from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from paper_query.ui import cli_chatbot

MODEL_PROVIDER = "openai"
MODEL_NAME = "gpt-4o-mini"

if MODEL_PROVIDER == "openai":
    from paper_query.constants import OPENAI_API_KEY

    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
else:
    raise ValueError(f"API key not provided for {MODEL_PROVIDER}")

# Define the chat model
model = init_chat_model(MODEL_NAME, model_provider=MODEL_PROVIDER)


# Define the state schema
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    job: str


# Define the message trimmer
trimmer = trim_messages(
    max_tokens=65,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

# Define the prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You talk like a {job}. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


# Define the model call function
def call_model(state: State):
    trimmed_messages = trimmer.invoke(state["messages"])
    prompt = prompt_template.invoke({"messages": trimmed_messages, "job": state["job"]})
    response = model.invoke(prompt)
    return {"messages": [response]}


# Define the workflow
workflow = StateGraph(state_schema=State)
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Compile the workflow with memory saver
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


# Define the main function
def main():
    parser = argparse.ArgumentParser(description="LangChain CLI Chatbot")
    parser.add_argument("--job", type=str, default="pirate", help="The job role to simulate")
    args = parser.parse_args()

    print()
    print(r"paper-query-v0: LangChain CLI Chatbot. Talk like a {job}.")
    print(f"Using the {MODEL_NAME} model from {MODEL_PROVIDER}.")
    print()
    cli_chatbot(app, job=args.job)


if __name__ == "__main__":
    main()
