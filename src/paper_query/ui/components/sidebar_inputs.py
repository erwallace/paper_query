import inspect
import tempfile

import streamlit as st


def get_class_params(cls):
    params = inspect.signature(cls.__init__).parameters
    return [name for name, param in params.items() if name != "self"]


def model_name_input(name="gpt-4o"):
    return st.sidebar.text_input("Model Name", value=name)


def model_provider_input(provider="openai"):
    return st.sidebar.text_input("Model Provider", value=provider)


def paper_path_input():
    uploaded_file = st.sidebar.file_uploader("Upload PDF", type="pdf")
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    return "./assets/strainrelief_preprint.pdf"


def references_input():
    uploaded_file = st.sidebar.file_uploader("Upload References", type="pdf")
    if uploaded_file is not None:
        # TODO: Implement references handling
        pass
    return ""


def code_dir_input():
    uploaded_file = st.sidebar.file_uploader("Upload Code", type="zip")
    if uploaded_file is not None:
        # TODO: Implement code directory handling
        pass
    return ""


def get_param(param):
    param_functions = {
        "model_name": model_name_input,
        "model_provider": model_provider_input,
        "paper_path": paper_path_input,
        "refernces_dir": references_input,
        "code_dir": code_dir_input,
    }
    if param in param_functions:
        return param_functions[param]()
    raise KeyError(f"{param} is not a valid chatbot argument.")


def get_chatbot_params(selected_chatbot_class):
    chatbot_params = get_class_params(selected_chatbot_class)
    return {param: get_param(param) for param in chatbot_params}
