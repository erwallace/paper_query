import os

from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from loguru import logger

from paper_query.constants import PERSIST_DIRECTORY


def openai_embeddings():
    """Create OpenAI embeddings object."""
    if os.environ.get("OPENAI_API_KEY") is None:
        raise ValueError(
            "OPENAI_API_KEY environment variable must be set to use OpenAI embeddings."
        )
    return OpenAIEmbeddings(chunk_size=100)


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

    logger.info(f"Using embedding method: {embedding_method}")

    return EMBEDDING_METHODS[embedding_method]


def create_vectorstore(
    documents: list[Document],
    embedding_method: str = "openai",
    persist_directory: str = PERSIST_DIRECTORY,
    **embedding_kwargs,
) -> Chroma:
    """Create a vectorstore from a list of documents."""
    embedding_function = get_embedding_method(embedding_method)(**embedding_kwargs)
    logger.info(f"Creating vectorstore with {len(documents)} documents.")
    return Chroma.from_documents(documents, embedding_function, persist_directory=persist_directory)


def setup_vectorstore(
    persist_directory: str = PERSIST_DIRECTORY,
    embedding_method: str = "openai",
    **embedding_kwargs,
) -> Chroma:
    """Set up a vectorstore."""
    if not os.path.exists(persist_directory):
        raise ValueError(f"Persist directory does not exist: {persist_directory}")

    embedding_function = get_embedding_method(embedding_method)(**embedding_kwargs)
    logger.info(f"Loading vectorstore from {persist_directory}.")
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function,
        # create_collection_if_not_exists=False,
        # collection_name="paper-query",
    )
