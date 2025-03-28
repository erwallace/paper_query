import sys

import pytest
from paper_query.utils import load_api_keys


@pytest.mark.skipif(sys.platform == "linux", reason="Skip for GitHub actions")
def test_load_api_keys():
    with pytest.raises(FileNotFoundError):
        load_api_keys("non_existent_file")

    api_keys = load_api_keys()
    assert "OPENAI_API_KEY" in api_keys
    assert "GROQ_API_KEY" in api_keys
