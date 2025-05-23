import sys

import streamlit as st
from langchain_openai import ChatOpenAI
from loguru import logger

from paper_query.chatbots import HybridQueryChatbot
from paper_query.constants import assets_dir
from paper_query.ui.components.chat_interface import display_chat_interface

# Configure logger to use DEBUG level
logger.remove()
logger.add(sys.stderr, level="DEBUG")

CHEAP_MODEL = "GPT-4.1-nano"
EXPENSIVE_MODEL = "GPT-4.1"


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
        st.session_state.model_name = CHEAP_MODEL

    # Initialize last_validated_key to track key changes
    if "last_validated_key" not in st.session_state:
        st.session_state.last_validated_key = ""

    # Only validate when key changes or is newly entered
    if openai_api_key and openai_api_key != st.session_state.last_validated_key:
        try:
            chat = ChatOpenAI(openai_api_key=openai_api_key, model=CHEAP_MODEL.lower())
            chat.invoke("Hello")
            logger.debug("API key validation successful.")
            st.session_state.model_name = EXPENSIVE_MODEL
            st.session_state.last_validated_key = openai_api_key
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            st.sidebar.error("Invalid API key. Please check your OpenAI API key.")
            st.session_state.model_name = CHEAP_MODEL
    elif not openai_api_key:
        # Reset to nano model if key is cleared
        st.session_state.model_name = CHEAP_MODEL

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
            st.markdown(
                ":gray[**Abstract**: Ligand strain energy, the energy difference between the "
                "bound and unbound conformations of a ligand, is an important component of "
                "structure-based small molecule drug design. A large majority of observed "
                "ligands in protein-small molecule co-crystal structures bind in low-strain "
                "conformations, making strain energy a useful filter for structure-based drug "
                "design. In this work we present a tool for calculating ligand strain with a "
                "high accuracy. StrainRelief uses a MACE Neural Network Potential (NNP), "
                "trained on a large database of Density Functional Theory (DFT) calculations "
                "to estimate ligand strain of neutral molecules with quantum accuracy. We show "
                "that this tool estimates strain energy differences relative to DFT to within "
                "1.4 kcal/mol, more accurately than alternative NNPs. These results highlight "
                "the utility of NNPs in drug discovery, and provide a useful tool for drug "
                "discovery teams.]"
            )

            # Show info message only when using nano model
            if st.session_state.model_name == CHEAP_MODEL:
                st.info(
                    f"You are currently using {CHEAP_MODEL}. Add a valid OpenAI API key to access "
                    f"the more powerful {EXPENSIVE_MODEL} model."
                )

        display_chat_interface()

    with about_tab:
        st.markdown(
            f"""
        **StrainRelief is a tool for calculating ligand strain energy with quantum mechanical
        accuracy**.

        ##### What is ligand strain energy?
        Ligand strain energy is the energy difference between the bound and unbound conformations
        of a ligand. It's an important component in structure-based small molecule drug design.

        ##### How does StrainRelief work?
        StrainRelief uses a MACE Neural Network Potential (NNP) trained on a large database of
        Density Functional Theory (DFT) calculations to estimate ligand strain of neutral molecules
        with quantum accuracy.

        ##### About this chatbot
        This chatbot is built using a hybrid retrieval and cached augmented generation (RAG/CAG)
        approach:

        1. The full StrainRelief [paper](https://arxiv.org/abs/2503.13352) is loaded and cached
        in the context window for all queries
        2. Reference papers cited in StrainRelief are embedded and available for retrieval
        3. The StrainRelief code [repository](https://github.com/prescient-design/StrainRelief)
        is embedded and available for retrieval

        The chatbot is currently has a naive modular framework. When you ask a question, the
        system:
        - Retrieves relevant information from the references and code
        - Combines this with the full paper context
        - Uses the LLM to generate a response based on all available information

        The chatbot uses the following components:
        - **LLM**: {EXPENSIVE_MODEL} from OpenAI for generating responses
        - **Embedding**: OpenAI embeddings for vector search
        - **Vector Database**: ChromaDB for storing and retrieving embedded documents

        Feel free to ask about the StrainRelief methodology, implementation details, or
        how to use the tool for drug discovery applications.
        """
        )


if __name__ == "__main__":
    strain_relief_chatbot()
