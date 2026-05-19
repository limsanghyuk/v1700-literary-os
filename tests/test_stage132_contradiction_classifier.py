from __future__ import annotations

from pathlib import Path

from v1700.contradiction_classifier import run_stage132_contradiction_classifier
from v1700.contradiction_classifier.classifier import build_stage132_fixture_evidence, classify_contradiction
from v1700.gates.stage132_release_gate import run_stage132_release_gate

ROOT = Path(__file__).resolve().parents[1]


def test_stage132_contradiction_classifier_passes() -> None:
    result = run_stage132_contradiction_classifier(ROOT)
    assert result["status"] == "pass"
    assert result["classifier_mode"] == "DETERMINISTIC_EVIDENCE_CLASSIFIER"
    assert result["case_count"] == 5


def test_stage132_distinguishes_true_contradiction_from_exemptions() -> None:
    results = {item.case_id: classify_contradiction(item) for item in build_stage132_fixture_evidence()}
    assert results["CEX-TRUE-001"].classification == "true_contradiction"
    assert results["CEX-TRUE-001"].requires_writer_approval is True
    assert results["CEX-MYST-001"].classification == "intentional_mystery"
    assert results["CEX-MYST-001"].exemption_status == "exempted_by_reveal_lock"
    assert results["CEX-POV-001"].classification == "character_misunderstanding"
    assert results["CEX-DELAY-001"].classification == "reveal_delay"


def test_stage132_mystery_exemption_requires_lock_and_budget() -> None:
    result = run_stage132_contradiction_classifier(ROOT)
    mystery = result["parts"]["mystery_exemption"]
    assert mystery["status"] == "pass"
    assert mystery["mystery_exemption_policy"] == "requires_reveal_lock_and_payoff_budget"
    assert result["mystery_exemption_requires_reveal_lock"] is True


def test_stage132_keeps_gate26_advisory_not_hard_block() -> None:
    result = run_stage132_contradiction_classifier(ROOT)
    assert result["gate26_hard_block_enabled"] is False
    assert result["gate26_hard_block_count"] == 0
    assert result["auto_repair_mutation_count"] == 0
    assert result["canon_auto_resolution_count"] == 0


def test_stage132_preserves_provider_zero_and_raw_boundaries() -> None:
    result = run_stage132_contradiction_classifier(ROOT)
    assert result["provider_default_calls"] == 0
    assert result["live_provider_call_count_in_release_gate"] == 0
    assert result["raw_manuscript_provider_leakage"] == 0
    assert result["raw_manuscript_cross_project_leakage"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage132_gitnexus_fallback_and_branchpoints_survive() -> None:
    result = run_stage132_contradiction_classifier(ROOT)
    preflight = result["parts"]["gitnexus_preflight"]
    assert preflight["shape_check"]["status"] == "pass"
    assert preflight["python_fallback"]["status"] == "PASS"
    assert all(preflight["survival_matrix"].values())


def test_stage132_release_gate_passes() -> None:
    gate = run_stage132_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["mystery_exemption_guard_pass"]["status"] == "pass"
    assert gate["checks"]["true_contradiction_review_pass"]["status"] == "pass"
