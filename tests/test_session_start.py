from __future__ import annotations

from pathlib import Path

from tools.session_start import run_session_start


def test_session_start_without_fetch_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    result = run_session_start(root, fetch_remote=True, write_report=False)
    assert result["status"] == "pass"
    assert result["mandatory_predevelopment"]["status"] == "pass"
    assert result["latest_stage_tag"].startswith("v1700-stage")
    assert result["latest_session_note"].endswith(".md")
