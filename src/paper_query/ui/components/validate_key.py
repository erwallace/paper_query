import streamlit as st
from loguru import logger
from openai import OpenAI

from paper_query.constants import STREAMLIT_CHEAP_MODEL, STREAMLIT_EXPENSIVE_MODEL


def validate_openai_api_key(api_key: str):
    """Validates the OpenAI API key and updates the session state accordingly."""
    if api_key and api_key != st.session_state.last_validated_key:
        try:
            client = OpenAI(api_key=api_key)
            client.models.list()
            logger.debug("API key validation successful.")
            st.session_state.model_name = STREAMLIT_EXPENSIVE_MODEL
            st.session_state.last_validated_key = api_key
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            st.sidebar.error("Invalid API key. Please check your OpenAI API key.")
            st.session_state.model_name = STREAMLIT_CHEAP_MODEL
            st.session_state.last_validated_key = None  # Reset if validation fails
    elif not api_key:
        # Reset to cheap model if key is cleared
        st.session_state.model_name = STREAMLIT_CHEAP_MODEL
        st.session_state.last_validated_key = None
