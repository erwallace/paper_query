from unittest.mock import MagicMock, patch

import pytest
from paper_query.rag.retrieval import (
    base_retriever,
    contextual_compression_retriever,
    setup_retriever,
)


def test_base_retriever():
    """Test base_retriever returns a retriever with correct search_kwargs."""
    mock_vectorstore = MagicMock()
    mock_retriever = MagicMock()
    mock_vectorstore.as_retriever.return_value = mock_retriever

    result = base_retriever(mock_vectorstore, k=10)
    assert result == mock_retriever
    mock_vectorstore.as_retriever.assert_called_once_with(search_kwargs={"k": 10})


@pytest.mark.skip(reason="Not implemented yet")
def test_contextual_compression_retriever():
    contextual_compression_retriever()


def test_setup_retriever_invalid_method():
    """Test setup_retriever raises ValueError for unsupported methods."""
    mock_vectorstore = MagicMock()

    with pytest.raises(ValueError, match="Unsupported retriever method: invalid"):
        setup_retriever(mock_vectorstore, method="invalid")


def test_setup_retriever_base():
    """Test setup_retriever calls base_retriever for the 'base' method."""
    mock_vectorstore = MagicMock()
    mock_retriever = MagicMock()

    with patch(
        "paper_query.rag.retrieval.base_retriever", return_value=mock_retriever
    ) as mock_base_retriever:
        result = setup_retriever(mock_vectorstore, method="base", k=10)
        assert result == mock_retriever
        mock_base_retriever.assert_called_once_with(mock_vectorstore, k=10)
