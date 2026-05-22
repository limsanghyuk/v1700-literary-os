from __future__ import annotations

from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage144_release_gate import run_stage144_release_gate
from v1700.stage144 import run_stage144

ROOT = Path(__file__).resolve().parents[1]


def test_stage144_report_passes() -> None:
    result = run_stage144(ROOT)
    assert result["status"] == "pass"
    assert result["workflow_split_only"] is True
    assert result["workflow_split_complete"] is True
    assert result["runtime_lane_count"] >= 5


def test_stage144_preserves_provider_zero_and_boundaries() -> None:
    result = run_stage144(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["losdb_write_enabled"] is False
    assert result["migration_execution_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage144_reuses_stage143_baseline_and_passes_gate() -> None:
    result = run_stage144(ROOT)
    baseline = result["parts"]["stage143_baseline"]
    assert baseline["status"] == "pass"
    assert baseline["branchpoint_lineage_preserved"] is True
    gate = run_stage144_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["workflow_split_complete_pass"]["status"] == "pass"


def test_stage144_is_the_active_release_baseline() -> None:
    manifest = (ROOT / "manifests" / "live_core_manifest.json").read_text(encoding="utf-8")
    assert '"active_version": "stage144"' in manifest or '"active_version": "stage145"' in manifest or '"active_version": "stage146"' in manifest or '"active_version": "stage147"' in manifest
    assert '"stage144_split_ci_runtime_strategy"' in manifest
    assert '"stage144_release_gate"' in manifest

    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage144_release_gate"]["status"] == "pass"
