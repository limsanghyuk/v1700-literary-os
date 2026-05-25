from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage156_release_gate import run_stage156_release_gate
from v1700.stage157 import run_stage157

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage157_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage157":
        existing = _load_report(root, "stage157_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage157(root)
    parts = stage.get("parts", {})
    nodes = parts.get("plan_graph_nodes", {})
    edges = parts.get("plan_graph_edges", {})
    order = parts.get("topological_order", {})
    integrity = parts.get("dependency_integrity", {})
    checksum = parts.get("deterministic_graph_checksum", {})
    projection = parts.get("node2_plan_projection_matrix", {})
    policy = parts.get("plan_graph_policy", {})
    regression = parts.get("regression_snapshot", {})

    checks = {
        "stage156_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage157_report_pass": _check(stage.get("status") == "pass"),
        "deterministic_plan_graph_mode_pass": _check(stage.get("mode") == "DETERMINISTIC_PLAN_GRAPH_BUILDER_LOCAL_ONLY"),
        "plan_graph_nodes_pass": _check(nodes.get("status") == "pass" and nodes.get("node_count", 0) >= 6),
        "plan_graph_edges_pass": _check(edges.get("status") == "pass" and edges.get("edge_count", 0) >= 5),
        "topological_order_pass": _check(order.get("status") == "pass" and order.get("order_count", 0) == stage.get("node_count")),
        "dependency_integrity_pass": _check(integrity.get("status") == "pass"),
        "deterministic_checksum_pass": _check(checksum.get("status") == "pass" and len(str(stage.get("graph_checksum", ""))) == 64),
        "node2_plan_projection_pass": _check(projection.get("status") == "pass" and stage.get("node2_raw_reveal_access") == 0),
        "plan_graph_policy_pass": _check(policy.get("status") == "pass" and stage.get("graph_write_enabled") is False),
        "regression_snapshot_pass": _check(regression.get("status") == "pass"),
        "runtime_execution_disabled": _check(stage.get("runtime_execution_enabled") is False and stage.get("generation_runtime_enabled") is False),
        "provider_execution_disabled": _check(stage.get("provider_execution_enabled") is False),
        "memory_store_graph_write_blocked": _check(stage.get("memory_write_enabled") is False and stage.get("execution_write_enabled") is False and stage.get("store_write_enabled") is False and stage.get("graph_write_enabled") is False),
        "canon_mutation_blocked": _check(stage.get("canon_mutation_enabled") is False and stage.get("canon_auto_resolution_count") == 0),
        "auto_repair_blocked": _check(stage.get("auto_repair_apply_enabled") is False and stage.get("auto_repair_mutation_count") == 0),
        "vector_db_runtime_dependency_blocked": _check(stage.get("vector_db_runtime_dependency") is False),
        "live_provider_rag_blocked": _check(stage.get("live_provider_rag_enabled") is False),
        "runtime_training_blocked": _check(stage.get("runtime_training_enabled") is False),
        "model_weight_update_zero": _check(stage.get("model_weight_update_count") == 0),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0 and stage.get("boundary_violation_count") == 0),
        "raw_manuscript_leakage_zero": _check(stage.get("raw_manuscript_provider_leakage") == 0 and stage.get("raw_manuscript_cross_project_leakage") == 0),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "157",
        "baseline_stage": "156",
        "title": "Deterministic Plan Graph Builder",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage157": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "runtime_execution_enabled": False,
        "graph_write_enabled": False,
        "store_write_enabled": False,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage157_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage157":
        report = _load_report(root, "stage156_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage156_release_gate(root)


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_report(root: Path, name: str) -> dict[str, Any] | None:
    path = root / "release/current" / name
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = ("status", "stage", "baseline_stage", "title", "issues", "mode", "node_count", "edge_count", "critical_path_length", "graph_checksum", "topological_order_count", "page03_execution_packet_store_inherited", "stage158_dependency_conflict_preflight_ready", "runtime_execution_enabled", "generation_runtime_enabled", "provider_execution_enabled", "memory_write_enabled", "execution_write_enabled", "store_write_enabled", "graph_write_enabled", "canon_mutation_enabled", "auto_repair_apply_enabled", "runtime_training_enabled", "model_weight_update_count", "canon_auto_resolution_count", "auto_repair_mutation_count", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "boundary_violation_count", "raw_manuscript_provider_leakage", "raw_manuscript_cross_project_leakage", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage157.md",
        "docs/proposals/stage157_deterministic_plan_graph_builder_proposal.md",
        "docs/architecture/stage157_deterministic_plan_graph_builder_blueprint.md",
        "docs/development/stage157_developer_handoff.md",
        "manifests/stage157_manifest.json",
        "manifests/stage157_deterministic_plan_graph_builder_manifest.json",
        "manifests/stage157_branchpoint_trace_manifest.json",
        "manifests/live_core_stage157_overlay.json",
        "release/current/stage157_release_asset_manifest.json",
        "release/current/stage157_deterministic_plan_graph_builder_report.json",
        "release/current/stage157_deterministic_plan_graph_builder_pack/plan_graph_nodes.json",
        "release/current/stage157_deterministic_plan_graph_builder_pack/plan_graph_edges.json",
        "release/current/stage157_deterministic_plan_graph_builder_pack/topological_order.json",
        "release/current/stage157_deterministic_plan_graph_builder_pack/dependency_integrity.json",
        "release/current/stage157_deterministic_plan_graph_builder_pack/deterministic_graph_checksum.json",
        "release/current/stage157_deterministic_plan_graph_builder_pack/node2_plan_projection_matrix.json",
        "release/current/stage157_deterministic_plan_graph_builder_pack/plan_graph_policy.json",
        "release/current/stage157_deterministic_plan_graph_builder_pack/regression_snapshot.json",
    ])


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage157", "run_stage157_deterministic_plan_graph_builder.py", "run_stage157_release_gate.py"])
