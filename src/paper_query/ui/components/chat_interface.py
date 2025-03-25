import streamlit as st


def display_chat_interface() -> None:
    """Display the chat interface."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if "chatbot_confirmed" in st.session_state and st.session_state.chatbot_confirmed:
        if user_input := st.chat_input("What is your question?"):
            st.chat_message("user").markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                for response_chunk in st.session_state.chatbot.stream_response(user_input):
                    full_response += response_chunk
                    message_placeholder.markdown(full_response)

                message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        st.info("Please select a chatbot type and confirm in the sidebar to start chatting.")
