from __future__ import annotations

from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage145_release_gate import run_stage145_release_gate
from v1700.stage145 import run_stage145

ROOT = Path(__file__).resolve().parents[1]


def test_stage145_report_passes() -> None:
    result = run_stage145(ROOT)
    assert result["status"] == "pass"
    assert result["body_constitution_only"] is True
    assert result["formula_policy_complete"] is True
    assert result["body_layer_count"] >= 7
    assert result["stage150_memory_body_ready"] is True


def test_stage145_preserves_provider_zero_and_boundaries() -> None:
    result = run_stage145(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["losdb_write_enabled"] is False
    assert result["migration_execution_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage145_reuses_stage144_baseline_and_passes_gate() -> None:
    result = run_stage145(ROOT)
    baseline = result["parts"]["stage144_baseline"]
    assert baseline["status"] == "pass"
    assert baseline["branchpoint_lineage_preserved"] is True
    gate = run_stage145_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["formula_policy_complete_pass"]["status"] == "pass"
    assert gate["checks"]["stage150_entry_criteria_pass"]["status"] == "pass"


def test_stage145_remains_registered_in_the_active_release_chain() -> None:
    manifest = (ROOT / "manifests" / "live_core_manifest.json").read_text(encoding="utf-8")
    assert '"active_version": "stage145"' in manifest or '"active_version": "stage146"' in manifest or '"active_version": "stage147"' in manifest or '"active_version": "stage148"' in manifest or '"active_version": "stage149"' in manifest
    assert '"stage145_body_constitution"' in manifest
    assert '"stage145_release_gate"' in manifest

    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage145_release_gate"]["status"] == "pass"
