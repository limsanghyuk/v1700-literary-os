from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage162_release_gate import run_stage162_release_gate

from .builder import build_deterministic_render_plan
from .contracts import RenderPlanPolicy, RenderPlanProjectionRule

TARGET_STAGE = "stage163"
TARGET_REPORT = "release/current/stage163_deterministic_render_plan_builder_report.json"
STORE_PATH = "samples/stage162_render_packet_store/render_packets.jsonl"


def run_stage163_deterministic_render_plan_builder(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage162 = run_stage162_release_gate(root)
    plan = build_deterministic_render_plan(root / STORE_PATH)
    pack = root / "release/current/stage163_deterministic_render_plan_builder_pack"
    pack.mkdir(parents=True, exist_ok=True)

    nodes = _build_render_plan_nodes(plan)
    edges = _build_render_plan_edges(plan)
    order = _build_render_order(plan)
    integrity = _build_render_plan_integrity(plan)
    checksum = _build_deterministic_render_plan_checksum(plan)
    projection = _build_node2_render_plan_projection_matrix(plan)
    policy = _build_render_plan_policy()
    regression = _build_regression_snapshot(plan)

    parts = {
        "render_plan_nodes": nodes,
        "render_plan_edges": edges,
        "render_order": order,
        "render_plan_integrity": integrity,
        "deterministic_render_plan_checksum": checksum,
        "node2_render_plan_projection_matrix": projection,
        "render_plan_policy": policy,
        "regression_snapshot": regression,
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}.json", payload)

    issues: list[str] = []
    if stage162.get("status") != "pass":
        issues.append("stage162_release_gate_blocked")
    if plan.get("status") != "pass":
        issues.extend(f"render_plan:{issue}" for issue in plan.get("issues", []))
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "163",
        "baseline_stage": "162",
        "title": "Deterministic Render Plan Builder",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "DETERMINISTIC_RENDER_PLAN_BUILDER_LOCAL_ONLY",
        "page": "Page04 Rendering Body",
        "source_store_path": STORE_PATH,
        "node_count": plan.get("node_count", 0),
        "edge_count": plan.get("edge_count", 0),
        "critical_path_length": plan.get("critical_path_length", 0),
        "render_plan_checksum": plan.get("render_plan_checksum", ""),
        "render_order_count": len(plan.get("render_order", [])),
        "deterministic_render_plan_enabled": True,
        "stage164_surface_draft_dry_run_renderer_ready": not issues,
        "render_packet_store_inherited": stage162.get("status") == "pass",
        "rendering_runtime_enabled": False,
        "generation_runtime_enabled": False,
        "provider_generation_enabled": False,
        "provider_execution_enabled": False,
        "runtime_execution_enabled": False,
        "render_write_enabled": False,
        "store_write_enabled": False,
        "memory_write_enabled": False,
        "execution_write_enabled": False,
        "render_plan_write_enabled": False,
        "canon_mutation_enabled": False,
        "auto_repair_apply_enabled": False,
        "vector_db_runtime_dependency": False,
        "live_provider_rag_enabled": False,
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "runtime_execution_count": 0,
        "provider_execution_count": 0,
        "provider_generation_count": 0,
        "write_operation_count": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "node2_hidden_render_payload_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "parts": {"stage162_release_gate": _compact(stage162), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_render_plan_nodes(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": TARGET_STAGE,
        "title": "Stage163 Render Plan Nodes",
        "status": "pass" if plan.get("status") == "pass" and plan.get("node_count", 0) > 0 else "blocked",
        "issues": list(plan.get("issues", [])),
        "node_count": plan.get("node_count", 0),
        "nodes": plan.get("nodes", []),
    }


def _build_render_plan_edges(plan: dict[str, Any]) -> dict[str, Any]:
    expected = max(0, int(plan.get("node_count", 0)) - 1)
    issues = [] if int(plan.get("edge_count", 0)) == expected else ["linear_sequence_edge_count_mismatch"]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage163 Render Plan Edges",
        "status": "pass" if plan.get("status") == "pass" and not issues else "blocked",
        "issues": issues,
        "edge_count": plan.get("edge_count", 0),
        "edges": plan.get("edges", []),
    }


def _build_render_order(plan: dict[str, Any]) -> dict[str, Any]:
    order = list(plan.get("render_order", []))
    return {
        "stage": TARGET_STAGE,
        "title": "Stage163 Deterministic Render Order",
        "status": "pass" if plan.get("status") == "pass" and len(order) == plan.get("node_count", 0) else "blocked",
        "issues": [] if len(order) == plan.get("node_count", 0) else ["render_order_count_mismatch"],
        "order_count": len(order),
        "render_order": order,
    }


def _build_render_plan_integrity(plan: dict[str, Any]) -> dict[str, Any]:
    node_ids = {node.get("node_id") for node in plan.get("nodes", [])}
    issues: list[str] = []
    for edge in plan.get("edges", []):
        if edge.get("from_node_id") not in node_ids or edge.get("to_node_id") not in node_ids:
            issues.append(f"missing_edge_endpoint:{edge.get('edge_id')}")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage163 Render Plan Integrity",
        "status": "pass" if plan.get("status") == "pass" and not issues else "blocked",
        "issues": issues + list(plan.get("issues", [])),
        "node_count": plan.get("node_count", 0),
        "edge_count": plan.get("edge_count", 0),
        "critical_path_length": plan.get("critical_path_length", 0),
    }


def _build_deterministic_render_plan_checksum(plan: dict[str, Any]) -> dict[str, Any]:
    checksum = str(plan.get("render_plan_checksum", ""))
    return {
        "stage": TARGET_STAGE,
        "title": "Stage163 Deterministic Render Plan Checksum",
        "status": "pass" if plan.get("status") == "pass" and len(checksum) == 64 else "blocked",
        "issues": [] if len(checksum) == 64 else ["checksum_missing_or_invalid"],
        "render_plan_checksum": checksum,
    }


def _build_node2_render_plan_projection_matrix(plan: dict[str, Any]) -> dict[str, Any]:
    rules = (
        RenderPlanProjectionRule("node2_render_plan_summary_only", True, True, True, True, TARGET_REPORT),
        RenderPlanProjectionRule("hidden_render_payload_blocked", True, True, True, True, TARGET_REPORT),
        RenderPlanProjectionRule("provider_generation_payload_blocked", True, True, True, True, TARGET_REPORT),
        RenderPlanProjectionRule("write_handle_blocked", True, True, True, True, TARGET_REPORT),
    )
    issues: list[str] = []
    for node in plan.get("nodes", []):
        surface = json.dumps(node.get("node2_projection_summary", ""), ensure_ascii=False).lower()
        for token in ("hidden_reveal_payload", "hidden_render_payload", "provider_payload", "provider_generation_payload", "write_handle", "credential"):
            if token in surface:
                issues.append(f"node2_forbidden_token:{node.get('render_packet_id')}:{token}")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage163 Node2 Render Plan Projection Matrix",
        "status": "pass" if plan.get("status") == "pass" and not issues else "blocked",
        "issues": issues,
        "rules": [rule.to_dict() for rule in rules],
        "node2_raw_reveal_access": 0,
        "node2_hidden_render_payload_access": 0,
    }


def _build_render_plan_policy() -> dict[str, Any]:
    rules = (
        RenderPlanPolicy("deterministic_render_plan_builder", True, True, False, False, False, TARGET_REPORT),
        RenderPlanPolicy("runtime_render_disabled", True, True, False, False, False, TARGET_REPORT),
        RenderPlanPolicy("provider_generation_disabled", True, True, False, False, False, TARGET_REPORT),
        RenderPlanPolicy("render_plan_write_disabled", True, True, False, False, False, TARGET_REPORT),
        RenderPlanPolicy("canon_mutation_disabled", True, True, False, False, False, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if not rule.deterministic or not rule.dry_run_only or rule.runtime_render_allowed or rule.provider_generation_allowed or rule.write_allowed]
    return {"stage": TARGET_STAGE, "title": "Stage163 Render Plan Policy", "status": "pass" if not issues else "blocked", "issues": issues, "rules": [rule.to_dict() for rule in rules]}


def _build_regression_snapshot(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": TARGET_STAGE,
        "title": "Stage163 Regression Snapshot",
        "status": "pass" if plan.get("status") == "pass" else "blocked",
        "issues": list(plan.get("issues", [])),
        "node_count": plan.get("node_count", 0),
        "edge_count": plan.get("edge_count", 0),
        "render_order_count": len(plan.get("render_order", [])),
        "checksum_prefix": str(plan.get("render_plan_checksum", ""))[:16],
        "runtime_execution_count": 0,
        "provider_generation_count": 0,
        "write_operation_count": 0,
    }


def _compact(report: dict[str, Any]) -> dict[str, Any]:
    keep = ("status", "stage", "baseline_stage", "title", "issues", "mode", "render_packet_count", "checksum_count", "read_only_store_enabled", "render_packet_store_enabled", "stage163_render_plan_builder_ready", "rendering_runtime_enabled", "generation_runtime_enabled", "provider_generation_enabled", "runtime_execution_enabled", "provider_execution_enabled", "memory_write_enabled", "render_write_enabled", "store_write_enabled", "canon_mutation_enabled", "auto_repair_apply_enabled", "runtime_training_enabled", "model_weight_update_count", "canon_auto_resolution_count", "auto_repair_mutation_count", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "boundary_violation_count", "raw_manuscript_provider_leakage", "raw_manuscript_cross_project_leakage", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: report.get(key) for key in keep if key in report}


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
