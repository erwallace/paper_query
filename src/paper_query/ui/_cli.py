from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph

from paper_query.utils import random_string


def cli_chatbot(app: StateGraph, **kwargs):
    """CLI Chatbot for LangChain.

    Parameters
    ----------
    app: (Compiled)StateGraph
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
            {"configurable": {"thread_id": random_string()}},
            stream_mode="messages",
        ):
            print(chunk.content, end="", flush=True)
        print()
