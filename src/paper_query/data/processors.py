from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from loguru import logger


def split_with_recursive_character(
    documents: list[Document], chunk_size: int = 1000, chunk_overlap: int = 200
) -> list[Document]:
    """Split documents using RecursiveCharacterTextSplitter."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return _split_documents(documents, text_splitter)


def _split_documents(documents: list[Document], splitter) -> list[Document]:
    """Split documents using a given splitter."""
    split_docs = []
    for doc in documents:
        chunks = splitter.split_text(doc.page_content)
        split_docs.extend([Document(page_content=chunk, metadata=doc.metadata) for chunk in chunks])
    return split_docs


SPLITTING_METHODS = {
    "recursive": split_with_recursive_character,
    # add more splitting methods here...
}


def split_documents(
    documents: list[Document], method: str = "recursive", **kwargs
) -> list[Document]:
    """Split documents using a given method."""
    if method not in SPLITTING_METHODS:
        raise ValueError(f"Unsupported splitting method: {method}")

    logger.info(f"Using splitting method: {method}")

    return SPLITTING_METHODS[method](documents, **kwargs)
