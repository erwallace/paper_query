from pathlib import Path

# Base paths
project_dir: Path = Path(__file__).resolve().parents[3]
src_dir: Path = project_dir / "src"
test_dir: Path = project_dir / "test"
data_dir: Path = project_dir / "data"
assets_dir: Path = project_dir / "assets"

PERSIST_DIRECTORY: str = project_dir / "vectorstore"
