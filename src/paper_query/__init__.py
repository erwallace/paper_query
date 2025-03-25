from pathlib import Path

from ._paper_query_v0 import main as paper_query_v0
from ._paper_query_v1 import main as paper_query_v1

# Directories
project_dir: Path = Path(__file__).resolve().parents[2]
src_dir: Path = project_dir / "src"
test_dir: Path = project_dir / "tests"
data_dir: Path = project_dir / "data"
assets_dir: Path = project_dir / "assets"

__all__ = [
    "paper_query_v0",
    "paper_query_v1",
    "project_dir",
    "src_dir",
    "test_dir",
    "data_dir",
    "assets_dir",
]
