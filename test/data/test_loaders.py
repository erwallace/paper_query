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
    path = assets_dir / "example_pdf.pdf"
    doc = pypdf_loader(path)
    assert isinstance(doc, Document)


@pytest.mark.slow
def test_pypdf_loader_w_images(assets_dir):
    path = assets_dir / "example_pdf.pdf"
    doc = pypdf_loader_w_images(path, "gpt-4o-mini")
    assert isinstance(doc, Document)


def test_references_loader(assets_dir):
    refs_dir = assets_dir / "references"
    docs = references_loader(refs_dir)
    assert isinstance(docs, list)
    assert isinstance(docs[0], Document)


def test_code_loader(assets_dir):
    docs = code_loader(
        "https://github.com/prescient-design/StrainRelief.git", repo_path=str(assets_dir / "code")
    )
    assert isinstance(docs, list)
    assert isinstance(docs[0], Document)

    shutil.rmtree(assets_dir / "code")
