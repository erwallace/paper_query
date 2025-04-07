import shutil

import pytest
from langchain_core.documents.base import Document
from paper_query.data.loaders import (
    code_loader,
    pypdf_loader,
    pypdf_loader_w_images,
    references_loader,
)


def test_pypdf_loader(assets_dir):
    """Test the pypdf_loader function."""
    path = assets_dir / "example_pdf.pdf"
    doc = pypdf_loader(path)
    assert isinstance(doc, Document)


@pytest.mark.slow
def test_pypdf_loader_w_images(assets_dir):
    """Test the pypdf_loader_w_images function."""
    path = assets_dir / "example_pdf.pdf"
    # TODO: change to free model
    doc = pypdf_loader_w_images(path, "gpt-4o-mini", "openai")
    assert isinstance(doc, Document)


def test_references_loader(assets_dir):
    """Test the references_loader function."""
    refs_dir = assets_dir / "references"
    docs = references_loader(refs_dir)
    assert isinstance(docs, list)
    assert isinstance(docs[0], Document)


def test_references_loader_only_pdf(assets_dir):
    """Test the references_loader function."""
    refs_dir = assets_dir / "references"
    docs = references_loader(refs_dir)
    assert len(docs) == 1


def test_code_loader(assets_dir):
    """Test the code_loader function."""
    docs = code_loader(
        "https://github.com/prescient-design/StrainRelief.git", repo_path=str(assets_dir / "code")
    )
    assert isinstance(docs, list)
    assert isinstance(docs[0], Document)

    shutil.rmtree(assets_dir / "code")
