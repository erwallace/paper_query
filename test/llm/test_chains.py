from langchain_core.runnables.base import RunnableSequence
from paper_query.llm.chains import setup_chain


def test_setup_chain(prompt, llm):
    chain = setup_chain(
        llm,
        prompt=prompt,
        additional_keys={
            "custom_key": lambda x: x["custom_key"],
        },
    )

    assert isinstance(chain, RunnableSequence)
