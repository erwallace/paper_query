import inspect
import tempfile
from pathlib import Path

import streamlit as st

assets_dir = Path(__file__).resolve().parents[4] / "assets"


def get_class_params(cls) -> list[str]:
    """Get the parameters of a class."""
    params = inspect.signature(cls.__init__).parameters
    return [
        name
        for name in params.keys()
        if name
        in ("model_name", "model_provider", "paper_path", "references_dir", "github_repo_url")
    ]


def model_name_input(name: str = "gpt-4o") -> str:
    """Get the model name from the sidebar."""
    return st.sidebar.text_input("Model Name", value=name, key="model_name_input")


def model_provider_input(provider: str = "openai") -> str:
    """Get the model provider from the sidebar."""
    return st.sidebar.text_input("Model Provider", value=provider, key="model_provider_input")


def paper_path_input() -> str:
    """Get the paper path from the sidebar."""
    uploaded_file = st.sidebar.file_uploader("Upload PDF", type="pdf")
    if uploaded_file is not None:
        # Save the uploaded file to a temporary directory
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    return str(assets_dir / "strainrelief_preprint.pdf")


def references_input() -> str:
    """Get the references from the sidebar and store them in a temporary directory."""
    uploaded_files = st.sidebar.file_uploader(
        "Upload References", type="pdf", accept_multiple_files=True
    )
    if uploaded_files:
        # Create a temporary directory to store the uploaded reference PDFs
        temp_dir = tempfile.mkdtemp()
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=temp_dir) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
        return temp_dir
    return str(assets_dir / "references")


def code_dir_input(github_repo_url="https://github.com/prescient-design/StrainRelief.git") -> str:
    """Get the code directory from the sidebar."""
    return st.sidebar.text_input("GitHub Repository URL", value=github_repo_url)


def get_param(param: str) -> str | list[str]:
    """Get the parameter value from the sidebar."""
    param_functions = {
        "model_name": model_name_input,
        "model_provider": model_provider_input,
        "paper_path": paper_path_input,
        "references_dir": references_input,
        "github_repo_url": code_dir_input,
    }
    if param in param_functions:
        return param_functions[param]()
    raise KeyError(f"{param} is not a valid chatbot argument.")


def get_chatbot_params(selected_chatbot_class: type) -> dict:
    """Get the chatbot parameters from the sidebar."""
    chatbot_params = get_class_params(selected_chatbot_class)
    return {param: get_param(param) for param in chatbot_params}
