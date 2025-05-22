import streamlit as st
from langchain_openai import ChatOpenAI
from loguru import logger


def setup_sidebar() -> str | None:
    """Set up the sidebar and handle API key configuration.

    Returns:
        The validated OpenAI API key or None if invalid
    """
    st.markdown(
        """
    <style>
        section[data-testid="stSidebar"] {
            width: 60px !important; # Set the width to your desired value
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.sidebar.title("API Configuration")

    # Add API key input in sidebar
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="If you don't have an API key, you can get one from [OpenAI](https://platform.openai.com/api-keys).",
        key="api_input",
    )

    if not openai_api_key:
        return None

    logger.debug(f"OpenAI API key provided: {openai_api_key}")

    # Validate API key
    try:
        chat = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4.1-nano")
        chat.invoke("Hello")
        logger.debug("API key validation successful.")
        return openai_api_key
    except Exception as e:
        logger.error(f"API key validation failed: {e}")
        st.sidebar.error("Invalid API key. Please check your OpenAI API key.")
        return None
