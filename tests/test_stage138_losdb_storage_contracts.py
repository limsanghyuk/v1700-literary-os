from __future__ import annotations

from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage138_release_gate import run_stage138_release_gate
from v1700.losdb_storage_contracts import run_stage138_losdb_storage_contracts
from v1700.losdb_storage_contracts.gate import LOSDB_STORAGE_CONTRACT_MODE

ROOT = Path(__file__).resolve().parents[1]


def test_stage138_report_passes() -> None:
    result = run_stage138_losdb_storage_contracts(ROOT)
    assert result["status"] == "pass"
    assert result["mode"] == LOSDB_STORAGE_CONTRACT_MODE
    assert result["storage_contract_catalog_only"] is True
    assert result["schema_contract_count"] >= 3


def test_stage138_covers_every_stage137_binding_route() -> None:
    result = run_stage138_losdb_storage_contracts(ROOT)
    assert result["binding_route_count"] >= 1
    assert result["covered_binding_count"] == result["binding_route_count"]
    assert result["governance_ready_count"] == result["binding_route_count"]
    assert result["approval_lane_count"] >= 1


def test_stage138_blocks_writes_training_and_providers() -> None:
    result = run_stage138_losdb_storage_contracts(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["losdb_write_enabled"] is False
    assert result["migration_execution_enabled"] is False
    assert result["storage_contract_write_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage138_preserves_review_lane_and_dependencies() -> None:
    result = run_stage138_losdb_storage_contracts(ROOT)
    lanes = result["parts"]["storage_contract_catalog"]["approval_lanes"]
    routes = result["parts"]["storage_contract_catalog"]["routes"]
    assert lanes
    assert any(lane["lane_name"] == "writer_review_queue" for lane in lanes)
    assert any(route["approval_lane"] == "writer_review_queue" for route in routes)
    assert all(route["depends_on_step"] for route in routes)


def test_stage138_preflight_and_release_gate_pass() -> None:
    result = run_stage138_losdb_storage_contracts(ROOT)
    preflight = result["parts"]["preflight"]
    assert preflight["python_fallback"]["status"] == "PASS"
    assert all(preflight["survival_matrix"].values())
    gate = run_stage138_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["governance_ready_pass"]["status"] == "pass"


def test_stage138_is_the_active_release_baseline() -> None:
    manifest = (ROOT / "manifests" / "live_core_manifest.json").read_text(encoding="utf-8")
    assert '"active_version": "stage138"' in manifest
    assert '"stage138_losdb_storage_contracts"' in manifest
    assert '"stage138_release_gate"' in manifest

    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage138_release_gate"]["status"] == "pass"
