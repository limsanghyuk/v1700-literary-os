from __future__ import annotations

import hashlib
import json
from typing import Any

from .contracts import DryRunTraceStep

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


def build_execution_dry_run_trace(stage157_report: dict[str, Any], stage158_report: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    if stage157_report.get("status") != "pass":
        issues.append("stage157_report_not_pass")
    if stage158_report.get("status") != "pass":
        issues.append("stage158_report_not_pass")
    if stage158_report.get("conflict_count", 0) != 0:
        issues.append("stage158_conflicts_present")
    if stage158_report.get("boundary_violation_count", 0) != 0:
        issues.append("stage158_boundary_violations_present")

    graph_parts = stage157_report.get("parts", {})
    nodes = list(graph_parts.get("plan_graph_nodes", {}).get("nodes", []))
    dependency_map = dict(graph_parts.get("dependency_integrity", {}).get("dependency_map", {}))
    order = list(graph_parts.get("topological_order", {}).get("topological_order", []))
    node_by_packet = {str(node.get("packet_id")): node for node in nodes}

    if not order:
        issues.append("empty_topological_order")
    if len(order) != len(nodes):
        issues.append("topological_order_node_count_mismatch")
    if len(order) != len(set(order)):
        issues.append("duplicate_packet_in_trace_order")

    seen: set[str] = set()
    steps: list[DryRunTraceStep] = []
    replay_records: list[dict[str, Any]] = []
    for index, packet_id in enumerate(order):
        packet_id = str(packet_id)
        node = node_by_packet.get(packet_id)
        if node is None:
            issues.append(f"trace_missing_node:{packet_id}")
            continue
        deps = tuple(str(dep) for dep in dependency_map.get(packet_id, []))
        missing_prior = sorted(dep for dep in deps if dep not in seen)
        if missing_prior:
            issues.append(f"trace_dependency_not_satisfied:{packet_id}:{','.join(missing_prior)}")
        packet_type = str(node.get("packet_type", ""))
        if packet_type in FORBIDDEN_PACKET_TYPES:
            issues.append(f"forbidden_packet_type:{packet_id}:{packet_type}")
        surface = str(node.get("node2_projection_summary", ""))
        hits = sorted(token for token in FORBIDDEN_NODE2_TOKENS if token in surface.lower())
        if hits:
            issues.extend(f"node2_forbidden_token:{packet_id}:{token}" for token in hits)
        step_payload = {
            "step_index": index,
            "packet_id": packet_id,
            "node_id": node.get("node_id", ""),
            "packet_type": packet_type,
            "dependency_ids": list(deps),
            "dry_run_action": "validate_noop_execution_plan",
            "status": "pass" if not missing_prior and not hits and packet_type not in FORBIDDEN_PACKET_TYPES else "blocked",
        }
        step_checksum = _stable_checksum(step_payload)
        trace_id = f"dry_run_step_{index:03d}_{packet_id}"
        steps.append(DryRunTraceStep(
            trace_id=trace_id,
            step_index=index,
            packet_id=packet_id,
            node_id=str(node.get("node_id", "")),
            packet_type=packet_type,
            boundary_level=str(node.get("boundary_level", "")),
            dependency_ids=deps,
            dry_run_action="validate_noop_execution_plan",
            status=step_payload["status"],
            node2_projection_summary=surface,
            checksum=step_checksum,
        ))
        replay_records.append({"trace_id": trace_id, "packet_id": packet_id, "checksum": step_checksum})
        seen.add(packet_id)

    canonical = {
        "source_graph_checksum": stage157_report.get("graph_checksum", ""),
        "source_preflight_checksum": stage158_report.get("preflight_checksum", ""),
        "steps": [step.to_dict() for step in steps],
    }
    trace_checksum = _stable_checksum(canonical)
    return {
        "status": "pass" if not issues else "blocked",
        "issues": sorted(set(issues)),
        "trace_step_count": len(steps),
        "dry_run_trace": [step.to_dict() for step in steps],
        "replay_records": replay_records,
        "trace_checksum": trace_checksum,
        "source_graph_checksum": stage157_report.get("graph_checksum", ""),
        "source_preflight_checksum": stage158_report.get("preflight_checksum", ""),
        "runtime_execution_count": 0,
        "provider_execution_count": 0,
        "write_operation_count": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": len([issue for issue in issues if issue.startswith("node2_") or issue.startswith("trace_dependency")]),
    }


def _stable_checksum(payload: dict[str, Any]) -> str:
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()
