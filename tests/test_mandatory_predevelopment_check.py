from pathlib import Path

from tools.run_mandatory_predevelopment_check import run_mandatory_predevelopment_check


ROOT = Path(__file__).resolve().parents[1]


def test_mandatory_predevelopment_check_passes_for_stage101_repository():
    report = run_mandatory_predevelopment_check(ROOT)
    assert report["status"] == "pass"
    assert "session_start_sync" in report["must_check"]
    assert "gitnexus_index_freshness" in report["must_check"]
    assert "docs/workflow/WORKFLOW.md" in report["workflow_documents"]
    assert "docs/workflow/BRANCH_STRATEGY.md" in report["workflow_documents"]
    assert "docs/workflow/PREFLIGHT_GUIDE_v1.1_STAGE160.md" in report["workflow_documents"]
    assert report["invariant_checks"]["stage101_gate_pass"] is True
    assert report["invariant_checks"]["active_stage_gate_pass"] is True
    assert report["invariant_checks"]["main_release_gate_pass"] is True
    assert report["invariant_checks"]["gitnexus_runtime_dependency_required_false"] is True
    assert report["invariant_checks"]["github_main_green_required"] is True
    assert report["invariant_checks"]["release_assets_triplet_required"] is True
    assert report["invariant_checks"]["workflow_documents_declared"] is True
    assert report["workflow_upgrade_status"] == "v1_1_stage160_applied"
