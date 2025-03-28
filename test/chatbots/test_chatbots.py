from pathlib import Path

import pytest
from paper_query.chatbots import (
    BaseChatbot,
    CodeQueryChatbot,
    HybridQueryChatbot,
    PaperQueryChatbot,
    PaperQueryPlusChatbot,
)

assets_dir = Path(__file__).resolve().parents[1] / "assets"
MODEL_NAME = "llama-3.1-8b-instant"
MODEL_PROVIDER = "groq"


@pytest.mark.integration
def test_base_chatbot():
    chatbot = BaseChatbot(MODEL_NAME, MODEL_PROVIDER)
    chatbot.stream_response("Hello")


@pytest.mark.integration
def test_paper_query_chatbot():
    chatbot = PaperQueryChatbot(
        MODEL_NAME,
        MODEL_PROVIDER,
        assets_dir / "example_pdf.pdf",
    )
    chatbot.stream_response("Hello")


@pytest.mark.integration
def test_paper_query_plus_chatbot():
    chatbot = PaperQueryPlusChatbot(
        MODEL_NAME,
        MODEL_PROVIDER,
        assets_dir / "example_pdf.pdf",
        assets_dir / "references",
    )
    chatbot.stream_response("Hello")


@pytest.mark.integration
def test_code_query_chatbot():
    chatbot = CodeQueryChatbot(
        MODEL_NAME,
        MODEL_PROVIDER,
        assets_dir / "example_pdf.pdf",
    )
    chatbot.stream_response("Hello")


@pytest.mark.skip("Function not yet implemented")
@pytest.mark.integration
def test_hybrid_query_chatbot():
    chatbot = HybridQueryChatbot(
        MODEL_NAME,
        MODEL_PROVIDER,
        assets_dir / "example_pdf.pdf",
        assets_dir / "references",
    )
    chatbot.stream_response("Hello")
