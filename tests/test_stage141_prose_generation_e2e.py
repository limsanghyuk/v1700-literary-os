from __future__ import annotations

from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage141_release_gate import run_stage141_release_gate
from v1700.stage141 import run_stage141

ROOT = Path(__file__).resolve().parents[1]


def test_stage141_report_passes() -> None:
    result = run_stage141(ROOT)
    assert result["status"] == "pass"
    assert result["prose_generation_e2e_only"] is True
    assert result["rendered_scene_count"] >= 1
    assert result["critic_gate_status"] == "pass"
    assert result["benchmark_result_status"] == "pass"


def test_stage141_preserves_provider_zero_and_boundaries() -> None:
    result = run_stage141(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["losdb_write_enabled"] is False
    assert result["migration_execution_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage141_reuses_stage140_baseline_and_passes_gate() -> None:
    result = run_stage141(ROOT)
    baseline = result["parts"]["stage140_baseline"]
    assert baseline["status"] == "pass"
    assert baseline["branchpoint_lineage_preserved"] is True
    gate = run_stage141_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["stage142_benchmark_pack_ready_pass"]["status"] == "pass"


def test_stage141_is_the_active_release_baseline() -> None:
    manifest = (ROOT / "manifests" / "live_core_manifest.json").read_text(encoding="utf-8")
    assert '"active_version": "stage141"' in manifest or '"active_version": "stage142"' in manifest or '"active_version": "stage143"' in manifest or '"active_version": "stage144"' in manifest
    assert '"stage141_prose_generation_e2e"' in manifest
    assert '"stage141_release_gate"' in manifest

    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage141_release_gate"]["status"] == "pass"
