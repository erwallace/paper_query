import pytest
from paper_query import paths
from streamlit.testing.v1 import AppTest

# TODO: max context of 6,000 tokens. Most chatbots require more to hold the paper in context.
MODEL_NAME = "llama-3.1-8b-instant"
MODEL_PROVIDER = "groq"


@pytest.fixture
def app():
    """Returns a streamlit app for testing."""
    app = AppTest.from_file(str(paths.project_dir / "src/paper_query/ui/custom_app.py"))
    app.run()
    return app


@pytest.mark.app
def test_streamlit_chatbot(app):
    """Tests opening the streamlit app."""
    assert not app.exception


@pytest.mark.app
def test_confirm_chatbot(app):
    """Tests activating the chatbot with the default model."""
    app.sidebar.button("confirm_chatbot_button").click().run()
    assert not app.exception


@pytest.mark.app
def test_model_selection(app):
    """Test model selection text input."""
    assert app.sidebar.text_input("model_name_input").value == "gpt-4o"
    app.sidebar.text_input("model_name_input").set_value(MODEL_NAME)
    assert app.sidebar.text_input("model_name_input").value == MODEL_NAME


@pytest.mark.app
def test_model_provider(app):
    """Test model provider text input."""
    assert app.sidebar.text_input("model_provider_input").value == "openai"
    app.sidebar.text_input("model_provider_input").set_value(MODEL_PROVIDER)
    assert app.sidebar.text_input("model_provider_input").value == MODEL_PROVIDER


@pytest.mark.app
def test_chatbot_selection(app):
    """Test chatbot selection."""
    assert app.sidebar.selectbox("chatbot_label").value == "Base"
    app.sidebar.selectbox("chatbot_label").set_value("PaperQuery")
    assert app.sidebar.selectbox("chatbot_label").value == "PaperQuery"


@pytest.mark.app
@pytest.mark.parametrize(
    "chatbot_selected",
    [
        "Base",
        #  "PaperQuery",
        #  "PaperQuery+",
        #  "CodeQuery",
        #  "HybridQuery"
    ],
)
def test_chatbot_interaction(app, chatbot_selected):
    """Tests interacting with the chatbot."""
    app.sidebar.selectbox("chatbot_label").set_value(chatbot_selected)
    app.sidebar.text_input("model_name_input").set_value(MODEL_NAME)
    app.sidebar.text_input("model_provider_input").set_value(MODEL_PROVIDER)
    app.sidebar.button("confirm_chatbot_button").click().run()
    app.chat_input("user_input").set_value("hello").run(timeout=10)
    assert not app.exception
