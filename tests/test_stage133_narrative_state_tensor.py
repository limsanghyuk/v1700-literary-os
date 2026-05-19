from __future__ import annotations

from pathlib import Path

from v1700.gates.stage133_release_gate import run_stage133_release_gate
from v1700.narrative_state_tensor import run_stage133_narrative_state_tensor
from v1700.narrative_state_tensor.measurement import DIMENSIONS, measure_stage132_classifier_output
from v1700.contradiction_classifier.classifier import run_stage132_classifier_matrix

ROOT = Path(__file__).resolve().parents[1]


def test_stage133_tensor_report_passes() -> None:
    result = run_stage133_narrative_state_tensor(ROOT)
    assert result["status"] == "pass"
    assert result["measurement_mode"] == "DETERMINISTIC_8D_LOCAL_ONLY"
    assert result["dimension_count"] == 8
    assert result["tensor_case_count"] == 5


def test_stage133_has_exact_8d_dimension_contract() -> None:
    assert DIMENSIONS == (
        "causality_integrity",
        "temporal_continuity",
        "reveal_budget_integrity",
        "character_agency",
        "emotional_momentum",
        "voice_stability",
        "attention_economy",
        "canon_isolation",
    )


def test_stage133_routes_true_contradiction_to_review_not_repair() -> None:
    tensor = measure_stage132_classifier_output(run_stage132_classifier_matrix())
    true_case = next(item for item in tensor.tensors if item.classification == "true_contradiction")
    assert true_case.status == "REVIEW_REQUIRED"
    assert true_case.writer_review_required is True
    assert true_case.mutation_allowed is False


def test_stage133_keeps_mystery_exemption_pass_when_locked() -> None:
    tensor = measure_stage132_classifier_output(run_stage132_classifier_matrix())
    mystery = next(item for item in tensor.tensors if item.classification == "intentional_mystery")
    assert mystery.status == "PASS"
    assert mystery.dimensions["reveal_budget_integrity"] >= 0.90


def test_stage133_preserves_provider_zero_and_node2_boundaries() -> None:
    result = run_stage133_narrative_state_tensor(ROOT)
    assert result["provider_default_calls"] == 0
    assert result["live_provider_call_count_in_release_gate"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["raw_manuscript_provider_leakage"] == 0
    assert result["raw_manuscript_cross_project_leakage"] == 0


def test_stage133_blocks_auto_resolution_and_cross_project_write() -> None:
    result = run_stage133_narrative_state_tensor(ROOT)
    assert result["gate26_hard_block_enabled"] is False
    assert result["canon_auto_resolution_count"] == 0
    assert result["auto_repair_mutation_count"] == 0
    assert result["cross_project_write_allowed"] is False


def test_stage133_preflight_and_release_gate_pass() -> None:
    result = run_stage133_narrative_state_tensor(ROOT)
    preflight = result["parts"]["gitnexus_preflight"]
    assert preflight["python_fallback"]["status"] == "PASS"
    assert all(preflight["survival_matrix"].values())
    gate = run_stage133_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["dimension_count_8_pass"]["status"] == "pass"
