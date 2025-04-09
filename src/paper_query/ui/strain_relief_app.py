from pathlib import Path

import streamlit as st

from paper_query.chatbots import PaperQueryChatbot
from paper_query.ui.components.chat_interface import display_chat_interface

assets_dir = Path(__file__).resolve().parents[3] / "assets"


def strain_relief_chatbot():
    """Chatbot for the StrainRelief paper."""
    st.session_state.chatbot_confirmed = True
    st.session_state.chatbot = PaperQueryChatbot(
        model_name="gpt-4o",
        model_provider="openai",
        paper_path=str(assets_dir / "strainrelief_preprint.pdf"),
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
    strain_relief_chatbot()
