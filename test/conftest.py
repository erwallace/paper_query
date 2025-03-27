import os
import sys
from pathlib import Path

import pytest

if sys.platform != "ubuntu":  # Skip for GitHub actions
    print(sys.platform)
    from paper_query.constants import GROQ_API_KEY, OPENAI_API_KEY

    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY


@pytest.fixture(scope="session")
def assets_dir():
    return Path(__file__).resolve().parents[0] / "assets"
