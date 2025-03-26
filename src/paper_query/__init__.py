from pathlib import Path

from .base_chatbot import main as base_chatbot
from .paper_query_chatbot import main as paper_query_chatbot
from .paper_query_plus_chatbot import main as paper_query_plus_chatbot

# Directories
project_dir: Path = Path(__file__).resolve().parents[2]
src_dir: Path = project_dir / "src"
test_dir: Path = project_dir / "tests"
data_dir: Path = project_dir / "data"
assets_dir: Path = project_dir / "assets"

__all__ = [
    "base_chatbot",
    "paper_query_chatbot",
    "paper_query_plus_chatbot",
    "project_dir",
    "src_dir",
    "test_dir",
    "data_dir",
    "assets_dir",
]
