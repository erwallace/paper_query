import pytest
from paper_query.llm import setup_model


@pytest.mark.parametrize(
    "model_name, model_provider",
    [
        ("gpt-3.5-turbo", "groq"),
        ("gpt-3.5-turbo", "openai"),
    ],
)
def test_get_model_with_valid_provider(model_name, model_provider):
    setup_model(model_name, model_provider)
