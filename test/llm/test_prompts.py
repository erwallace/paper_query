import pytest
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from paper_query.llm.prompts import (
    base_prompt,
    code_query_prompt,
    hybrid_query_prompt,
    paper_query_plus_prompt,
    paper_query_prompt,
)


@pytest.mark.parametrize(
    "prompt, expected_placeholders",
    [
        (base_prompt, ["chat_history"]),
        (paper_query_prompt, ["chat_history"]),
        (paper_query_plus_prompt, ["chat_history"]),
        (code_query_prompt, ["chat_history"]),
        (hybrid_query_prompt, ["chat_history"]),
    ],
)
def test_prompt_placeholders(prompt, expected_placeholders):
    """Test that all prompts contain the expected placeholders."""
    assert isinstance(prompt, ChatPromptTemplate)

    placeholders = [
        msg.variable_name for msg in prompt.messages if isinstance(msg, MessagesPlaceholder)
    ]
    assert placeholders == expected_placeholders
