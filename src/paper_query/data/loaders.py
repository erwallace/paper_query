import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.git import GitLoader
from langchain_community.document_loaders.parsers.images import LLMImageBlobParser
from langchain_core.documents import Document
from loguru import logger

from paper_query.constants import assets_dir
from paper_query.llm import setup_model


def pypdf_loader(file_path: str) -> Document:
    """Function to load text from a PDF file."""
    logger.debug("Loading PDF file using PyPDFLoader")
    return PyPDFLoader(file_path, mode="single").load()[0]


def pypdf_loader_w_images(
    file_path: str, model: str, provider: str, max_tokens: int = 1024
) -> Document:
    """Function to load text from a PDF file with images."""
    logger.debug("Loading PDF file using LLMImageBlobParser")
    images_parser = LLMImageBlobParser(
        model=setup_model(model, provider, max_tokens=max_tokens),
    )
    return PyPDFLoader(
        file_path,
        mode="single",
        images_inner_format="text",
        images_parser=images_parser,
    ).load()[0]


def references_loader(refs_dir: str) -> list[Document]:
    """Function to load references from a directory of PDF files."""
    if not (os.path.exists(refs_dir) and os.path.isdir(refs_dir)):
        raise FileNotFoundError(f"Directory {refs_dir} does not exist.")

    logger.info(f"Loading references from {refs_dir}")

    references = []
    for file in os.listdir(refs_dir):
        if file.endswith(".pdf"):
            document = pypdf_loader(os.path.join(refs_dir, file))
            document.metadata["filename"] = file
            references.append(document)
    return references


def code_loader(github_repo_url: str, repo_path: str = str(assets_dir / "code")) -> list[Document]:
    """Function to load code from a git repository."""
    logger.info(f"Loading code repository from {github_repo_url}")
    return GitLoader(
        repo_path=repo_path,
        clone_url=github_repo_url,
    ).load()
