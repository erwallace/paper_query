import os
from collections.abc import Generator

from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from paper_query.data.loaders import code_loader, pypdf_loader, references_loader
from paper_query.data.processors import split_documents
from paper_query.llm import get_chain
from paper_query.llm.prompts import (
    base_prompt,
    code_query_prompt,
    paper_query_plus_prompt,
    paper_query_prompt,
)
from paper_query.rag.retrieval import setup_retriever
from paper_query.rag.vectorstore import create_vectorstore


class BaseChatbot:
    """Base class for chatbots."""

    def __init__(self, model_name: str, model_provider: str):
        self.model_name: str = model_name
        self.model_provider: str = model_provider
        self.chat_history: list[BaseMessage] = []
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.chain = get_chain(model_name, model_provider, prompt=base_prompt)

    def stream_response(self, user_input: str, chain_args: dict = {}) -> Generator[str, None, None]:
        """Process user input and stream AI response."""
        # Add user message to history before streaming
        self.chat_history.append(HumanMessage(content=user_input))

        full_response = ""
        for chunk in self.chain.stream(
            {"input": user_input, "chat_history": self.chat_history, **chain_args}
        ):
            full_response += chunk
            yield chunk

        # After streaming is complete, add the full response to chat history
        self.chat_history.append(AIMessage(content=full_response))


class PaperQueryChatbot(BaseChatbot):
    """Chatbot for querying a single paper. The entire paper is held in context."""

    def __init__(self, model_name: str, model_provider: str, paper_path: str):
        super().__init__(model_name, model_provider)
        self.chain = get_chain(
            model_name,
            model_provider,
            prompt=paper_query_prompt,
            additional_keys={"paper_text": lambda x: x["paper_text"]},
        )
        self.paper_text = pypdf_loader(paper_path)

    def stream_response(self, user_input: str) -> Generator[str, None, None]:
        return super().stream_response(user_input, {"paper_text": self.paper_text})


class PaperQueryPlusChatbot(BaseChatbot):
    """RAG chatbot for querying a paper and all of its references. The paper is held in context,
    references are stored in embeddings."""

    def __init__(
        self,
        model_name: str,
        model_provider: str,
        paper_path: str,
        references_dir: str,
        split_method: str = "recursive",
        embedding_method: str = "openai",
        retriever_method: str = "base",
        **kwargs,
    ):
        super().__init__(model_name, model_provider)

        # Load the main paper
        self.paper_text = pypdf_loader(paper_path)

        # Process references for embeddings
        self.references = references_loader(references_dir)
        split_docs = split_documents(
            self.references, method=split_method, **kwargs.get("split_kwargs", {})
        )

        # Create vectorstore and retriever
        self.vectorstore = create_vectorstore(
            split_docs, embedding_method=embedding_method, **kwargs.get("embedding_kwargs", {})
        )
        self.retriever = setup_retriever(
            self.vectorstore, method=retriever_method, **kwargs.get("retriever_kwargs", {})
        )

        # Update the chain
        self.chain = get_chain(
            model_name,
            model_provider,
            prompt=paper_query_plus_prompt,
            additional_keys={
                "paper_text": lambda x: x["paper_text"],
                "relevant_references": lambda x: x["relevant_references"],
            },
        )

    def stream_response(self, user_input: str) -> Generator[str, None, None]:
        # Retrieve relevant reference information
        relevant_docs = self.retriever.invoke(user_input)
        relevant_references = "\n".join(
            [f"From {doc.metadata['filename']}:\n{doc.page_content}" for doc in relevant_docs]
        )

        return super().stream_response(
            user_input, {"paper_text": self.paper_text, "relevant_references": relevant_references}
        )


class CodeQueryChatbot(BaseChatbot):
    """RAG chatbot for querying a code repository. Code is stored in embeddings."""

    def __init__(
        self,
        model_name: str,
        model_provider: str,
        paper_path: str,
        # split_method: str = "recursive",
        embedding_method: str = "openai",
        retriever_method: str = "base",
        **kwargs,
    ):
        super().__init__(model_name, model_provider)

        # Load the main paper
        self.paper_text = pypdf_loader(paper_path)

        # Load code
        self.code = code_loader()

        # Create vectorstore and retriever
        self.vectorstore = create_vectorstore(
            self.code, embedding_method=embedding_method, **kwargs.get("embedding_kwargs", {})
        )
        self.retriever = setup_retriever(
            self.vectorstore, method=retriever_method, **kwargs.get("retriever_kwargs", {})
        )

        # Update the chain
        self.chain = get_chain(
            model_name,
            model_provider,
            prompt=code_query_prompt,
            additional_keys={
                "paper_text": lambda x: x["paper_text"],
                "relevant_code": lambda x: x["relevant_code"],
            },
        )

    def stream_response(self, user_input: str) -> Generator[str, None, None]:
        # Retrieve relevant reference information
        relevant_docs = self.retriever.invoke(user_input)
        relevant_code = "\n".join(
            [f"From {doc.metadata['file_path']}:\n{doc.page_content}" for doc in relevant_docs]
        )

        return super().stream_response(
            user_input, {"paper_text": self.paper_text, "relevant_code": relevant_code}
        )


class HybridQueryChatbot(BaseChatbot):
    """RAG chatbot for querying a paper, it's code repository and all of it's references."""

    def __init__(
        self,
        model_name: str,
        model_provider: str,
        paper_path: str,
        references_dir: str,
        code_dir: str,
    ):
        super().__init__(model_name, model_provider)
        self.chain = get_chain(
            model_name,
            model_provider,
            prompt=paper_query_plus_prompt,
            additional_keys={
                "paper_text": lambda x: x["paper_text"],
                "references": lambda x: x["references"],
                "code_dir": lambda x: x["code_dir"],
            },
        )
        self.paper_text = pypdf_loader(paper_path)

        self.references = []
        for file in os.listdir(references_dir):
            self.references.append(pypdf_loader(os.path.join(references_dir, file)))

        self.code_dir = ""

    def stream_response(self, user_input: str) -> Generator[str, None, None]:
        return super().stream_response(
            user_input,
            {
                "paper_text": self.paper_text,
                "references": self.references,
                "code_dir": self.code_dir,
            },
        )
