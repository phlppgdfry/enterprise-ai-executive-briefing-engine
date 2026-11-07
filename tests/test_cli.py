"""Unit tests for Briefing Engine CLI."""

import subprocess
import sys
import os
from pathlib import Path


def test_cli_execution_runs_cleanly(repo_root):
    cli_script = repo_root / "src" / "briefing_engine" / "cli.py"

    cmd = [
        sys.executable,
        str(cli_script),
        "run",
        "--csv", str(repo_root / "data" / "sample_financial_kpis.csv"),
        "--project", str(repo_root / "data" / "sample_project_status.json"),
        "--repo", str(repo_root / "data" / "sample_github_repo_brief.md"),
        "--provider", "mock",
        "--out", str(repo_root / "output")
    ]

    env = {**os.environ, "PYTHONPATH": str(repo_root / "src")}
    res = subprocess.run(cmd, capture_output=True, text=True, check=True, env=env)
    assert "ENTERPRISE AI EXECUTIVE BRIEFING ENGINE" in res.stdout
    assert "Operational Health Score:" in res.stdout
    assert "Artifacts successfully exported:" in res.stdout
    assert (repo_root / "output" / "executive_briefing.md").exists()
    assert (repo_root / "output" / "executive_briefing.html").exists()
