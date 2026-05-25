from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from v1700.local_execution_packet_store.loader import validate_execution_packet_store
from .contracts import PlanGraphEdge, PlanGraphNode

FORBIDDEN_NODE2_TOKENS = (
    "hidden_reveal_payload",
    "private_note",
    "write_handle",
    "canon_mutation_command",
    "learning_payload",
    "raw_manuscript_payload",
    "credential",
    "provider_payload",
)


def build_deterministic_plan_graph(store_path: Path) -> dict[str, Any]:
    validation = validate_execution_packet_store(store_path)
    issues: list[str] = []
    if validation.get("status") != "pass":
        issues.extend(f"packet_store:{issue}" for issue in validation.get("issues", []))
        return _blocked(issues, validation)

    packets = sorted(validation.get("packets", []), key=lambda packet: str(packet.get("packet_id", "")))
    by_id = {str(packet["packet_id"]): packet for packet in packets}
    dependencies: dict[str, tuple[str, ...]] = {
        packet_id: tuple(str(dep) for dep in packet.get("dependency_ids", []))
        for packet_id, packet in by_id.items()
    }

    for packet_id, deps in dependencies.items():
        for dep in deps:
            if dep == packet_id:
                issues.append(f"self_dependency:{packet_id}")
            if dep not in by_id:
                issues.append(f"missing_dependency:{packet_id}:{dep}")

    dependents: dict[str, list[str]] = defaultdict(list)
    indegree = {packet_id: 0 for packet_id in by_id}
    for packet_id, deps in dependencies.items():
        for dep in deps:
            if dep in by_id and dep != packet_id:
                dependents[dep].append(packet_id)
                indegree[packet_id] += 1

    ready = sorted(packet_id for packet_id, degree in indegree.items() if degree == 0)
    order: list[str] = []
    while ready:
        current = ready.pop(0)
        order.append(current)
        for child in sorted(dependents.get(current, [])):
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
                ready.sort()
    if len(order) != len(by_id):
        unresolved = sorted(packet_id for packet_id in by_id if packet_id not in order)
        issues.append(f"cycle_detected:{','.join(unresolved)}")

    levels: dict[str, int] = {}
    for packet_id in order:
        deps = [dep for dep in dependencies[packet_id] if dep in by_id]
        levels[packet_id] = 0 if not deps else max(levels.get(dep, 0) for dep in deps) + 1

    nodes = [
        PlanGraphNode(
            node_id=f"plan_node_{packet_id}",
            packet_id=packet_id,
            packet_type=str(by_id[packet_id].get("packet_type", "")),
            project_id=str(by_id[packet_id].get("project_id", "")),
            boundary_level=str(by_id[packet_id].get("boundary_level", "")),
            visibility=str(by_id[packet_id].get("visibility", "")),
            checksum=str(by_id[packet_id].get("checksum", "")),
            level=levels.get(packet_id, 0),
            node2_projection_summary=str(by_id[packet_id].get("node2_projection_summary", "")),
        )
        for packet_id in order
    ]
    edges = [
        PlanGraphEdge(
            edge_id=f"plan_edge_{dep}_to_{packet_id}",
            from_node_id=f"plan_node_{dep}",
            to_node_id=f"plan_node_{packet_id}",
            dependency_type="packet_dependency",
        )
        for packet_id in order
        for dep in sorted(dependencies[packet_id])
        if dep in by_id and dep != packet_id
    ]

    node2_issues = _node2_projection_issues(nodes)
    issues.extend(node2_issues)
    canonical = {
        "nodes": [node.to_dict() for node in nodes],
        "edges": [edge.to_dict() for edge in sorted(edges, key=lambda edge: edge.edge_id)],
        "topological_order": order,
    }
    checksum = _stable_checksum(canonical)
    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "packet_store_status": validation.get("status"),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "topological_order": order,
        "critical_path_length": max((node.level for node in nodes), default=0) + (1 if nodes else 0),
        "graph_checksum": checksum,
        "nodes": [node.to_dict() for node in nodes],
        "edges": [edge.to_dict() for edge in sorted(edges, key=lambda edge: edge.edge_id)],
        "dependency_map": {packet_id: list(deps) for packet_id, deps in sorted(dependencies.items())},
    }


def _node2_projection_issues(nodes: list[PlanGraphNode]) -> list[str]:
    issues: list[str] = []
    for node in nodes:
        surface = node.node2_projection_summary.lower()
        for token in FORBIDDEN_NODE2_TOKENS:
            if token in surface:
                issues.append(f"node2_forbidden_token:{node.packet_id}:{token}")
    return issues


def _stable_checksum(payload: dict[str, Any]) -> str:
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _blocked(issues: list[str], validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "blocked",
        "issues": issues,
        "packet_store_status": validation.get("status"),
        "node_count": 0,
        "edge_count": 0,
        "topological_order": [],
        "critical_path_length": 0,
        "graph_checksum": "",
        "nodes": [],
        "edges": [],
        "dependency_map": {},
    }
