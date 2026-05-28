from __future__ import annotations

from pathlib import Path

from tools.session_start import run_session_start


def test_session_start_without_fetch_reports_local_state() -> None:
    root = Path(__file__).resolve().parents[1]
    result = run_session_start(root, fetch_remote=False, write_report=False)
    assert result["mandatory_predevelopment"]["status"] == "pass"
    assert result["latest_session_note"].endswith(".md")
    assert result["branch"]
    assert result["head"]
    if result["status"] == "blocked":
        assert set(result["issues"]).issubset({"origin_main_missing", "latest_stage_tag_missing"})
