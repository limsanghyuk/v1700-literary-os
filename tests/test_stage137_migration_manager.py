from __future__ import annotations

from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage137_release_gate import run_stage137_release_gate
from v1700.migration_manager import run_stage137_migration_manager
from v1700.migration_manager.gate import MIGRATION_MANAGER_MODE

ROOT = Path(__file__).resolve().parents[1]


def test_stage137_report_passes() -> None:
    result = run_stage137_migration_manager(ROOT)
    assert result["status"] == "pass"
    assert result["mode"] == MIGRATION_MANAGER_MODE
    assert result["migration_plan_only"] is True
    assert result["migration_step_count"] >= 1


def test_stage137_covers_every_stage136_binding() -> None:
    result = run_stage137_migration_manager(ROOT)
    assert result["binding_step_count"] >= 1
    assert result["covered_binding_count"] == result["binding_step_count"]
    assert result["approval_checkpoint_count"] >= 1
    assert result["rollback_ready_count"] == result["migration_step_count"]


def test_stage137_blocks_execution_writes_and_providers() -> None:
    result = run_stage137_migration_manager(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["losdb_write_enabled"] is False
    assert result["migration_execution_enabled"] is False
    assert result["storage_contract_write_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage137_preserves_review_only_approval_checkpoint() -> None:
    result = run_stage137_migration_manager(ROOT)
    steps = result["parts"]["migration_plan"]["steps"]
    checkpoints = [step for step in steps if step["scope"] == "checkpoint"]
    assert checkpoints
    assert any(step["requires_human_approval"] is True for step in checkpoints)
    assert any(step["step_id"] == "STAGE137-CHECKPOINT-REVIEW-ONLY" for step in checkpoints)


def test_stage137_preflight_and_release_gate_pass() -> None:
    result = run_stage137_migration_manager(ROOT)
    preflight = result["parts"]["preflight"]
    assert preflight["python_fallback"]["status"] == "PASS"
    assert all(preflight["survival_matrix"].values())
    gate = run_stage137_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["all_bindings_covered_pass"]["status"] == "pass"


def test_stage137_is_the_active_release_baseline() -> None:
    manifest = (ROOT / "manifests" / "live_core_manifest.json").read_text(encoding="utf-8")
    assert '"active_version": "stage137"' in manifest
    assert '"stage137_migration_manager"' in manifest
    assert '"stage137_release_gate"' in manifest

    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage137_release_gate"]["status"] == "pass"
