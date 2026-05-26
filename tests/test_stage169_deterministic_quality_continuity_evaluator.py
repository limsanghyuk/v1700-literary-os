from __future__ import annotations

import json
from pathlib import Path

from v1700.evaluation_engine.report import _score_packet, _load_rubric, _metric_catalog, _thresholds, run_stage169_deterministic_evaluator
from v1700.evaluation_packet_store.loader import load_evaluation_packets
from v1700.gates.stage169_release_gate import run_stage169_release_gate

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "samples/stage168_evaluation_packet_store/evaluation_packets.jsonl"


def test_stage169_deterministic_evaluator_passes() -> None:
    result = run_stage169_deterministic_evaluator(ROOT)
    assert result["status"] == "pass"
    assert result["quality_channel_pass"] is True
    assert result["continuity_channel_pass"] is True
    assert result["regression_channel_pass"] is True
    assert result["boundary_channel_pass"] is True
    assert result["determinism_channel_pass"] is True
    assert result["stage170_regression_harness_ready"] is True
    assert result["provider_default_calls"] == 0
    assert result["provider_evaluation_enabled"] is False
    assert result["evaluation_write_enabled"] is False
    assert result["node2_raw_reveal_access"] == 0


def test_stage169_release_gate_passes() -> None:
    result = run_stage169_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["stage169"]["quality_channel_pass"] is True
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["evaluation_write_enabled"] is False


def test_stage169_scorecards_are_deterministic() -> None:
    packets = load_evaluation_packets(STORE)
    rubric = _load_rubric(ROOT)
    metrics = _metric_catalog(rubric)
    thresholds = _thresholds(rubric)
    first = [_score_packet(packet, metrics, thresholds, ROOT).deterministic_checksum for packet in packets]
    second = [_score_packet(packet, metrics, thresholds, ROOT).deterministic_checksum for packet in packets]
    assert first == second


def test_stage169_boundary_override_blocks_even_with_high_score() -> None:
    packet = load_evaluation_packets(STORE)[0]
    packet["node2_projection_summary"] = "surface-safe summary with raw_reveal provider_handle"
    rubric = _load_rubric(ROOT)
    card = _score_packet(packet, _metric_catalog(rubric), _thresholds(rubric), ROOT)
    assert card.boundary_violation_count > 0
    assert card.status == "blocked"
    assert "boundary_violation_detected" in card.block_reasons


def test_stage169_missing_reference_blocks_continuity() -> None:
    packet = load_evaluation_packets(STORE)[0]
    packet["required_stage_refs"] = ["release/current/missing_stage_ref.json"]
    rubric = _load_rubric(ROOT)
    card = _score_packet(packet, _metric_catalog(rubric), _thresholds(rubric), ROOT)
    assert card.continuity_violation_index > 0
    assert card.status == "blocked"
    assert "continuity_hard_violation" in card.block_reasons


def test_stage169_outputs_release_evidence_files() -> None:
    run_stage169_deterministic_evaluator(ROOT)
    expected = [
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/evaluation_metric_matrix.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/quality_continuity_scorecard.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/continuity_violation_matrix.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/boundary_override_matrix.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/regression_delta_matrix.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/node2_evaluation_projection_verdict.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/determinism_matrix.json",
        "release/current/stage169_deterministic_quality_continuity_evaluator_pack/stage170_entry_criteria.json",
    ]
    assert all((ROOT / rel).exists() for rel in expected)
