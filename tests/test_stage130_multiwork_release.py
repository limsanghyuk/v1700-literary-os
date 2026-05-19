from __future__ import annotations

from pathlib import Path

from v1700.multiwork_release import run_stage130_multiwork_release
from v1700.gates.stage130_release_gate import run_stage130_release_gate

ROOT = Path(__file__).resolve().parents[1]


def test_stage130_multiwork_release_passes() -> None:
    result = run_stage130_multiwork_release(ROOT)
    assert result["status"] == "pass"
    assert result["multiwork_release_authorized"] is True


def test_stage130_preserves_stage127_to_stage129_evidence() -> None:
    result = run_stage130_multiwork_release(ROOT)
    assert result["stage127_to_stage129_evidence_preserved"] is True
    assert result["stage127_preflight_pass"] is True
    assert result["stage128_read_only_absorption_pass"] is True
    assert result["stage129_cim_governor_pass"] is True


def test_stage130_blocks_write_and_raw_text_surfaces() -> None:
    result = run_stage130_multiwork_release(ROOT)
    assert result["direct_v571_merge_detected"] is False
    assert result["cross_project_write_allowed"] is False
    assert result["raw_manuscript_cross_project_leakage"] == 0
    assert result["full_text_exported"] is False


def test_stage130_defers_gate26_hard_block_to_stage131() -> None:
    result = run_stage130_multiwork_release(ROOT)
    assert result["stage131_gig_advisory_required"] is True
    assert result["gate26_hard_block_enabled"] is False


def test_stage130_gitnexus_python_fallback_survives() -> None:
    result = run_stage130_multiwork_release(ROOT)
    preflight = result["parts"]["gitnexus_preflight"]
    assert preflight["shape_check"]["status"] == "pass"
    assert preflight["python_fallback"]["status"] == "PASS"
    assert all(preflight["survival_matrix"].values())


def test_stage130_release_gate_passes() -> None:
    gate = run_stage130_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["multiwork_release_authorized"]["status"] == "pass"
