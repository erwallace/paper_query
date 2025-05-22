import pytest
from paper_query.rag.retrieval import (
    base_retriever,
    contextual_compression_retriever,
    setup_retriever,
)


def test_setup_retiever_unsupported_method(vectorstore):
    """Test the setup retriever function with an unsupported method."""
    with pytest.raises(KeyError):
        setup_retriever(vectorstore, method="unsupported_method")


@pytest.mark.parametrize(
    "method, kwargs",
    [
        # There should be a test here for every key in RETREIVER_METHODS
        ("base", {}),
        # ("contextual_compression", {})
    ],
)
def test_setup_retriever(vectorstore, method, kwargs, request):
    """Test the setup retriever function."""
    # Dynamically resolve fixtures in kwargs
    for key, value in kwargs.items():
        if isinstance(value, str):  # Check if the value is a fixture name
            kwargs[key] = request.getfixturevalue(value)

    retriever = setup_retriever(vectorstore, method=method, **kwargs)
    assert retriever


def test_base_retriever(vectorstore):
    """Test the base retriever."""
    retriever = base_retriever(vectorstore)
    assert len(retriever.invoke("hello")) > 0


@pytest.mark.skip(reason="contextual_compression_retriever is not implemented yet.")
def test_contextual_compression_retriever(vectorstore):
    """Test the base retriever."""
    retriever = contextual_compression_retriever(vectorstore)
    assert len(retriever.invoke("hello")) > 0
