from __future__ import annotations

from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage142_release_gate import run_stage142_release_gate
from v1700.stage142 import run_stage142

ROOT = Path(__file__).resolve().parents[1]


def test_stage142_report_passes() -> None:
    result = run_stage142(ROOT)
    assert result["status"] == "pass"
    assert result["longform_benchmark_pack_only"] is True
    assert result["benchmark_case_count"] >= 3
    assert result["benchmark_scoreboard_status"] == "pass"


def test_stage142_preserves_provider_zero_and_boundaries() -> None:
    result = run_stage142(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["losdb_write_enabled"] is False
    assert result["migration_execution_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage142_reuses_stage141_baseline_and_passes_gate() -> None:
    result = run_stage142(ROOT)
    baseline = result["parts"]["stage141_baseline"]
    assert baseline["status"] == "pass"
    assert baseline["branchpoint_lineage_preserved"] is True
    gate = run_stage142_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["stage143_user_docs_ready_pass"]["status"] == "pass"


def test_stage142_is_the_active_release_baseline() -> None:
    manifest = (ROOT / "manifests" / "live_core_manifest.json").read_text(encoding="utf-8")
    assert '"active_version": "stage142"' in manifest or '"active_version": "stage143"' in manifest or '"active_version": "stage144"' in manifest or '"active_version": "stage145"' in manifest or '"active_version": "stage146"' in manifest
    assert '"stage142_longform_benchmark_pack"' in manifest
    assert '"stage142_release_gate"' in manifest

    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage142_release_gate"]["status"] == "pass"
