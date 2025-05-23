import pytest
import streamlit as st
from paper_query.constants import OPENAI_API_KEY, STREAMLIT_CHEAP_MODEL, STREAMLIT_EXPENSIVE_MODEL
from paper_query.ui.components.validate_key import validate_openai_api_key


@pytest.mark.app
@pytest.mark.parametrize(
    "api_key, last_key, model_name",
    [
        (OPENAI_API_KEY, OPENAI_API_KEY, STREAMLIT_EXPENSIVE_MODEL),
        (None, None, STREAMLIT_CHEAP_MODEL),
        ("invalid_key", None, STREAMLIT_CHEAP_MODEL),
    ],
)
def test_validate_openai_api_key_correct(api_key, last_key, model_name):
    """Test the OpenAI API key validation."""
    st.session_state.last_validated_key = True

    validate_openai_api_key(api_key)
    assert st.session_state.last_validated_key == last_key
    assert st.session_state.model_name == model_name
