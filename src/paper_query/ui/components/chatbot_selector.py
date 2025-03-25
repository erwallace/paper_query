import streamlit as st

from paper_query.chatbots import (
    BaseChatbot,
    CodeQueryChatbot,
    HybridQueryChatbot,
    PaperQueryChatbot,
    PaperQueryPlusChatbot,
)


def select_chatbot():
    chatbot_options = {
        "Base": BaseChatbot,
        "PaperQuery": PaperQueryChatbot,
        "PaperQuery+": PaperQueryPlusChatbot,
        "CodeQuery": CodeQueryChatbot,
        "HybridQuery": HybridQueryChatbot,
    }

    selected_label = st.sidebar.selectbox(
        "Select Chatbot", list(chatbot_options.keys()), key="chatbot_label"
    )
    selected_chatbot_class = chatbot_options[selected_label]

    return selected_chatbot_class, selected_label
