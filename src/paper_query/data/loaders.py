from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.parsers.images import LLMImageBlobParser
from langchain_openai import ChatOpenAI


def pypdf_loader(file_path: str):
    return PyPDFLoader(file_path, mode="single").load()[0]


def pypdf_loader_w_images(file_path: str, model: str, max_tokens: int = 1024):
    images_parser = LLMImageBlobParser(model=ChatOpenAI(model=model, max_tokens=max_tokens))
    return PyPDFLoader(
        file_path,
        mode="single",
        images_inner_format="text",
        images_parser=images_parser,
    ).load()[0]
