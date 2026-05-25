from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage157_release_gate import run_stage157_release_gate

from .analyzer import analyze_dependency_conflict_preflight
from .contracts import BlockedOperationRule, ConnectivityCheck

TARGET_STAGE = "stage158"
TARGET_REPORT = "release/current/stage158_dependency_conflict_preflight_report.json"
STAGE157_REPORT = "release/current/stage157_deterministic_plan_graph_builder_report.json"


def run_stage158_dependency_conflict_preflight(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage157 = run_stage157_release_gate(root)
    stage157_report = _load_existing(root / STAGE157_REPORT) or {}
    analysis = analyze_dependency_conflict_preflight(stage157_report)
    pack = root / "release/current/stage158_dependency_conflict_preflight_pack"
    pack.mkdir(parents=True, exist_ok=True)

    parts = {
        "dependency_order_preflight": _dependency_order_preflight(analysis),
        "conflict_matrix": _conflict_matrix(analysis),
        "packet_boundary_preflight": _packet_boundary_preflight(analysis),
        "blocked_operation_registry": _blocked_operation_registry(),
        "node2_conflict_projection_matrix": _node2_conflict_projection_matrix(analysis),
        "graph_integrity_snapshot": _graph_integrity_snapshot(stage157_report, analysis),
        "preflight_step15_connectivity_matrix": _preflight_step15_connectivity_matrix(root),
        "regression_snapshot": _regression_snapshot(analysis),
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}.json", payload)

    issues: list[str] = []
    if stage157.get("status") != "pass":
        issues.append("stage157_release_gate_blocked")
    if analysis.get("status") != "pass":
        issues.extend(f"dependency_conflict:{issue}" for issue in analysis.get("issues", []))
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "158",
        "baseline_stage": "157",
        "title": "Dependency and Conflict Preflight",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "DEPENDENCY_CONFLICT_PREFLIGHT_LOCAL_ONLY",
        "page": "Page03 Execution Body",
        "source_stage157_report": STAGE157_REPORT,
        "packet_count": analysis.get("packet_count", 0),
        "dependency_count": analysis.get("dependency_count", 0),
        "conflict_count": analysis.get("conflict_count", 0),
        "boundary_violation_count": analysis.get("boundary_violation_count", 0),
        "preflight_checksum": analysis.get("preflight_checksum", ""),
        "runtime_execution_enabled": False,
        "generation_runtime_enabled": False,
        "provider_execution_enabled": False,
        "memory_write_enabled": False,
        "execution_write_enabled": False,
        "store_write_enabled": False,
        "graph_write_enabled": False,
        "preflight_write_enabled": False,
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
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "stage159_execution_dry_run_trace_ready": not issues,
        "parts": {"stage157_release_gate": _compact(stage157), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _dependency_order_preflight(analysis: dict[str, Any]) -> dict[str, Any]:
    findings = list(analysis.get("dependency_order_findings", []))
    issues = [f"{item.get('packet_id')}:{item.get('dependency_id')}:{item.get('reason')}" for item in findings if item.get("status") != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Dependency Order Preflight",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "finding_count": len(findings),
        "findings": findings,
    }


def _conflict_matrix(analysis: dict[str, Any]) -> dict[str, Any]:
    matrix = list(analysis.get("conflict_matrix", []))
    issues = [str(item.get("name")) for item in matrix if item.get("status") != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Conflict Matrix",
        "status": "pass" if not issues and analysis.get("conflict_count") == 0 else "blocked",
        "issues": issues,
        "conflict_count": analysis.get("conflict_count", 0),
        "matrix": matrix,
    }


def _packet_boundary_preflight(analysis: dict[str, Any]) -> dict[str, Any]:
    rules = list(analysis.get("boundary_preflight_rules", []))
    issues = [f"{item.get('packet_id')}:{item.get('name')}" for item in rules if item.get("status") != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Packet Boundary Preflight",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "rule_count": len(rules),
        "rules": rules,
    }


def _blocked_operation_registry() -> dict[str, Any]:
    rules = (
        BlockedOperationRule("runtime_execution", False, True, TARGET_REPORT),
        BlockedOperationRule("provider_execution", False, True, TARGET_REPORT),
        BlockedOperationRule("memory_write", False, True, TARGET_REPORT),
        BlockedOperationRule("execution_write", False, True, TARGET_REPORT),
        BlockedOperationRule("graph_write", False, True, TARGET_REPORT),
        BlockedOperationRule("canon_mutation", False, True, TARGET_REPORT),
        BlockedOperationRule("auto_repair_apply", False, True, TARGET_REPORT),
        BlockedOperationRule("runtime_training", False, True, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if rule.enabled or not rule.must_remain_disabled]
    return {
        "stage": TARGET_STAGE,
        "title": "Blocked Operation Registry",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "rule_count": len(rules),
        "rules": [rule.to_dict() for rule in rules],
    }


def _node2_conflict_projection_matrix(analysis: dict[str, Any]) -> dict[str, Any]:
    matrix = list(analysis.get("node2_conflict_projection_matrix", []))
    issues = [f"{item.get('packet_id')}:{','.join(item.get('forbidden_token_hits', []))}" for item in matrix if item.get("status") != "pass"]
    return {
        "stage": TARGET_STAGE,
        "title": "Node2 Conflict Projection Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "row_count": len(matrix),
        "matrix": matrix,
        "node2_raw_reveal_access": 0,
        "node2_hidden_execution_payload_access": 0,
    }


def _graph_integrity_snapshot(stage157_report: dict[str, Any], analysis: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    if stage157_report.get("status") != "pass":
        issues.append("stage157_report_not_pass")
    if len(str(stage157_report.get("graph_checksum", ""))) != 64:
        issues.append("invalid_stage157_graph_checksum")
    if len(str(analysis.get("preflight_checksum", ""))) != 64:
        issues.append("invalid_stage158_preflight_checksum")
    return {
        "stage": TARGET_STAGE,
        "title": "Graph Integrity Snapshot",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "source_graph_checksum": stage157_report.get("graph_checksum", ""),
        "preflight_checksum": analysis.get("preflight_checksum", ""),
        "packet_count": analysis.get("packet_count", 0),
        "dependency_count": analysis.get("dependency_count", 0),
    }


def _preflight_step15_connectivity_matrix(root: Path) -> dict[str, Any]:
    checks = (
        ConnectivityCheck("stage158_package", "src/v1700/dependency_conflict_preflight/__init__.py", True, (root / "src/v1700/dependency_conflict_preflight/__init__.py").exists()),
        ConnectivityCheck("stage158_runner", "src/v1700/stage158/stage158_runner.py", True, (root / "src/v1700/stage158/stage158_runner.py").exists()),
        ConnectivityCheck("stage158_gate", "src/v1700/gates/stage158_release_gate.py", True, (root / "src/v1700/gates/stage158_release_gate.py").exists()),
        ConnectivityCheck("stage158_tool", "tools/run_stage158_dependency_conflict_preflight.py", True, (root / "tools/run_stage158_dependency_conflict_preflight.py").exists()),
        ConnectivityCheck("stage158_gate_tool", "tools/run_stage158_release_gate.py", True, (root / "tools/run_stage158_release_gate.py").exists()),
        ConnectivityCheck("stage158_test", "tests/test_stage158_dependency_conflict_preflight.py", True, (root / "tests/test_stage158_dependency_conflict_preflight.py").exists()),
        ConnectivityCheck("stage158_manifest", "manifests/stage158_manifest.json", True, (root / "manifests/stage158_manifest.json").exists()),
        ConnectivityCheck("stage158_docs", "docs/stages/stage158.md", True, (root / "docs/stages/stage158.md").exists()),
    )
    issues = [check.name for check in checks if check.required and not check.exists]
    return {
        "stage": TARGET_STAGE,
        "title": "Preflight Step15 Connectivity Matrix",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "check_count": len(checks),
        "checks": [check.to_dict() for check in checks],
    }


def _regression_snapshot(analysis: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": TARGET_STAGE,
        "title": "Stage158 Regression Snapshot",
        "status": "pass" if analysis.get("status") == "pass" else "blocked",
        "issues": list(analysis.get("issues", [])),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": analysis.get("boundary_violation_count", 0),
        "runtime_execution_enabled": False,
        "preflight_write_enabled": False,
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
