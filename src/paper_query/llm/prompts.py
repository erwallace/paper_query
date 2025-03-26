from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

base_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful assistant. Answer the following questions to the best of your
            ability.""",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

paper_query_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Below is the full text of a research paper. "
            "Reference this content when answering questions:\n\n{paper_text}",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

paper_query_plus_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an AI assistant specialized in analyzing scientific papers and their
            references. Use the provided paper text and relevant information from references
            to answer questions. Always cite your sources at the end of your response using
            the format [source_name].

        Main paper text:
        {paper_text}

        Relevant information from references:
        {relevant_references}
        """,
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

code_query_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "[placeholder]"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

hybrid_query_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "[placeholder]"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)
