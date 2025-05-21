import os
import shutil
from contextlib import contextmanager
from unittest.mock import patch

import chromadb
import pytest
from paper_query.rag.vectorstore import (
    create_vectorstore,
    get_embedding_method,
    openai_embeddings,
    setup_vectorstore,
)


@contextmanager
def clean_chroma_state():
    """Reset ChromaDB singleton state to prevent test interference.

    This context manager ensures ChromaDB resources are properly cleaned up
    between tests to prevent state leakage across test runs. ChromaDB uses
    singleton patterns for internal state management, which can cause issues
    in test environments where multiple tests interact with ChromaDB instances.

    It performs two cleanup operations:
    1. Calls chromadb.reset_default() to reset the default client
    2. Clears chromadb._DATA_MANAGERS singleton dictionary as a fallback

    Both operations are performed safely with exception handling to ensure
    cleanup attempts don't cause test failures.

    Usage:
        with clean_chroma_state():
            # Code that creates/uses ChromaDB instances

    Returns:
        A context manager that yields control and cleans up after the block completes

    Notes:
        This is especially important when testing code that creates multiple vector
        stores with the same persistence directory across different test functions.
    """
    try:
        yield
    finally:
        # Clean up ChromaDB state
        if hasattr(chromadb, "reset_default"):
            try:
                chromadb.reset_default()
            except Exception as e:
                # Log error instead of ignoring it
                print(f"Warning: ChromaDB reset failed: {e}")

        # Clean up singleton instances as a fallback
        if hasattr(chromadb, "_DATA_MANAGERS"):
            try:
                chromadb._DATA_MANAGERS.clear()  # Using clear() is safer than reassigning
            except Exception as e:
                print(f"Warning: ChromaDB singleton cleanup failed: {e}")


@pytest.fixture
def tmp_db(tmp_path) -> str:
    """Fixture to create a temporary database directory."""
    path = str(tmp_path / "vectorstore" / "docs" / "chroma")
    yield path  # This is the path to the temporary database directory
    # Clean up after test using the context manager
    with clean_chroma_state():
        pass


@pytest.mark.parametrize(
    "embedding_method, expected_exception",
    [
        ("openai", None),
        ("huggingface", None),
        ("invalid_method", KeyError),
    ],
)
def test_get_embedding_method(embedding_method, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            get_embedding_method(embedding_method)
    else:
        method = get_embedding_method(embedding_method)
        assert callable(method), f"Expected a callable, got {type(method)}"


def test_openai_embeddings_no_api_key():
    """Test openai_embeddings raises an error if OPENAI_API_KEY is not set."""
    with patch("os.environ", {}):
        with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable must be set"):
            openai_embeddings()


@pytest.mark.parametrize("embedding_method", ["openai"])
def test_create_vectorstore(embedding_method, documents, tmp_db):
    """Test the creation of a vectorstore."""
    vectorstore = create_vectorstore(
        documents=documents,
        persist_directory=tmp_db,
        embedding_method=embedding_method,
    )
    assert vectorstore is not None, "Vectorstore should not be None"
    assert vectorstore._collection.count() == len(documents), (
        f"Loaded vectorstore count mismatch, "
        f"{len(documents)} expected, "
        f"{vectorstore._collection.count()} found"
    )


@pytest.mark.parametrize("embedding_method", ["openai"])
def test_setup_vectorstore(embedding_method, documents, tmp_db):
    create_dir = os.path.join(tmp_db, "create")
    setup_dir = os.path.join(tmp_db, "setup")
    with clean_chroma_state():
        _vectorstore = create_vectorstore(
            documents=documents,
            embedding_method=embedding_method,
            persist_directory=create_dir,
        )
        assert _vectorstore._collection.count() == len(documents), (
            f"Loaded vectorstore count mismatch, "
            f"{len(documents)} expected, "
            f"{_vectorstore._collection.count()} found"
        )
    # Copy the data to the setup directory
    os.makedirs(os.path.dirname(setup_dir), exist_ok=True)
    # Only copy if the source exists and target doesn't
    if os.path.exists(create_dir) and not os.path.exists(setup_dir):
        shutil.copytree(create_dir, setup_dir)

    # Second operation: Set up a vectorstore from existing files
    with clean_chroma_state():
        vectorstore = setup_vectorstore(
            persist_directory=setup_dir,
            embedding_method=embedding_method,
        )
        assert vectorstore is not None, "Vectorstore should not be None"
        assert vectorstore._collection.count() == len(documents), (
            f"Loaded vectorstore count mismatch, "
            f"{len(documents)} expected, "
            f"{vectorstore._collection.count()} found"
        )
