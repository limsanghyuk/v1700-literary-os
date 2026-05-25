from __future__ import annotations

from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage149_release_gate import run_stage149_release_gate
from v1700.stage149 import run_stage149

ROOT = Path(__file__).resolve().parents[1]


def test_stage149_report_passes() -> None:
    result = run_stage149(ROOT)
    assert result["status"] == "pass"
    assert result["body_constitution_release_gate_only"] is True
    assert result["gate_rule_count"] >= 8
    assert result["sealed_page01"] is True
    assert result["stage150_memory_body_ready"] is True


def test_stage149_preserves_provider_zero_and_page01_blockers() -> None:
    result = run_stage149(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["losdb_write_enabled"] is False
    assert result["migration_execution_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage149_reuses_stage148_baseline_and_passes_gate() -> None:
    result = run_stage149(ROOT)
    baseline = result["parts"]["stage148_baseline"]
    assert baseline["status"] == "pass"
    assert baseline["branchpoint_lineage_preserved"] is True
    gate = run_stage149_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["gate_matrix_pass"]["status"] == "pass"
    assert gate["checks"]["page01_constitution_seal_pass"]["status"] == "pass"


def test_stage149_is_the_active_release_baseline() -> None:
    manifest = (ROOT / "manifests" / "live_core_manifest.json").read_text(encoding="utf-8")
    assert any(
        f'"active_version": "stage{stage}"' in manifest
        for stage in (149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161)
    )
    assert '"stage149_body_constitution_release_gate"' in manifest
    assert '"stage149_release_gate"' in manifest

    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage149_release_gate"]["status"] == "pass"
