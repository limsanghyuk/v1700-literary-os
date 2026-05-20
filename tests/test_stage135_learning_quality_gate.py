from __future__ import annotations

from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage135_release_gate import run_stage135_release_gate
from v1700.learning_quality_gate import run_stage135_learning_quality_gate
from v1700.learning_quality_gate.gate import LEARNING_QUALITY_MODE, build_candidate_registry
from v1700.stage134 import run_stage134

ROOT = Path(__file__).resolve().parents[1]


def test_stage135_report_passes() -> None:
    result = run_stage135_learning_quality_gate(ROOT)
    assert result["status"] == "pass"
    assert result["mode"] == LEARNING_QUALITY_MODE
    assert result["learning_candidate_only"] is True
    assert result["candidate_count"] >= 1


def test_stage135_blocks_learning_training_and_mutation() -> None:
    result = run_stage135_learning_quality_gate(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["learning_allowed_count"] == 0
    assert result["training_triggered_count"] == 0
    assert result["mutation_allowed_count"] == 0
    assert result["auto_repair_mutation_count"] == 0


def test_stage135_preserves_provider_zero_and_boundaries() -> None:
    result = run_stage135_learning_quality_gate(ROOT)
    assert result["provider_default_calls"] == 0
    assert result["live_provider_call_count_in_release_gate"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["raw_manuscript_provider_leakage"] == 0
    assert result["raw_manuscript_cross_project_leakage"] == 0
    assert result["credential_leakage"] == 0
    assert result["canon_auto_resolution_count"] == 0
    assert result["cross_project_write_allowed"] is False


def test_stage135_routes_stage134_review_to_review_only() -> None:
    registry = build_candidate_registry(run_stage134(ROOT))
    assert registry.status == "pass"
    review_cases = [case for case in registry.candidates if case.decision == "REVIEW_ONLY"]
    assert review_cases
    assert all(case.learning_allowed is False for case in review_cases)
    assert all(case.training_triggered is False for case in review_cases)


def test_stage135_preflight_and_release_gate_pass() -> None:
    result = run_stage135_learning_quality_gate(ROOT)
    preflight = result["parts"]["preflight"]
    assert preflight["python_fallback"]["status"] == "PASS"
    assert all(preflight["survival_matrix"].values())
    gate = run_stage135_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["candidate_only_mode_pass"]["status"] == "pass"


def test_stage135_is_the_active_release_baseline() -> None:
    manifest = (ROOT / "manifests" / "live_core_manifest.json").read_text(encoding="utf-8")
    assert '"active_version": "stage135"' in manifest
    assert '"stage135_learning_quality_gate"' in manifest
    assert '"stage135_release_gate"' in manifest

    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage135_release_gate"]["status"] == "pass"
