import sys

import streamlit as st
from loguru import logger

from paper_query.chatbots import HybridQueryChatbot
from paper_query.constants import STREAMLIT_CHEAP_MODEL, STREAMLIT_EXPENSIVE_MODEL, assets_dir
from paper_query.ui.components.chat_interface import display_chat_interface
from paper_query.ui.components.text import ABOUT, ABSTRACT
from paper_query.ui.components.validate_key import validate_openai_api_key

# Configure logger to use DEBUG level
logger.remove()
logger.add(sys.stderr, level="DEBUG")


def initialize_session_state():
    """Initialize session state variables."""
    if "chatbot_ready" not in st.session_state:
        st.session_state.chatbot_ready = True

    if "chatbot" not in st.session_state:
        st.session_state.chatbot = None

    if "model_name" not in st.session_state:
        st.session_state.model_name = STREAMLIT_CHEAP_MODEL


def strain_relief_chatbot():
    """Chatbot for the StrainRelief paper."""
    initialize_session_state()

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

    validate_openai_api_key(openai_api_key)
    # Display current model
    st.sidebar.markdown(f"Using **{st.session_state.model_name}** model.")

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

        else:
            logger.warning(st.session_state.messages)

        display_chat_interface()

    with about_tab:
        st.markdown(ABOUT)


if __name__ == "__main__":
    strain_relief_chatbot()
