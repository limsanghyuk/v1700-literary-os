from __future__ import annotations

from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage147_release_gate import run_stage147_release_gate
from v1700.stage147 import run_stage147

ROOT = Path(__file__).resolve().parents[1]


def test_stage147_report_passes() -> None:
    result = run_stage147(ROOT)
    assert result["status"] == "pass"
    assert result["project_manifest_body_only"] is True
    assert result["manifest_section_count"] >= 5
    assert result["canonical_packet_count"] >= 7
    assert result["state_binding_count"] >= 7
    assert result["policy_boundary_complete"] is True
    assert result["load_order_complete"] is True


def test_stage147_preserves_provider_zero_and_boundaries() -> None:
    result = run_stage147(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["losdb_write_enabled"] is False
    assert result["migration_execution_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage147_reuses_stage146_baseline_and_passes_gate() -> None:
    result = run_stage147(ROOT)
    baseline = result["parts"]["stage146_baseline"]
    assert baseline["status"] == "pass"
    assert baseline["branchpoint_lineage_preserved"] is True
    gate = run_stage147_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["manifest_state_bindings_pass"]["status"] == "pass"
    assert gate["checks"]["manifest_policy_boundary_pass"]["status"] == "pass"


def test_stage147_is_the_active_release_baseline() -> None:
    manifest = (ROOT / "manifests" / "live_core_manifest.json").read_text(encoding="utf-8")
    assert '"active_version": "stage147"' in manifest or '"active_version": "stage148"' in manifest
    assert '"stage147_project_manifest_body"' in manifest
    assert '"stage147_release_gate"' in manifest

    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage147_release_gate"]["status"] == "pass"
