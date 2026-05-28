from __future__ import annotations

from pathlib import Path

from tools.run_precommit_guard import run_precommit_guard


def test_precommit_guard_passes_on_clean_repo() -> None:
    root = Path(__file__).resolve().parents[1]
    result = run_precommit_guard(root, require_release_gate=False)
    assert result["status"] == "pass"
    assert result["mandatory_predevelopment"]["status"] == "pass"
