import os

from langchain.chat_models import init_chat_model
from loguru import logger


def setup_model(model_name: str, model_provider: str, **kwargs):
    """Initialize the chat model."""
    logger.info(f"Initializing {model_name} model from {model_provider}")
    if model_provider == "openai":
        from paper_query.constants import OPENAI_API_KEY

        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    if model_provider == "groq":
        from paper_query.constants import GROQ_API_KEY

        os.environ["GROQ_API_KEY"] = GROQ_API_KEY

    return init_chat_model(model_name, model_provider=model_provider, **kwargs)
