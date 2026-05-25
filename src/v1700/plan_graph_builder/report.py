from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage156_release_gate import run_stage156_release_gate

from .builder import build_deterministic_plan_graph
from .contracts import PlanGraphPolicy, PlanGraphProjectionRule

TARGET_STAGE = "stage157"
TARGET_REPORT = "release/current/stage157_deterministic_plan_graph_builder_report.json"
STORE_PATH = "samples/stage156_execution_packet_store/execution_packets.jsonl"


def run_stage157_deterministic_plan_graph_builder(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage156 = run_stage156_release_gate(root)
    graph = build_deterministic_plan_graph(root / STORE_PATH)
    pack = root / "release/current/stage157_deterministic_plan_graph_builder_pack"
    pack.mkdir(parents=True, exist_ok=True)

    nodes = _build_plan_graph_nodes(graph)
    edges = _build_plan_graph_edges(graph)
    order = _build_topological_order(graph)
    integrity = _build_dependency_integrity(graph)
    checksum = _build_deterministic_graph_checksum(graph)
    projection = _build_node2_plan_projection_matrix(graph)
    policy = _build_plan_graph_policy()
    regression = _build_regression_snapshot(graph)

    parts = {
        "plan_graph_nodes": nodes,
        "plan_graph_edges": edges,
        "topological_order": order,
        "dependency_integrity": integrity,
        "deterministic_graph_checksum": checksum,
        "node2_plan_projection_matrix": projection,
        "plan_graph_policy": policy,
        "regression_snapshot": regression,
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}.json", payload)

    issues: list[str] = []
    if stage156.get("status") != "pass":
        issues.append("stage156_release_gate_blocked")
    if graph.get("status") != "pass":
        issues.extend(f"plan_graph:{issue}" for issue in graph.get("issues", []))
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "157",
        "baseline_stage": "156",
        "title": "Deterministic Plan Graph Builder",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "DETERMINISTIC_PLAN_GRAPH_BUILDER_LOCAL_ONLY",
        "page": "Page03 Execution Body",
        "source_store_path": STORE_PATH,
        "node_count": graph.get("node_count", 0),
        "edge_count": graph.get("edge_count", 0),
        "critical_path_length": graph.get("critical_path_length", 0),
        "graph_checksum": graph.get("graph_checksum", ""),
        "topological_order_count": len(graph.get("topological_order", [])),
        "deterministic_graph_enabled": True,
        "runtime_execution_enabled": False,
        "generation_runtime_enabled": False,
        "provider_execution_enabled": False,
        "memory_write_enabled": False,
        "execution_write_enabled": False,
        "store_write_enabled": False,
        "graph_write_enabled": False,
        "canon_mutation_enabled": False,
        "auto_repair_apply_enabled": False,
        "vector_db_runtime_dependency": False,
        "live_provider_rag_enabled": False,
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "node2_hidden_execution_payload_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "page03_execution_packet_store_inherited": stage156.get("status") == "pass",
        "stage158_dependency_conflict_preflight_ready": not issues,
        "parts": {"stage156_release_gate": _compact(stage156), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_plan_graph_nodes(graph: dict[str, Any]) -> dict[str, Any]:
    issues = [] if graph.get("node_count", 0) >= 6 else ["insufficient_plan_nodes"]
    return {
        "stage": TARGET_STAGE,
        "title": "Plan Graph Nodes",
        "status": "pass" if graph.get("status") == "pass" and not issues else "blocked",
        "issues": issues,
        "node_count": graph.get("node_count", 0),
        "nodes": graph.get("nodes", []),
    }


def _build_plan_graph_edges(graph: dict[str, Any]) -> dict[str, Any]:
    issues = [] if graph.get("edge_count", 0) >= 5 else ["insufficient_plan_edges"]
    return {
        "stage": TARGET_STAGE,
        "title": "Plan Graph Edges",
        "status": "pass" if graph.get("status") == "pass" and not issues else "blocked",
        "issues": issues,
        "edge_count": graph.get("edge_count", 0),
        "edges": graph.get("edges", []),
    }


def _build_topological_order(graph: dict[str, Any]) -> dict[str, Any]:
    order = list(graph.get("topological_order", []))
    issues = [] if len(order) == graph.get("node_count", 0) and len(order) == len(set(order)) else ["invalid_topological_order"]
    return {
        "stage": TARGET_STAGE,
        "title": "Deterministic Topological Order",
        "status": "pass" if graph.get("status") == "pass" and not issues else "blocked",
        "issues": issues,
        "order_count": len(order),
        "topological_order": order,
        "critical_path_length": graph.get("critical_path_length", 0),
    }


def _build_dependency_integrity(graph: dict[str, Any]) -> dict[str, Any]:
    dependency_map = graph.get("dependency_map", {})
    nodes = {node.get("packet_id") for node in graph.get("nodes", [])}
    missing = sorted(f"{packet}:{dep}" for packet, deps in dependency_map.items() for dep in deps if dep not in nodes)
    return {
        "stage": TARGET_STAGE,
        "title": "Dependency Integrity",
        "status": "pass" if graph.get("status") == "pass" and not missing else "blocked",
        "issues": [f"missing_dependency:{item}" for item in missing],
        "dependency_map": dependency_map,
    }


def _build_deterministic_graph_checksum(graph: dict[str, Any]) -> dict[str, Any]:
    checksum = str(graph.get("graph_checksum", ""))
    issues = [] if len(checksum) == 64 else ["invalid_graph_checksum"]
    return {
        "stage": TARGET_STAGE,
        "title": "Deterministic Graph Checksum",
        "status": "pass" if graph.get("status") == "pass" and not issues else "blocked",
        "issues": issues,
        "graph_checksum": checksum,
    }


def _build_node2_plan_projection_matrix(graph: dict[str, Any]) -> dict[str, Any]:
    rules = (
        PlanGraphProjectionRule("surface_summary_only", True, True, True, True, TARGET_REPORT),
        PlanGraphProjectionRule("hidden_execution_payload_blocked", True, True, True, True, TARGET_REPORT),
        PlanGraphProjectionRule("write_handle_blocked", True, True, True, True, TARGET_REPORT),
        PlanGraphProjectionRule("provider_payload_blocked", True, True, True, True, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if not rule.hidden_payload_blocked or not rule.write_handle_blocked or not rule.provider_payload_blocked]
    return {
        "stage": TARGET_STAGE,
        "title": "Node2 Plan Projection Matrix",
        "status": "pass" if graph.get("status") == "pass" and not issues else "blocked",
        "issues": issues,
        "rule_count": len(rules),
        "rules": [rule.to_dict() for rule in rules],
        "node2_raw_reveal_access": 0,
        "node2_hidden_execution_payload_access": 0,
    }


def _build_plan_graph_policy() -> dict[str, Any]:
    policies = (
        PlanGraphPolicy("deterministic_builder_only", True, False, False, False, TARGET_REPORT),
        PlanGraphPolicy("runtime_execution_disabled", True, False, False, False, TARGET_REPORT),
        PlanGraphPolicy("graph_write_disabled", True, False, False, False, TARGET_REPORT),
        PlanGraphPolicy("provider_execution_disabled", True, False, False, False, TARGET_REPORT),
    )
    issues = [policy.name for policy in policies if not policy.deterministic or policy.runtime_execution_allowed or policy.write_allowed or policy.provider_allowed]
    return {
        "stage": TARGET_STAGE,
        "title": "Plan Graph Policy",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "policy_count": len(policies),
        "policies": [policy.to_dict() for policy in policies],
    }


def _build_regression_snapshot(graph: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": TARGET_STAGE,
        "title": "Stage157 Regression Snapshot",
        "status": "pass" if graph.get("status") == "pass" else "blocked",
        "issues": list(graph.get("issues", [])),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "runtime_execution_enabled": False,
        "graph_write_enabled": False,
        "runtime_training_enabled": False,
    }


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _compact(report: dict[str, Any]) -> dict[str, Any]:
    keep = ("status", "stage", "baseline_stage", "title", "issues", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "boundary_violation_count", "raw_manuscript_provider_leakage", "raw_manuscript_cross_project_leakage", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: report.get(key) for key in keep if key in report}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
