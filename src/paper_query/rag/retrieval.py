from langchain_community.vectorstores import Chroma
from loguru import logger


def base_retriever(vectorstore: Chroma, k: int = 5):
    """Set up a base retriever."""
    return vectorstore.as_retriever(search_kwargs={"k": k})


def contextual_compression_retriever(vectorstore: Chroma, llm, k: int = 5):
    """Set up a retriever with contextual compression."""
    raise NotImplementedError("Contextual compression retriever is not yet implemented.")
    # base_retriever = base_retriever(vectorstore, k)
    # compressor = LLMChainExtractor.from_llm(llm)
    # return ContextualCompressionRetriever(
    #     base_compressor=compressor,
    #     base_retriever=base_retriever
    # )


RETREIVER_METHODS = {
    "base": base_retriever,
    # "contextual_compression": contextual_compression_retriever,
}


def setup_retriever(vectorstore: Chroma, method: str = "base", **kwargs):
    """Set up a retriever."""
    if method not in RETREIVER_METHODS:
        raise KeyError(f"Unsupported retriever method: {method}")

    logger.info(f"Setting up retriever with method: {method}")

    return RETREIVER_METHODS[method](vectorstore, **kwargs)
