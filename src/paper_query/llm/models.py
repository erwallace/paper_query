import os

from langchain.chat_models import init_chat_model


def get_model(model_name: str, model_provider: str):
    """Initialize the chat model."""
    if model_provider == "openai":
        from paper_query.constants import OPENAI_API_KEY

        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    else:
        raise ValueError(f"API key not provided for {model_provider}")

    return init_chat_model(model_name, model_provider=model_provider)
