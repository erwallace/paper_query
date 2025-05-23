import pytest
from paper_query.constants import (
    OPENAI_API_KEY,
    STREAMLIT_CHEAP_MODEL,
    STREAMLIT_EXPENSIVE_MODEL,
    src_dir,
)
from streamlit.testing.v1 import AppTest

TIMEOUT = 20


@pytest.fixture
def app():
    """Returns a streamlit app for testing."""
    app = AppTest.from_file(str(src_dir / "paper_query/ui/strain_relief_app.py"))
    app.run(timeout=10)
    return app


@pytest.mark.app
def test_streamlit_chatbot(app):
    """Tests opening the streamlit app."""
    assert not app.exception


@pytest.mark.app
def test_chatbot_interaction_default_model(app):
    """Tests interacting with the chatbot."""
    app.chat_input("user_input").set_value("hello").run(timeout=TIMEOUT)
    assert not app.exception


@pytest.mark.app
def test_chatbot_interaction_expensive_model(app):
    """Tests interacting with the chatbot."""
    assert app.session_state.model_name == STREAMLIT_CHEAP_MODEL
    app.sidebar.text_input("api_input").set_value(OPENAI_API_KEY).run()
    assert app.session_state.model_name == STREAMLIT_EXPENSIVE_MODEL
    app.chat_input("user_input").set_value("hello").run(timeout=TIMEOUT)
    assert not app.exception


@pytest.mark.app
def test_invalid_api_key(app):
    """Tests interacting with the chatbot."""
    assert app.session_state.model_name == STREAMLIT_CHEAP_MODEL
    app.sidebar.text_input("api_input").set_value("invlaid key").run()
    assert app.session_state.model_name == STREAMLIT_CHEAP_MODEL
    app.chat_input("user_input").set_value("hello").run(timeout=TIMEOUT)
    assert not app.exception
