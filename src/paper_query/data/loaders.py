import os
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.git import GitLoader
from langchain_community.document_loaders.parsers.images import LLMImageBlobParser
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

assets_dir = Path(__file__).resolve().parents[3] / "assets"


def pypdf_loader(file_path: str) -> Document:
    """Function to load text from a PDF file."""
    return PyPDFLoader(file_path, mode="single").load()[0]


def pypdf_loader_w_images(file_path: str, model: str, max_tokens: int = 1024) -> Document:
    """Function to load text from a PDF file with images."""
    # TODO: add other models functionality.
    images_parser = LLMImageBlobParser(model=ChatOpenAI(model=model, max_tokens=max_tokens))
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

    references = []
    for file in os.listdir(refs_dir):
        document = pypdf_loader(os.path.join(refs_dir, file))
        document.metadata["filename"] = file
        references.append(document)
    return references


def code_loader(github_repo_url: str, repo_path: str = str(assets_dir / "code")) -> list[Document]:
    """Function to load code from a git repository."""
    return GitLoader(
        repo_path=repo_path,
        clone_url=github_repo_url,
    ).load()
