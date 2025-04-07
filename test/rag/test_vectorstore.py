from unittest.mock import MagicMock, patch

import pytest
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from paper_query.rag.vectorstore import (
    create_vectorstore,
    huggingface_embeddings,
    openai_embeddings,
)


def test_openai_embeddings_no_api_key():
    """Test openai_embeddings raises an error if OPENAI_API_KEY is not set."""
    with patch("os.environ", {}):
        with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable must be set"):
            openai_embeddings()


def test_openai_embeddings():
    """Test openai_embeddings creates an OpenAIEmbeddings object."""
    assert isinstance(openai_embeddings(), OpenAIEmbeddings)


def test_huggingface_embeddings():
    """Test huggingface_embeddings creates a HuggingFaceEmbeddings object."""
    assert isinstance(huggingface_embeddings("all-MiniLM-L6-v2"), HuggingFaceEmbeddings)


def test_create_vectorstore_invalid_method():
    """Test create_vectorstore raises an error for unsupported embedding methods."""
    with pytest.raises(ValueError, match="Unsupported embedding method: invalid"):
        create_vectorstore([], embedding_method="invalid")


def test_create_vectorstore_openai():
    """Test create_vectorstore successfully creates a vectorstore with OpenAI embeddings."""
    mock_documents = [MagicMock(spec=Document)]
    mock_embeddings = MagicMock()
    mock_chroma = MagicMock()

    with patch(
        "paper_query.rag.vectorstore.openai_embeddings", return_value=mock_embeddings
    ), patch(
        "paper_query.rag.vectorstore.Chroma.from_documents", return_value=mock_chroma
    ) as mock_from_documents:
        result = create_vectorstore(mock_documents, embedding_method="openai")
        assert result == mock_chroma
        mock_from_documents.assert_called_once_with(mock_documents, mock_embeddings)
