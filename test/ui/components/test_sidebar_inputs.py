import pytest
from paper_query.chatbots import BaseChatbot
from paper_query.constants import assets_dir
from paper_query.ui.components.sidebar_inputs import (
    code_dir_input,
    get_chatbot_params,
    get_param,
    model_name_input,
    model_provider_input,
    paper_path_input,
    references_input,
)


def test_model_name_input():
    assert model_name_input() == "gpt-4.1"
    assert model_name_input("gpt-4.1-nano") == "gpt-4.1-nano"


def test_model_provider_input():
    assert model_provider_input() == "openai"
    assert model_provider_input("huggingface") == "huggingface"


def test_paper_path_input():
    # TODO: add test for tmp_file
    assert paper_path_input() == str(assets_dir / "strainrelief_preprint.pdf")


def test_references_input():
    # TODO: add test for tmp_dir
    assert references_input() == str(assets_dir / "references")


def test_code_dir_input():
    assert code_dir_input() == "https://github.com/prescient-design/StrainRelief.git"
    assert code_dir_input("some_url") == "some_url"


def test_get_param():
    assert get_param("model_name") == "gpt-4.1-nano"
    assert get_param("model_provider") == "openai"
    assert get_param("paper_path") == str(assets_dir / "strainrelief_preprint.pdf")
    assert get_param("references_dir") == str(assets_dir / "references")
    assert get_param("github_repo_url") == "https://github.com/prescient-design/StrainRelief.git"
    with pytest.raises(KeyError):
        get_param("invalid")


def test_get_chatbot_params():
    assert get_chatbot_params(BaseChatbot) == {"model_name": "gpt-4.1", "model_provider": "openai"}
