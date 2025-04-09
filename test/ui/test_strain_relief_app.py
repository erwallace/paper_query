import pytest
from paper_query import paths
from streamlit.testing.v1 import AppTest

# TODO: max context of 6,000 tokens. Most chatbots require more to hold the paper in context.
MODEL_NAME = "llama-3.1-8b-instant"
MODEL_PROVIDER = "groq"


@pytest.fixture
def app():
    """Returns a streamlit app for testing."""
    app = AppTest.from_file(str(paths.project_dir / "src/paper_query/ui/strain_relief_app.py"))
    app.run()
    return app


@pytest.mark.app
def test_streamlit_chatbot(app):
    """Tests opening the streamlit app."""
    assert not app.exception


@pytest.mark.app
def test_chatbot_interaction(app):
    """Tests interacting with the chatbot."""
    app.chat_input("user_input").set_value("hello").run(timeout=10)
    assert not app.exception
