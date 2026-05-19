from __future__ import annotations

from pathlib import Path

from v1700.gig_advisory import run_stage131_gig_advisory
from v1700.gates.stage131_release_gate import run_stage131_release_gate

ROOT = Path(__file__).resolve().parents[1]


def test_stage131_gig_advisory_passes() -> None:
    result = run_stage131_gig_advisory(ROOT)
    assert result["status"] == "pass"
    assert result["advisory_mode"] == "GIG_GATE26_ADVISORY_ONLY"
    assert result["case_count"] == 4


def test_stage131_keeps_gate26_advisory_not_hard_block() -> None:
    result = run_stage131_gig_advisory(ROOT)
    assert result["gate26_hard_block_enabled"] is False
    assert result["gate26_hard_block_count"] == 0
    assert result["auto_repair_mutation_count"] == 0


def test_stage131_distinguishes_conflict_types() -> None:
    result = run_stage131_gig_advisory(ROOT)
    cases = {case["conflict_type"] for case in result["parts"]["classifier"]["cases"]}
    assert {"true_contradiction", "intentional_mystery", "character_misunderstanding", "reveal_delay"} <= cases
    assert result["true_contradiction_review_required"] is True


def test_stage131_preserves_provider_zero_and_raw_boundaries() -> None:
    result = run_stage131_gig_advisory(ROOT)
    assert result["provider_default_calls"] == 0
    assert result["live_provider_call_count_in_release_gate"] == 0
    assert result["raw_manuscript_provider_leakage"] == 0
    assert result["raw_manuscript_cross_project_leakage"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage131_gitnexus_fallback_and_branchpoints_survive() -> None:
    result = run_stage131_gig_advisory(ROOT)
    preflight = result["parts"]["gitnexus_preflight"]
    assert preflight["shape_check"]["status"] == "pass"
    assert preflight["python_fallback"]["status"] == "PASS"
    assert all(preflight["survival_matrix"].values())


def test_stage131_release_gate_passes() -> None:
    gate = run_stage131_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["gate26_advisory_only_pass"]["status"] == "pass"
    assert gate["checks"]["writer_approval_guard_pass"]["status"] == "pass"
