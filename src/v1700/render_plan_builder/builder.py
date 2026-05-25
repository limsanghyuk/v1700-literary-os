from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from v1700.local_render_packet_store.loader import validate_render_packet_store

from .contracts import RenderPlanEdge, RenderPlanNode

FORBIDDEN_NODE2_TOKENS = (
    "hidden_reveal_payload",
    "hidden_render_payload",
    "private_note",
    "provider handle",
    "provider_handle",
    "provider_payload",
    "provider_generation_payload",
    "write_handle",
    "canon_mutation_command",
    "learning_payload",
    "raw_manuscript_payload",
    "credential",
    "internal_trace_payload",
)

RENDER_TYPE_PRIORITY = {
    "synopsis_surface": 0,
    "scene_surface": 10,
    "beat_surface": 20,
    "dialogue_surface": 30,
    "stage_direction_surface": 40,
    "chapter_bridge_surface": 50,
}
SURFACE_CHANNEL_PRIORITY = {"synopsis": 0, "novel": 10, "drama": 20}


def build_deterministic_render_plan(store_path: Path) -> dict[str, Any]:
    validation = validate_render_packet_store(store_path)
    issues: list[str] = []
    if validation.get("status") != "pass":
        issues.extend(f"render_packet_store:{issue}" for issue in validation.get("issues", []))
        return _blocked(issues, validation)

    packets = sorted(
        validation.get("packets", []),
        key=lambda packet: (
            SURFACE_CHANNEL_PRIORITY.get(str(packet.get("surface_channel", "")), 999),
            RENDER_TYPE_PRIORITY.get(str(packet.get("render_type", "")), 999),
            str(packet.get("render_packet_id", "")),
        ),
    )
    by_id = {str(packet["render_packet_id"]): packet for packet in packets}
    if len(by_id) != len(packets):
        issues.append("duplicate_render_packet_id_after_validation")

    ordered_ids = [str(packet["render_packet_id"]) for packet in packets]
    nodes: list[RenderPlanNode] = []
    for level, packet_id in enumerate(ordered_ids):
        packet = by_id[packet_id]
        nodes.append(
            RenderPlanNode(
                node_id=f"render_plan_node_{packet_id}",
                render_packet_id=packet_id,
                render_type=str(packet.get("render_type", "")),
                project_id=str(packet.get("project_id", "")),
                surface_channel=str(packet.get("surface_channel", "")),
                boundary_level=str(packet.get("boundary_level", "")),
                visibility=str(packet.get("visibility", "")),
                render_mode=str(packet.get("render_mode", "")),
                checksum=str(packet.get("checksum", "")),
                level=level,
                node2_projection_summary=str(packet.get("node2_projection_summary", "")),
            )
        )

    edges: list[RenderPlanEdge] = []
    for index in range(1, len(ordered_ids)):
        previous_id = ordered_ids[index - 1]
        packet_id = ordered_ids[index]
        edges.append(
            RenderPlanEdge(
                edge_id=f"render_plan_edge_{previous_id}_to_{packet_id}",
                from_node_id=f"render_plan_node_{previous_id}",
                to_node_id=f"render_plan_node_{packet_id}",
                dependency_type="deterministic_render_sequence",
            )
        )

    issues.extend(_node2_projection_issues(nodes))
    if len(edges) != max(0, len(nodes) - 1):
        issues.append("edge_count_not_linearized")
    node_ids = {node.node_id for node in nodes}
    for edge in edges:
        if edge.from_node_id not in node_ids or edge.to_node_id not in node_ids:
            issues.append(f"missing_edge_endpoint:{edge.edge_id}")
    if _has_cycle([edge.to_dict() for edge in edges]):
        issues.append("cycle_detected")

    canonical = {
        "nodes": [node.to_dict() for node in nodes],
        "edges": [edge.to_dict() for edge in edges],
        "render_order": ordered_ids,
    }
    checksum = _stable_checksum(canonical)
    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "render_packet_store_status": validation.get("status"),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "render_order": ordered_ids,
        "critical_path_length": len(nodes),
        "render_plan_checksum": checksum,
        "nodes": [node.to_dict() for node in nodes],
        "edges": [edge.to_dict() for edge in edges],
        "source_packet_ids": ordered_ids,
        "source_checksum_count": len(validation.get("checksum_index", [])),
    }


def _node2_projection_issues(nodes: list[RenderPlanNode]) -> list[str]:
    issues: list[str] = []
    for node in nodes:
        surface = node.node2_projection_summary.lower()
        for token in FORBIDDEN_NODE2_TOKENS:
            if token in surface:
                issues.append(f"node2_forbidden_token:{node.render_packet_id}:{token}")
    return issues


def _has_cycle(edges: list[dict[str, str]]) -> bool:
    graph: dict[str, set[str]] = {}
    nodes: set[str] = set()
    for edge in edges:
        src = edge["from_node_id"]
        dst = edge["to_node_id"]
        graph.setdefault(src, set()).add(dst)
        nodes.update([src, dst])
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for child in graph.get(node, set()):
            if visit(child):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in sorted(nodes))


def _stable_checksum(payload: dict[str, Any]) -> str:
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _blocked(issues: list[str], validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "blocked",
        "issues": issues,
        "render_packet_store_status": validation.get("status"),
        "node_count": 0,
        "edge_count": 0,
        "render_order": [],
        "critical_path_length": 0,
        "render_plan_checksum": "",
        "nodes": [],
        "edges": [],
        "source_packet_ids": [],
        "source_checksum_count": 0,
    }
