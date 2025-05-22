from .base_chatbot import main as base_chatbot
from .code_query_chatbot import main as code_query_chatbot
from .paper_query_chatbot import main as paper_query_chatbot
from .paper_query_plus_chatbot import main as paper_query_plus_chatbot

__all__ = [
    "base_chatbot",
    "paper_query_chatbot",
    "paper_query_plus_chatbot",
    "code_query_chatbot",
]
