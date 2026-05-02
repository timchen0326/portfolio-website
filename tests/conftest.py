import pytest
from pathlib import Path


@pytest.fixture
def project_dir() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture
def docs_dir(project_dir) -> Path:
    return project_dir / "docs"


@pytest.fixture
def assets_dir(project_dir) -> Path:
    return project_dir / "assets"
