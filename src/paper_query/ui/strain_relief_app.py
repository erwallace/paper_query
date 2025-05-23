import sys

import streamlit as st
from langchain_openai import ChatOpenAI
from loguru import logger

from paper_query.chatbots import HybridQueryChatbot
from paper_query.constants import STREAMLIT_CHEAP_MODEL, STREAMLIT_EXPENSIVE_MODEL, assets_dir
from paper_query.ui.components.chat_interface import display_chat_interface
from paper_query.ui.components.text import ABOUT, ABSTRACT

# Configure logger to use DEBUG level
logger.remove()
logger.add(sys.stderr, level="DEBUG")


def strain_relief_chatbot():
    """Chatbot for the StrainRelief paper."""
    st.session_state.chatbot_ready = True

    st.title("The StrainRelief Chatbot")
    chat_tab, about_tab = st.tabs(["Chat", "About"])

    st.sidebar.title("API Configuration")
    # Enter API key in sidebar
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="If you don't have an API key, you can get one from [OpenAI](https://platform.openai.com/api-keys).",
        key="api_input",
    )

    # Initialize model_name in session state if not present
    if "model_name" not in st.session_state:
        st.session_state.model_name = STREAMLIT_CHEAP_MODEL

    # Initialize last_validated_key to track key changes
    if "last_validated_key" not in st.session_state:
        st.session_state.last_validated_key = ""

    # Only validate when key changes or is newly entered
    if openai_api_key and openai_api_key != st.session_state.last_validated_key:
        try:
            chat = ChatOpenAI(openai_api_key=openai_api_key, model=STREAMLIT_CHEAP_MODEL.lower())
            chat.invoke("Hello")
            logger.debug("API key validation successful.")
            st.session_state.model_name = STREAMLIT_EXPENSIVE_MODEL
            st.session_state.last_validated_key = openai_api_key
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            st.sidebar.error("Invalid API key. Please check your OpenAI API key.")
            st.session_state.model_name = STREAMLIT_CHEAP_MODEL
    elif not openai_api_key:
        # Reset to nano model if key is cleared
        st.session_state.model_name = STREAMLIT_CHEAP_MODEL

    # Display current model
    st.sidebar.markdown(f"Using {st.session_state.model_name} model.")

    if "chatbot" not in st.session_state:
        st.session_state.chatbot = HybridQueryChatbot(
            model_name=st.session_state.model_name.lower(),
            model_provider="openai",
            paper_path=str(assets_dir / "strainrelief_preprint.pdf"),
            references_dir=str(assets_dir / "references"),
        )

    with chat_tab:
        if "messages" not in st.session_state:
            st.markdown(ABSTRACT)

            # Show info message only when using nano model
            if st.session_state.model_name == STREAMLIT_CHEAP_MODEL:
                st.info(
                    f"You are currently using {STREAMLIT_CHEAP_MODEL}. Add a valid OpenAI API key "
                    f"to access the more powerful {STREAMLIT_EXPENSIVE_MODEL} model."
                )

        display_chat_interface()

    with about_tab:
        st.markdown(ABOUT)


if __name__ == "__main__":
    strain_relief_chatbot()
