import pytest
from paper_query.data.processors import (
    _split_documents,
    split_documents,
    split_with_recursive_character,
)


def test_split_with_recursive_character(documents):
    split_docs = split_with_recursive_character(documents, chunk_size=5, chunk_overlap=2)
    assert len(split_docs) == 6


def test__split_documents(documents):
    class Splitter:
        def split_text(self, text):
            return text.split()

    splitter = Splitter()

    split_docs = _split_documents(documents, splitter)
    assert len(split_docs) == 5


def test_split_documents(documents):
    split_docs = split_documents(documents, method="recursive", chunk_size=5, chunk_overlap=2)
    assert len(split_docs) == 6

    with pytest.raises(ValueError):
        split_documents(documents, method="unknown")
