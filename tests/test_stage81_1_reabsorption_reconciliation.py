from v1700.lineage.reabsorption_reconciliation import (
    build_reabsorption_completion_manifest,
    build_reconciled_core_logic_survival_matrix,
    run_reabsorption_reconciliation,
)
from v1700.gates.stage81_1_release_gate import run_stage81_1_release_gate


def test_reconciled_core_logic_matrix_updates_stage75_p0_missing_items():
    matrix = {entry.logic_id: entry for entry in build_reconciled_core_logic_survival_matrix()}
    assert matrix["temporal_continuity"].current_survival_status == "LIVE_RUNTIME"
    assert matrix["emotional_pressure_valve"].current_survival_status == "LIVE_RUNTIME"
    assert matrix["branch_commit_rollback"].current_survival_status == "LIVE_RUNTIME"
    assert matrix["sequence_scale_planning"].current_survival_status == "LIVE_RUNTIME"
    assert matrix["scene_scale_planning"].completion_level == "metadata_runtime_verified_not_full_render"


def test_reabsorption_completion_manifest_has_no_original_p0_missing_or_partial():
    manifest = build_reabsorption_completion_manifest()
    assert manifest["p0_total"] >= 10
    assert manifest["p0_missing_count"] == 0
    assert manifest["p0_partial_count"] == 0
    assert manifest["commercial_readiness_gaps"]


def test_reabsorption_reconciliation_gate_passes_truthfully():
    result = run_reabsorption_reconciliation()
    assert result["status"] == "pass"
    assert result["reabsorption_completion_manifest"]["p0_live_runtime_count"] >= 10
    gaps = result["commercial_readiness_gap_manifest"]["items"]
    assert any(gap["gap_id"] == "external_blind_critic_benchmark" for gap in gaps)


def test_stage81_1_release_gate_passes_and_keeps_commercial_gaps_visible():
    result = run_stage81_1_release_gate()
    assert result["status"] == "pass"
    assert result["p0_missing_count"] == 0
    assert result["p0_partial_count"] == 0
    assert result["commercial_readiness_gap_count"] >= 1
    assert result["node2_raw_reveal_access_count"] == 0
