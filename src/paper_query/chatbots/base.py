import os

from langchain.memory import ConversationBufferMemory
from langchain_core.messages import BaseMessage, HumanMessage

from paper_query.data import pypdf_loader
from paper_query.llm import get_chain
from paper_query.llm.prompts import base_prompt, paper_query_plus_prompt, paper_query_prompt


class BaseChatbot:
    """Base class for chatbots."""

    def __init__(self, model_name, model_provider):
        self.model_name: str = model_name
        self.model_provider: str = model_provider
        self.chat_history: list[BaseMessage] = []
        self.chain = get_chain(model_name, model_provider, prompt=base_prompt)

        # Setup memory
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def process_input(self, user_input: str, chain_kwargs: dict = {}) -> str:
        """Process user input and stream AI response."""
        # Add user message to history before streaming
        self.chat_history.append(HumanMessage(content=user_input))

        # Stream the response
        response_chunks = []

        for chunk in self.chain.stream(
            {"input": user_input, "chat_history": self.chat_history, **chain_kwargs}
        ):
            response_chunks.append(chunk)
            yield chunk

        # After streaming is complete, collect the full response and add to history
        response = "".join(response_chunks)
        self.chat_history.extend([HumanMessage(content=user_input), response])
        return response


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

    def process_input(self, user_input: str) -> str:
        return super().process_input(user_input, chain_kwargs={"paper_text": self.paper_text})


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

    def process_input(self, user_input: str) -> str:
        return super().process_input(
            user_input, chain_kwargs={"paper_text": self.paper_text, "references": self.references}
        )


class CodeQueryChatbot(BaseChatbot):
    """RAG chatbot for querying a code repository. Code is stored in embeddings."""

    pass


class HybridQueryChatbot(BaseChatbot):
    """RAG chatbot for querying a paper, it's code repository and all of it's references."""

    pass
