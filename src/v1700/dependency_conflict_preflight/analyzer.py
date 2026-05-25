from __future__ import annotations

import hashlib
import json
from itertools import combinations
from pathlib import Path
from typing import Any

from .contracts import BoundaryPreflightRule, ConflictRule, DependencyOrderFinding

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

FORBIDDEN_PACKET_TYPES = {
    "provider_execution",
    "memory_write",
    "canon_mutation",
    "runtime_training",
    "auto_repair_apply",
}

CONFLICT_RULES = (
    ConflictRule("provider_execution_conflict", "provider_execution", "*", True, "Provider execution cannot appear in Page03 preflight."),
    ConflictRule("memory_write_conflict", "memory_write", "*", True, "Memory write cannot appear in Page03 preflight."),
    ConflictRule("canon_mutation_conflict", "canon_mutation", "*", True, "Canon mutation cannot appear in Page03 preflight."),
    ConflictRule("runtime_training_conflict", "runtime_training", "*", True, "Runtime training cannot appear in Page03 preflight."),
)


def analyze_dependency_conflict_preflight(stage157_report: dict[str, Any]) -> dict[str, Any]:
    graph_parts = stage157_report.get("parts", {})
    nodes = list(graph_parts.get("plan_graph_nodes", {}).get("nodes", []))
    dependency_map = dict(graph_parts.get("dependency_integrity", {}).get("dependency_map", {}))
    topological_order = list(graph_parts.get("topological_order", {}).get("topological_order", []))
    issues: list[str] = []

    node_by_packet = {str(node.get("packet_id")): node for node in nodes}
    order_index = {str(packet_id): index for index, packet_id in enumerate(topological_order)}

    order_findings, order_issues = _dependency_order_findings(dependency_map, node_by_packet, order_index)
    conflict_matrix, conflict_issues = _conflict_matrix(nodes)
    boundary_rules, boundary_issues = _boundary_preflight(nodes, dependency_map, order_index)
    node2_matrix, node2_issues = _node2_projection_matrix(nodes)

    issues.extend(order_issues)
    issues.extend(conflict_issues)
    issues.extend(boundary_issues)
    issues.extend(node2_issues)

    canonical = {
        "dependency_order_findings": [finding.to_dict() for finding in order_findings],
        "conflict_matrix": conflict_matrix,
        "boundary_rules": [rule.to_dict() for rule in boundary_rules],
        "node2_matrix": node2_matrix,
        "source_graph_checksum": stage157_report.get("graph_checksum", ""),
    }
    return {
        "status": "pass" if not issues else "blocked",
        "issues": sorted(set(issues)),
        "dependency_order_findings": [finding.to_dict() for finding in order_findings],
        "conflict_matrix": conflict_matrix,
        "boundary_preflight_rules": [rule.to_dict() for rule in boundary_rules],
        "node2_conflict_projection_matrix": node2_matrix,
        "packet_count": len(nodes),
        "dependency_count": sum(len(deps) for deps in dependency_map.values()),
        "conflict_count": len(conflict_issues),
        "boundary_violation_count": len(boundary_issues) + len(node2_issues),
        "preflight_checksum": _stable_checksum(canonical),
    }


def _dependency_order_findings(
    dependency_map: dict[str, Any],
    node_by_packet: dict[str, dict[str, Any]],
    order_index: dict[str, int],
) -> tuple[list[DependencyOrderFinding], list[str]]:
    findings: list[DependencyOrderFinding] = []
    issues: list[str] = []
    for packet_id in sorted(dependency_map):
        if packet_id not in node_by_packet:
            issues.append(f"unknown_packet_in_dependency_map:{packet_id}")
        for dependency_id in sorted(str(dep) for dep in dependency_map.get(packet_id, [])):
            if dependency_id not in node_by_packet:
                findings.append(DependencyOrderFinding(packet_id, dependency_id, "blocked", "missing_dependency"))
                issues.append(f"missing_dependency:{packet_id}:{dependency_id}")
                continue
            if dependency_id == packet_id:
                findings.append(DependencyOrderFinding(packet_id, dependency_id, "blocked", "self_dependency"))
                issues.append(f"self_dependency:{packet_id}")
                continue
            if order_index.get(dependency_id, -1) >= order_index.get(packet_id, -1):
                findings.append(DependencyOrderFinding(packet_id, dependency_id, "blocked", "dependency_order_violation"))
                issues.append(f"dependency_order_violation:{packet_id}:{dependency_id}")
                continue
            findings.append(DependencyOrderFinding(packet_id, dependency_id, "pass", "dependency_precedes_packet"))
    return findings, issues


def _conflict_matrix(nodes: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    issues: list[str] = []
    packet_types = {str(node.get("packet_type", "")) for node in nodes}
    matrix: list[dict[str, Any]] = []
    for rule in CONFLICT_RULES:
        left_present = rule.left_packet_type in packet_types
        right_present = rule.right_packet_type == "*" or rule.right_packet_type in packet_types
        violated = rule.blocked and left_present and right_present
        if violated:
            issues.append(f"conflict_rule:{rule.name}:{rule.left_packet_type}")
        row = rule.to_dict()
        row.update({"left_present": left_present, "right_present": right_present, "status": "blocked" if violated else "pass"})
        matrix.append(row)
    for left, right in combinations(sorted(packet_types), 2):
        if left in FORBIDDEN_PACKET_TYPES or right in FORBIDDEN_PACKET_TYPES:
            issues.append(f"forbidden_packet_type_pair:{left}:{right}")
    return matrix, issues


def _boundary_preflight(
    nodes: list[dict[str, Any]],
    dependency_map: dict[str, Any],
    order_index: dict[str, int],
) -> tuple[list[BoundaryPreflightRule], list[str]]:
    issues: list[str] = []
    rules: list[BoundaryPreflightRule] = []
    for node in sorted(nodes, key=lambda item: str(item.get("packet_id", ""))):
        packet_id = str(node.get("packet_id", ""))
        boundary = str(node.get("boundary_level", ""))
        packet_type = str(node.get("packet_type", ""))
        if packet_type in FORBIDDEN_PACKET_TYPES:
            rules.append(BoundaryPreflightRule("forbidden_packet_type", packet_id, boundary, "blocked", packet_type))
            issues.append(f"forbidden_packet_type:{packet_id}:{packet_type}")
            continue
        if boundary == "HIDDEN_REVEAL_GUARD":
            deps = [str(dep) for dep in dependency_map.get(packet_id, [])]
            if not deps:
                rules.append(BoundaryPreflightRule("hidden_guard_requires_dependency", packet_id, boundary, "blocked", "guarded packet must depend on prior surface plan"))
                issues.append(f"hidden_guard_without_dependency:{packet_id}")
                continue
            if any(order_index.get(dep, -1) >= order_index.get(packet_id, -1) for dep in deps):
                rules.append(BoundaryPreflightRule("hidden_guard_dependency_order", packet_id, boundary, "blocked", "guard dependency must precede guarded packet"))
                issues.append(f"hidden_guard_order_violation:{packet_id}")
                continue
            rules.append(BoundaryPreflightRule("hidden_guard_dependency_order", packet_id, boundary, "pass", "guard dependencies precede hidden guard"))
        else:
            rules.append(BoundaryPreflightRule("surface_or_guarded_boundary", packet_id, boundary, "pass", "boundary is preflight-safe"))
    return rules, issues


def _node2_projection_matrix(nodes: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    issues: list[str] = []
    rows: list[dict[str, Any]] = []
    for node in sorted(nodes, key=lambda item: str(item.get("packet_id", ""))):
        packet_id = str(node.get("packet_id", ""))
        summary = str(node.get("node2_projection_summary", "")).lower()
        hits = sorted(token for token in FORBIDDEN_NODE2_TOKENS if token in summary)
        if hits:
            issues.extend(f"node2_forbidden_token:{packet_id}:{token}" for token in hits)
        rows.append({
            "packet_id": packet_id,
            "node_id": node.get("node_id", ""),
            "node2_surface_allowed": not hits,
            "forbidden_token_hits": hits,
            "status": "pass" if not hits else "blocked",
        })
    return rows, issues


def _stable_checksum(payload: dict[str, Any]) -> str:
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()
