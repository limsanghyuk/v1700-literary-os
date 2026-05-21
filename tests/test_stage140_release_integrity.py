from __future__ import annotations

from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage140_release_gate import run_stage140_release_gate
from v1700.stage140 import run_stage140

ROOT = Path(__file__).resolve().parents[1]


def test_stage140_report_passes() -> None:
    result = run_stage140(ROOT)
    assert result["status"] == "pass"
    assert result["release_integrity_gate_only"] is True
    assert result["product_proof_skeleton_only"] is True
    assert result["stage141_product_e2e_ready"] is True


def test_stage140_metadata_and_assets_align() -> None:
    result = run_stage140(ROOT)
    assert result["metadata_consistency_status"] == "pass"
    assert result["release_asset_integrity_status"] == "pass"
    assert result["sample_project_contract_status"] == "pass"
    assert result["benchmark_contract_status"] == "pass"


def test_stage140_blocks_writes_training_and_providers() -> None:
    result = run_stage140(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["losdb_write_enabled"] is False
    assert result["migration_execution_enabled"] is False
    assert result["storage_contract_write_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage140_preflight_and_release_gate_pass() -> None:
    result = run_stage140(ROOT)
    baseline = result["parts"]["stage139_baseline"]
    assert baseline["status"] == "pass"
    assert baseline["branchpoint_lineage_preserved"] is True
    gate = run_stage140_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["stage141_product_e2e_ready_pass"]["status"] == "pass"


def test_stage140_is_the_active_release_baseline() -> None:
    manifest = (ROOT / "manifests" / "live_core_manifest.json").read_text(encoding="utf-8")
    assert '"active_version": "stage140"' in manifest
    assert '"stage140_release_integrity"' in manifest
    assert '"stage140_release_gate"' in manifest

    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage140_release_gate"]["status"] == "pass"
