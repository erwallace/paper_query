from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.base import RunnableSequence
from paper_query.llm.chains import get_chain


def test_get_chain():
    # Setup
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "[placeholder]",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    additional_keys = {
        "custom_key": lambda x: x["custom_key"],
    }

    # Call the function
    chain = get_chain(
        model_name="gpt-3.5-turbo",
        model_provider="groq",
        prompt=prompt,
        additional_keys=additional_keys,
    )

    assert isinstance(chain, RunnableSequence)
