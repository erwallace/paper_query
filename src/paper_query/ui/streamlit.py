import streamlit as st

from paper_query.ui.components.chat_interface import display_chat_interface
from paper_query.ui.components.chatbot_selector import select_chatbot
from paper_query.ui.components.sidebar_inputs import get_chatbot_params


def streamlit_chatbot():
    st.sidebar.title("Chatbot Configuration")

    selected_chatbot_class, selected_label = select_chatbot()
    chatbot_args = get_chatbot_params(selected_chatbot_class)

    if st.sidebar.button("Confirm Chatbot"):
        st.session_state.chatbot_confirmed = True
        st.session_state.chatbot = selected_chatbot_class(**chatbot_args)
        st.sidebar.success(f"{selected_label} is ready!")
        st.title(f"{selected_label} Chatbot")

    display_chat_interface()


if __name__ == "__main__":
    streamlit_chatbot()
