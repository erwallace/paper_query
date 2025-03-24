from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.base import RunnableSequence

from .models import get_model
from .prompts import paper_query_prompt


def get_chain(model_name: str, model_provider: str) -> RunnableSequence:
    """Get the chain for the chatbot."""
    model = get_model(model_name, model_provider)
    return (
        {
            "input": lambda x: x["input"],
            "paper_text": lambda x: x["paper_text"],
            "chat_history": lambda x: x["chat_history"],
        }
        | paper_query_prompt
        | model
        | StrOutputParser()
    )
