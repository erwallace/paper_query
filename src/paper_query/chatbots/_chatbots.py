import os
from collections.abc import Generator

from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from paper_query.data import pypdf_loader
from paper_query.llm import get_chain
from paper_query.llm.prompts import base_prompt, paper_query_plus_prompt, paper_query_prompt


class BaseChatbot:
    """Base class for chatbots."""

    def __init__(self, model_name, model_provider):
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

    def stream_response(self, user_input: str) -> str:
        return super().stream_response(user_input, {"paper_text": self.paper_text})


class PaperQueryPlusChatbot(BaseChatbot):
    """RAG chatbot for querying a paper and all of its references. The paper is held in context,
    references are stored in embeddings."""

    def __init__(self, model_name: str, model_provider: str, paper_path: str, refernces_dir: str):
        super().__init__(model_name, model_provider)
        self.chain = get_chain(
            model_name,
            model_provider,
            prompt=paper_query_plus_prompt,
            additional_keys={
                "paper_text": lambda x: x["paper_text"],
                "references": lambda x: x["references"],
            },
        )
        self.paper_text = pypdf_loader(paper_path)

        self.references = []
        for file in os.listdir(refernces_dir):
            self.references.append(pypdf_loader(os.path.join(refernces_dir, file)))

    def stream_response(self, user_input: str) -> str:
        return super().stream_response(
            user_input, {"paper_text": self.paper_text, "references": self.references}
        )


class CodeQueryChatbot(BaseChatbot):
    """RAG chatbot for querying a code repository. Code is stored in embeddings."""

    def __init__(self, model_name: str, model_provider: str, code_dir: str):
        super().__init__(model_name, model_provider)
        self.chain = get_chain(
            model_name,
            model_provider,
            prompt=paper_query_plus_prompt,
            additional_keys={
                "code_dir": lambda x: x["code_dir"],
            },
        )
        self.code_dir = ""

    def stream_response(self, user_input: str) -> str:
        return super().stream_response(user_input, {"code_dir": self.code_dir})


class HybridQueryChatbot(BaseChatbot):
    """RAG chatbot for querying a paper, it's code repository and all of it's references."""

    def __init__(
        self,
        model_name: str,
        model_provider: str,
        paper_path: str,
        refernces_dir: str,
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
        for file in os.listdir(refernces_dir):
            self.references.append(pypdf_loader(os.path.join(refernces_dir, file)))

        self.code_dir = ""

    def stream_response(self, user_input: str) -> str:
        return super().stream_response(
            user_input,
            {
                "paper_text": self.paper_text,
                "references": self.references,
                "code_dir": self.code_dir,
            },
        )
