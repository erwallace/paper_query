from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

from .models import get_model


def get_chain(
    model_name: str, model_provider: str, prompt: ChatPromptTemplate, additional_keys: dict = {}
) -> RunnableSequence:
    """Get the chain for the chatbot."""
    model = get_model(model_name, model_provider)
    keys = {
        "input": lambda x: x["input"],
        "chat_history": lambda x: x["chat_history"],
        **additional_keys,
    }

    return keys | prompt | model | StrOutputParser()
