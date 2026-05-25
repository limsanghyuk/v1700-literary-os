from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from v1700.dependency_conflict_preflight.analyzer import analyze_dependency_conflict_preflight
from v1700.dependency_conflict_preflight import run_stage158_dependency_conflict_preflight
from v1700.gates.stage158_release_gate import run_stage158_release_gate

ROOT = Path(__file__).resolve().parents[1]


def _stage157_report() -> dict:
    import json
    return json.loads((ROOT / "release/current/stage157_deterministic_plan_graph_builder_report.json").read_text(encoding="utf-8"))


def test_stage158_dependency_conflict_preflight_passes() -> None:
    result = run_stage158_dependency_conflict_preflight(ROOT)
    assert result["status"] == "pass"
    assert result["conflict_count"] == 0
    assert result["boundary_violation_count"] == 0
    assert result["provider_default_calls"] == 0
    assert result["runtime_execution_enabled"] is False
    assert result["preflight_write_enabled"] is False
    assert len(result["preflight_checksum"]) == 64


def test_stage158_release_gate_preserves_page03_boundaries() -> None:
    result = run_stage158_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["boundary_violation_count"] == 0
    assert result["runtime_execution_enabled"] is False
    assert result["preflight_write_enabled"] is False


def test_stage158_detects_dependency_order_violation() -> None:
    report = _stage157_report()
    broken = deepcopy(report)
    broken["parts"]["topological_order"]["topological_order"] = list(reversed(broken["parts"]["topological_order"]["topological_order"]))
    result = analyze_dependency_conflict_preflight(broken)
    assert result["status"] == "blocked"
    assert any(issue.startswith("dependency_order_violation:") for issue in result["issues"])


def test_stage158_detects_forbidden_packet_type() -> None:
    report = _stage157_report()
    broken = deepcopy(report)
    broken["parts"]["plan_graph_nodes"]["nodes"][0]["packet_type"] = "provider_execution"
    result = analyze_dependency_conflict_preflight(broken)
    assert result["status"] == "blocked"
    assert any("provider_execution" in issue for issue in result["issues"])


def test_stage158_detects_node2_forbidden_projection_token() -> None:
    report = _stage157_report()
    broken = deepcopy(report)
    broken["parts"]["plan_graph_nodes"]["nodes"][0]["node2_projection_summary"] = "contains hidden_reveal_payload"
    result = analyze_dependency_conflict_preflight(broken)
    assert result["status"] == "blocked"
    assert any(issue.startswith("node2_forbidden_token:") for issue in result["issues"])


def test_stage158_connectivity_matrix_is_part_of_report() -> None:
    result = run_stage158_dependency_conflict_preflight(ROOT)
    matrix = result["parts"]["preflight_step15_connectivity_matrix"]
    assert matrix["status"] == "pass"
    assert matrix["check_count"] >= 8
