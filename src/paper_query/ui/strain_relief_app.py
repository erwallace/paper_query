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
    display_chat_interface()


if __name__ == "__main__":
    strain_relief_chatbot()
