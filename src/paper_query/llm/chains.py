from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence


def setup_chain(
    model: BaseLanguageModel, prompt: ChatPromptTemplate, additional_keys: dict = {}
) -> RunnableSequence:
    """Setup the chain for the chatbot."""
    keys = {
        "input": lambda x: x["input"],
        "chat_history": lambda x: x["chat_history"],
        **additional_keys,
    }

    return keys | prompt | model | StrOutputParser()
