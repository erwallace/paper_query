import os
import sys
from pathlib import Path

import pytest
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from paper_query import constants
from paper_query.constants import project_dir, test_dir

if sys.platform != "linux":  # Skip for GitHub actions
    from paper_query.constants import GROQ_API_KEY, OPENAI_API_KEY

    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY


@pytest.fixture(autouse=True)
def override_persist_directory():
    """Override PERSIST_DIRECTORY for tests - needed for GitLab CI.

    To be used PERSIST_DIRECTORY must be imported WITHIN the test function."""
    constants.PERSIST_DIRECTORY = str(project_dir / "test" / "assets" / "vectorstore")
    yield


@pytest.fixture
def test_assets_dir() -> Path:
    return test_dir / "assets"


@pytest.fixture
def llm():
    """Fixture to create a small LLM."""
    return init_chat_model(
        model="llama-3.1-8b-instant",
        model_provider="groq",
    )


@pytest.fixture
def prompt() -> ChatPromptTemplate:
    """Fixture to create a prompt template."""
    return ChatPromptTemplate.from_messages(
        [
            ("system", "Here is some context: {context}"),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )


@pytest.fixture
def documents() -> list[Document]:
    """Fixture to create a list of documents."""
    return [
        Document(
            page_content="This is a test document.",
            metadata={"source": "test_source"},
        )
    ]


@pytest.fixture
def embeddings():
    """Fixture to create OpenAI embeddings."""
    return OpenAIEmbeddings()


@pytest.fixture
def vectorstore(documents):
    """Fixture to create an Chroma vectorstore."""
    vectorstore = InMemoryVectorStore(OpenAIEmbeddings())
    vectorstore.add_documents(documents=documents)
    return vectorstore
