from __future__ import annotations

import json
from pathlib import Path

from v1700.plan_graph_builder.builder import build_deterministic_plan_graph
from v1700.plan_graph_builder import run_stage157_deterministic_plan_graph_builder
from v1700.gates.stage157_release_gate import run_stage157_release_gate
from v1700.local_execution_packet_store.loader import load_execution_packets, compute_packet_checksum

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "samples/stage156_execution_packet_store/execution_packets.jsonl"


def _write_packets(path: Path, packets: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(packet, ensure_ascii=False) for packet in packets) + "\n", encoding="utf-8")


def test_stage157_builds_deterministic_dag() -> None:
    graph = build_deterministic_plan_graph(STORE)
    assert graph["status"] == "pass"
    assert graph["node_count"] >= 6
    assert graph["edge_count"] >= 5
    assert len(graph["graph_checksum"]) == 64
    assert graph["topological_order"][0] == "exec_pkt_project_bootstrap"


def test_stage157_topological_order_respects_dependencies() -> None:
    graph = build_deterministic_plan_graph(STORE)
    position = {packet_id: index for index, packet_id in enumerate(graph["topological_order"])}
    for packet in load_execution_packets(STORE):
        packet_id = packet["packet_id"]
        for dep in packet["dependency_ids"]:
            assert position[dep] < position[packet_id]


def test_stage157_report_blocks_runtime_privilege() -> None:
    result = run_stage157_deterministic_plan_graph_builder(ROOT)
    assert result["status"] == "pass"
    assert result["node_count"] >= 6
    assert result["runtime_execution_enabled"] is False
    assert result["graph_write_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage157_release_gate_passes() -> None:
    result = run_stage157_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["stage157"]["node_count"] >= 6
    assert result["graph_write_enabled"] is False
    assert result["runtime_execution_enabled"] is False


def test_stage157_missing_dependency_blocks(tmp_path: Path) -> None:
    store = tmp_path / "execution_packets.jsonl"
    packets = load_execution_packets(STORE)
    packets[0]["dependency_ids"] = ["missing_packet"]
    packets[0]["checksum"] = compute_packet_checksum(packets[0])
    _write_packets(store, packets)
    graph = build_deterministic_plan_graph(store)
    assert graph["status"] == "blocked"
    assert any(issue.startswith("missing_dependency") for issue in graph["issues"])


def test_stage157_cycle_blocks(tmp_path: Path) -> None:
    store = tmp_path / "execution_packets.jsonl"
    packets = load_execution_packets(STORE)
    packets[0]["dependency_ids"] = [packets[-1]["packet_id"]]
    packets[0]["checksum"] = compute_packet_checksum(packets[0])
    _write_packets(store, packets)
    graph = build_deterministic_plan_graph(store)
    assert graph["status"] == "blocked"
    assert any(issue.startswith("cycle_detected") for issue in graph["issues"])
