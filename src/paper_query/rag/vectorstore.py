import os

from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings


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


def create_vectorstore(
    documents: list[Document], embedding_method: str = "openai", **kwargs
) -> Chroma:
    """Create a vectorstore from a list of documents."""
    embedding_methods = {
        "openai": openai_embeddings,
        "huggingface": huggingface_embeddings,
    }

    if embedding_method not in embedding_methods:
        raise ValueError(f"Unsupported embedding method: {embedding_method}")

    embeddings = embedding_methods[embedding_method](**kwargs)
    return Chroma.from_documents(documents, embeddings)
