import pytest
from paper_query.chatbots import (
    BaseChatbot,
    CodeQueryChatbot,
    HybridQueryChatbot,
    PaperQueryChatbot,
    PaperQueryPlusChatbot,
)

MODEL_NAME = "llama-3.1-8b-instant"
MODEL_PROVIDER = "groq"


@pytest.mark.integration
def test_base_chatbot():
    chatbot = BaseChatbot(MODEL_NAME, MODEL_PROVIDER)
    chatbot.stream_response("Hello")


@pytest.mark.integration
def test_paper_query_chatbot(test_assets_dir):
    chatbot = PaperQueryChatbot(
        MODEL_NAME,
        MODEL_PROVIDER,
        test_assets_dir / "example_pdf.pdf",
    )
    chatbot.stream_response("Hello")


@pytest.mark.integration
def test_paper_query_plus_chatbot(test_assets_dir):
    chatbot = PaperQueryPlusChatbot(
        MODEL_NAME,
        MODEL_PROVIDER,
        test_assets_dir / "example_pdf.pdf",
        test_assets_dir / "references",
    )
    chatbot.stream_response("Hello")


@pytest.mark.integration
def test_code_query_chatbot(test_assets_dir):
    chatbot = CodeQueryChatbot(
        MODEL_NAME,
        MODEL_PROVIDER,
        test_assets_dir / "example_pdf.pdf",
    )
    chatbot.stream_response("Hello")


@pytest.mark.integration
def test_hybrid_query_chatbot(test_assets_dir):
    chatbot = HybridQueryChatbot(
        MODEL_NAME,
        MODEL_PROVIDER,
        test_assets_dir / "example_pdf.pdf",
        test_assets_dir / "references",
    )
    chatbot.stream_response("Hello")
