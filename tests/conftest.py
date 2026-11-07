"""Pytest fixtures and test environment setup."""

import sys
from pathlib import Path
import pytest

# Ensure src/ is on sys.path
SRC_DIR = Path(__file__).parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from briefing_engine.orchestrator import BriefingOrchestrator
from briefing_engine.models.raw_data import IngestionBundle


@pytest.fixture
def repo_root():
    return Path(__file__).parent.parent


@pytest.fixture
def sample_bundle(repo_root):
    return BriefingOrchestrator.load_bundle_from_files(
        csv_path=str(repo_root / "data" / "sample_financial_kpis.csv"),
        json_path=str(repo_root / "data" / "sample_project_status.json"),
        md_path=str(repo_root / "data" / "sample_github_repo_brief.md")
    )
