from __future__ import annotations

from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage136_release_gate import run_stage136_release_gate
from v1700.schema_registry import run_stage136_schema_registry
from v1700.schema_registry.gate import SCHEMA_REGISTRY_MODE

ROOT = Path(__file__).resolve().parents[1]


def test_stage136_report_passes() -> None:
    result = run_stage136_schema_registry(ROOT)
    assert result["status"] == "pass"
    assert result["mode"] == SCHEMA_REGISTRY_MODE
    assert result["schema_registry_only"] is True
    assert result["schema_count"] >= 3


def test_stage136_binds_every_stage135_candidate() -> None:
    result = run_stage136_schema_registry(ROOT)
    assert result["binding_count"] >= 1
    assert result["binding_count"] == result["validated_candidate_count"]
    assert result["migration_ready_count"] == result["binding_count"]
    assert result["storage_contract_ready_count"] == result["binding_count"]


def test_stage136_blocks_writes_training_and_providers() -> None:
    result = run_stage136_schema_registry(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["losdb_write_enabled"] is False
    assert result["migration_execution_enabled"] is False
    assert result["storage_contract_write_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage136_preserves_review_only_route() -> None:
    result = run_stage136_schema_registry(ROOT)
    bindings = result["parts"]["schema_registry"]["bindings"]
    review_only = [binding for binding in bindings if binding["decision"] == "REVIEW_ONLY"]
    assert review_only
    assert all(binding["schema_id"] == "stage136.review_only_candidate.v1" for binding in review_only)
    assert all(binding["writer_review_required"] is True for binding in review_only)


def test_stage136_preflight_and_release_gate_pass() -> None:
    result = run_stage136_schema_registry(ROOT)
    preflight = result["parts"]["preflight"]
    assert preflight["python_fallback"]["status"] == "PASS"
    assert all(preflight["survival_matrix"].values())
    gate = run_stage136_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["all_candidates_bound_pass"]["status"] == "pass"


def test_stage136_is_the_active_release_baseline() -> None:
    manifest = (ROOT / "manifests" / "live_core_manifest.json").read_text(encoding="utf-8")
    assert '"active_version": "stage136"' in manifest
    assert '"stage136_schema_registry"' in manifest
    assert '"stage136_release_gate"' in manifest

    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage136_release_gate"]["status"] == "pass"
