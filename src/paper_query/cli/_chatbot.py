import random
import string

import langgraph
from langchain_core.messages import HumanMessage


def generate_random_string(length=6):
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for i in range(length))


def cli_chatbot(app: langgraph.graph.state.CompiledStateGraph, **kwargs):
    """CLI Chatbot for LangChain.

    Parameters
    ----------
    app: langgraph.graph.state.CompiledStateGraph
        The compiled state graph. Example usage:

        ********************************************
        workflow = StateGraph(state_schema=State)
        workflow.add_edge(START, "model")
        workflow.add_node("model", call_model)

        memory = MemorySaver()
        app = workflow.compile(checkpointer=memory)
        ********************************************

    kwargs: dict
        Additional keyword arguments.
    """
    print("Type 'exit' to quit the chatbot.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        input_messages = [HumanMessage(user_input)]

        print("Bot: ", end="", flush=True)
        for chunk, metadata in app.stream(
            {"messages": input_messages, **kwargs},
            {"configurable": {"thread_id": generate_random_string()}},
            stream_mode="messages",
        ):
            print(chunk.content, end="", flush=True)
        print()
