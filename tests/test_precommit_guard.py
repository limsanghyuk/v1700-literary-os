from __future__ import annotations

from pathlib import Path

from tools.run_precommit_guard import _diff_has_block_pattern, BLOCK_PATTERNS, run_precommit_guard


def test_precommit_guard_passes_on_clean_repo() -> None:
    root = Path(__file__).resolve().parents[1]
    result = run_precommit_guard(root, require_release_gate=False)
    assert result["status"] == "pass"
    assert result["mandatory_predevelopment"]["status"] == "pass"


def test_precommit_guard_matches_json_invariant_regression() -> None:
    diff = '+  "provider_default_calls": 1\n'
    assert _diff_has_block_pattern(diff, BLOCK_PATTERNS["provider_default_nonzero"]) is True
