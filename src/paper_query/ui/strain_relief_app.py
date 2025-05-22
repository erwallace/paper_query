import sys

import streamlit as st
from loguru import logger

from paper_query.chatbots import HybridQueryChatbot
from paper_query.constants import assets_dir
from paper_query.ui.components.chat_interface import display_chat_interface

# Configure logger to use DEBUG level
logger.remove()
logger.add(sys.stderr, level="DEBUG")


def strain_relief_chatbot():
    """Chatbot for the StrainRelief paper."""
    st.session_state.chatbot_confirmed = True
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = HybridQueryChatbot(
            model_name="gpt-4o",
            model_provider="openai",
            paper_path=str(assets_dir / "strainrelief_preprint.pdf"),
            references_dir=str(assets_dir / "references"),
        )

    st.title("The StrainRelief Chatbot")

    st.markdown(
        "This retrieval augmented generation (RAG) chatbot is designed to answer questions about "
        "the StrainRelief. The chatbot has access to the [paper](https://arxiv.org/abs/2503.13352),"
        " all references, and the code "
        "[repository](https://github.com/prescient-design/StrainRelief)."
    )
    if "messages" not in st.session_state:
        st.markdown(
            ":gray[**Abstract**: Ligand strain energy, the energy difference between the bound and "
            "unbound conformations of a ligand, is an important component of structure-based small "
            "molecule drug design. A large majority of observed ligands in protein-small molecule "
            "co-crystal structures bind in low-strain conformations, making strain energy a useful "
            "filter for structure-based drug design. In this work we present a tool for "
            "calculating ligand strain with a high accuracy. StrainRelief uses a MACE Neural "
            "Network Potential (NNP), trained on a large database of Density Functional Theory "
            "(DFT) calculations to estimate ligand strain of neutral molecules with quantum "
            "accuracy. We show that this tool estimates strain energy differences relative to DFT "
            "to within 1.4 kcal/mol, more accurately than alternative NNPs. These results "
            "highlight the utility of NNPs in drug discovery, and provide a useful tool for drug "
            "discovery teams.]"
        )

    display_chat_interface()


if __name__ == "__main__":
    # Get API keys from Streamlit secrets
    from paper_query import constants

    constants.OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    constants.GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    constants.HUGGINGFACE_API_KEY = st.secrets["HUGGINGFACE_API_KEY"]

    strain_relief_chatbot()
