from __future__ import annotations

from pathlib import Path

from v1700.execution_dry_run_trace import run_stage159_execution_dry_run_trace
from v1700.gates.stage159_release_gate import run_stage159_release_gate
from v1700.execution_dry_run_trace.tracer import build_execution_dry_run_trace

ROOT = Path(__file__).resolve().parents[1]


def test_stage159_report_passes() -> None:
    result = run_stage159_execution_dry_run_trace(ROOT)
    assert result["status"] == "pass"
    assert result["trace_step_count"] >= 6
    assert len(result["trace_checksum"]) == 64
    assert result["runtime_execution_count"] == 0
    assert result["provider_execution_count"] == 0
    assert result["write_operation_count"] == 0
    assert result["stage160_page03_release_seal_ready"] is True


def test_stage159_release_gate_passes() -> None:
    result = run_stage159_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["runtime_execution_count"] == 0
    assert result["provider_execution_count"] == 0
    assert result["write_operation_count"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["boundary_violation_count"] == 0


def test_stage159_replay_ledger_is_deterministic() -> None:
    result = run_stage159_execution_dry_run_trace(ROOT)
    ledger = result["parts"]["trace_replay_ledger"]
    assert ledger["status"] == "pass"
    checksums = [record["checksum"] for record in ledger["records"]]
    assert len(checksums) == len(set(checksums))


def test_stage159_blocks_forbidden_node2_projection() -> None:
    stage157 = {
        "status": "pass",
        "graph_checksum": "a" * 64,
        "parts": {
            "plan_graph_nodes": {"nodes": [{"packet_id": "p1", "node_id": "n1", "packet_type": "scene_plan", "boundary_level": "PUBLIC_SURFACE", "node2_projection_summary": "hidden_reveal_payload"}]},
            "dependency_integrity": {"dependency_map": {"p1": []}},
            "topological_order": {"topological_order": ["p1"]},
        },
    }
    stage158 = {"status": "pass", "conflict_count": 0, "boundary_violation_count": 0, "preflight_checksum": "b" * 64}
    trace = build_execution_dry_run_trace(stage157, stage158)
    assert trace["status"] == "blocked"
    assert any("node2_forbidden_token:p1:hidden_reveal_payload" in issue for issue in trace["issues"])


def test_stage159_blocks_unsatisfied_dependency() -> None:
    stage157 = {
        "status": "pass",
        "graph_checksum": "a" * 64,
        "parts": {
            "plan_graph_nodes": {"nodes": [
                {"packet_id": "p1", "node_id": "n1", "packet_type": "scene_plan", "boundary_level": "PUBLIC_SURFACE", "node2_projection_summary": "surface"},
                {"packet_id": "p2", "node_id": "n2", "packet_type": "scene_plan", "boundary_level": "PUBLIC_SURFACE", "node2_projection_summary": "surface"},
            ]},
            "dependency_integrity": {"dependency_map": {"p1": ["p2"], "p2": []}},
            "topological_order": {"topological_order": ["p1", "p2"]},
        },
    }
    stage158 = {"status": "pass", "conflict_count": 0, "boundary_violation_count": 0, "preflight_checksum": "b" * 64}
    trace = build_execution_dry_run_trace(stage157, stage158)
    assert trace["status"] == "blocked"
    assert any("trace_dependency_not_satisfied:p1:p2" in issue for issue in trace["issues"])


def test_stage159_side_effect_policy_is_frozen() -> None:
    result = run_stage159_execution_dry_run_trace(ROOT)
    policy = result["parts"]["side_effect_free_policy"]
    assert policy["status"] == "pass"
    for rule in policy["rules"]:
        assert rule["enabled"] is False
        assert rule["must_remain_disabled"] is True
