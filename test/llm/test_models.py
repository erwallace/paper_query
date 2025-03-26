import pytest
from paper_query.llm import get_model


def test_get_model_with_invalid_provider():
    with pytest.raises(ValueError, match="API key not provided for invalid_provider"):
        get_model("gpt-3.5-turbo", "invalid_provider")
