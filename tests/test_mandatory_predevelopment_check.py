from __future__ import annotations

from pathlib import Path

from tools.run_mandatory_predevelopment_check import run_mandatory_predevelopment_check


def test_mandatory_predevelopment_check_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    result = run_mandatory_predevelopment_check(root)
    assert result["status"] == "pass"
    assert result["invariant_checks"]["github_main_green_required"] is True
    assert result["invariant_checks"]["release_assets_triplet_required"] is True
    assert result["invariant_checks"]["session_start_tool_present"] is True
    assert result["invariant_checks"]["session_end_tool_present"] is True
    assert result["invariant_checks"]["hook_installers_present"] is True
    assert "docs/workflow/PREFLIGHT_GUIDE_v1.1_GPT_STAGE.md" in result["workflow_documents"]
