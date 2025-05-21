import os
from pathlib import Path

from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

PERSIST_DIRECTORY = str(Path(__file__).resolve().parents[3] / "vectorstore")


def openai_embeddings():
    """Create OpenAI embeddings object."""
    if os.environ.get("OPENAI_API_KEY") is None:
        raise ValueError(
            "OPENAI_API_KEY environment variable must be set to use OpenAI embeddings."
        )
    return OpenAIEmbeddings()


def huggingface_embeddings(model_name="sentence-transformers/all-mpnet-base-v2"):
    """Create HuggingFace embeddings object."""
    return HuggingFaceEmbeddings(model_name=model_name)


EMBEDDING_METHODS = {
    "openai": openai_embeddings,
    "huggingface": huggingface_embeddings,
}


def get_embedding_method(embedding_method: str) -> callable:
    """Retrieve the embedding method based on the provided name."""
    if embedding_method not in EMBEDDING_METHODS:
        raise KeyError(f"Unsupported embedding method: {embedding_method}")

    return EMBEDDING_METHODS[embedding_method]


def create_vectorstore(
    documents: list[Document], embedding_method: str = "openai", **kwargs
) -> Chroma:
    """Create a vectorstore from a list of documents."""
    embeddings = get_embedding_method(embedding_method)(**kwargs)
    return Chroma.from_documents(documents, embeddings)


def setup_vectorstore(
    persist_directory: str = PERSIST_DIRECTORY,
    embedding_method: str = "openai",
    **embedding_kwargs,
) -> Chroma:
    """Set up a vectorstore."""
    if not os.path.exists(persist_directory):
        raise ValueError(f"Persist directory does not exist: {persist_directory}")

    embeddings = get_embedding_method(embedding_method)(**embedding_kwargs)
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        create_collection_if_not_exists=False,
        collection_name="paper-query",
    )
