from __future__ import annotations

from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage143_release_gate import run_stage143_release_gate
from v1700.stage143 import run_stage143

ROOT = Path(__file__).resolve().parents[1]


def test_stage143_report_passes() -> None:
    result = run_stage143(ROOT)
    assert result["status"] == "pass"
    assert result["user_cli_api_docs_only"] is True
    assert result["cli_help_available"] is True
    assert result["api_contract_documented_only"] is True


def test_stage143_preserves_provider_zero_and_boundaries() -> None:
    result = run_stage143(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["losdb_write_enabled"] is False
    assert result["migration_execution_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage143_reuses_stage142_baseline_and_passes_gate() -> None:
    result = run_stage143(ROOT)
    baseline = result["parts"]["stage142_baseline"]
    assert baseline["status"] == "pass"
    assert baseline["branchpoint_lineage_preserved"] is True
    gate = run_stage143_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["stage144_split_ci_runtime_ready_pass"]["status"] == "pass"


def test_stage143_is_the_active_release_baseline() -> None:
    manifest = (ROOT / "manifests" / "live_core_manifest.json").read_text(encoding="utf-8")
    assert '"active_version": "stage143"' in manifest or '"active_version": "stage144"' in manifest or '"active_version": "stage145"' in manifest or '"active_version": "stage146"' in manifest
    assert '"stage143_user_cli_api_docs"' in manifest
    assert '"stage143_release_gate"' in manifest

    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage143_release_gate"]["status"] == "pass"
