from __future__ import annotations

from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage148_release_gate import run_stage148_release_gate
from v1700.stage148 import run_stage148

ROOT = Path(__file__).resolve().parents[1]


def test_stage148_report_passes() -> None:
    result = run_stage148(ROOT)
    assert result["status"] == "pass"
    assert result["node_boundary_constitution_only"] is True
    assert result["authority_rule_count"] >= 7
    assert result["route_count"] >= 6
    assert result["projection_rule_count"] >= 7
    assert result["node2_surface_only_enforced"] is True
    assert result["node3_critic_scope_defined"] is True


def test_stage148_preserves_provider_zero_and_boundaries() -> None:
    result = run_stage148(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["losdb_write_enabled"] is False
    assert result["migration_execution_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage148_reuses_stage147_baseline_and_passes_gate() -> None:
    result = run_stage148(ROOT)
    baseline = result["parts"]["stage147_baseline"]
    assert baseline["status"] == "pass"
    assert baseline["branchpoint_lineage_preserved"] is True
    gate = run_stage148_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["node_authority_matrix_pass"]["status"] == "pass"
    assert gate["checks"]["boundary_enforcement_summary_pass"]["status"] == "pass"


def test_stage148_is_the_active_release_baseline() -> None:
    manifest = (ROOT / "manifests" / "live_core_manifest.json").read_text(encoding="utf-8")
    assert '"active_version": "stage148"' in manifest
    assert '"stage148_node_boundary_constitution"' in manifest
    assert '"stage148_release_gate"' in manifest

    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage148_release_gate"]["status"] == "pass"
