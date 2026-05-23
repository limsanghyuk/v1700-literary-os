from __future__ import annotations

from pathlib import Path

from v1700.gates.stage153_release_gate import run_stage153_release_gate
from v1700.memory_health_boundary import run_stage153_memory_health_leakage_boundary

ROOT = Path(__file__).resolve().parents[1]


def test_stage153_memory_health_report_passes() -> None:
    result = run_stage153_memory_health_leakage_boundary(ROOT)
    assert result["status"] == "pass"
    assert result["health_monitor_enabled"] is True
    assert result["leakage_boundary_enabled"] is True
    assert result["boundary_violation_count"] == 0
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage153_leakage_scan_finds_no_forbidden_payloads() -> None:
    result = run_stage153_memory_health_leakage_boundary(ROOT)
    scan = result["parts"]["leakage_boundary_scan"]
    matrix = result["parts"]["node2_leakage_matrix"]
    assert scan["status"] == "pass"
    assert scan["total_leak_count"] == 0
    assert matrix["status"] == "pass"
    assert matrix["violation_count"] == 0


def test_stage153_query_boundary_probe_blocks_raw_reveals() -> None:
    result = run_stage153_memory_health_leakage_boundary(ROOT)
    probe = result["parts"]["query_boundary_probe"]
    assert probe["status"] == "pass"
    assert probe["probe_count"] >= 3
    assert probe["node2_raw_reveal_access"] == 0
    assert probe["blocked_projection_count"] >= 1


def test_stage153_release_gate_passes() -> None:
    result = run_stage153_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["memory_write_enabled"] is False
    assert result["runtime_training_enabled"] is False
