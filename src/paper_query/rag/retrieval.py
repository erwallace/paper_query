from langchain_community.vectorstores import Chroma


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


def setup_retriever(vectorstore: Chroma, method: str = "base", **kwargs):
    """Set up a retriever."""
    retriever_methods = {
        "base": base_retriever,
        "contextual_compression": contextual_compression_retriever,
    }

    if method not in retriever_methods:
        raise ValueError(f"Unsupported retriever method: {method}")

    return retriever_methods[method](vectorstore, **kwargs)
