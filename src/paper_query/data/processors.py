from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


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


def split_documents(
    documents: list[Document], method: str = "recursive", **kwargs
) -> list[Document]:
    """Split documents using a given method."""
    splitting_methods = {
        "recursive": split_with_recursive_character,
        # add more splitting methods here...
    }

    if method not in splitting_methods:
        raise ValueError(f"Unsupported splitting method: {method}")

    return splitting_methods[method](documents, **kwargs)
