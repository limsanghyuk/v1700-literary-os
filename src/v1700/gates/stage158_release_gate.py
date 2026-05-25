from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage157_release_gate import run_stage157_release_gate
from v1700.stage158 import run_stage158

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage158_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage158":
        existing = _load_report(root, "stage158_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage158(root)
    parts = stage.get("parts", {})
    order = parts.get("dependency_order_preflight", {})
    conflict = parts.get("conflict_matrix", {})
    boundary = parts.get("packet_boundary_preflight", {})
    blocked = parts.get("blocked_operation_registry", {})
    node2 = parts.get("node2_conflict_projection_matrix", {})
    integrity = parts.get("graph_integrity_snapshot", {})
    connectivity = parts.get("preflight_step15_connectivity_matrix", {})
    regression = parts.get("regression_snapshot", {})

    checks = {
        "stage157_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage158_report_pass": _check(stage.get("status") == "pass"),
        "dependency_conflict_preflight_mode_pass": _check(stage.get("mode") == "DEPENDENCY_CONFLICT_PREFLIGHT_LOCAL_ONLY"),
        "dependency_order_preflight_pass": _check(order.get("status") == "pass" and order.get("finding_count", 0) >= 5),
        "conflict_matrix_pass": _check(conflict.get("status") == "pass" and stage.get("conflict_count") == 0),
        "packet_boundary_preflight_pass": _check(boundary.get("status") == "pass" and stage.get("boundary_violation_count") == 0),
        "blocked_operation_registry_pass": _check(blocked.get("status") == "pass"),
        "node2_conflict_projection_pass": _check(node2.get("status") == "pass" and stage.get("node2_raw_reveal_access") == 0),
        "graph_integrity_snapshot_pass": _check(integrity.get("status") == "pass" and len(str(stage.get("preflight_checksum", ""))) == 64),
        "preflight_step15_connectivity_pass": _check(connectivity.get("status") == "pass"),
        "regression_snapshot_pass": _check(regression.get("status") == "pass"),
        "runtime_execution_disabled": _check(stage.get("runtime_execution_enabled") is False and stage.get("generation_runtime_enabled") is False),
        "provider_execution_disabled": _check(stage.get("provider_execution_enabled") is False),
        "preflight_write_blocked": _check(stage.get("preflight_write_enabled") is False and stage.get("execution_write_enabled") is False and stage.get("graph_write_enabled") is False),
        "memory_store_write_blocked": _check(stage.get("memory_write_enabled") is False and stage.get("store_write_enabled") is False),
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
        "stage": "158",
        "baseline_stage": "157",
        "title": "Dependency and Conflict Preflight",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage158": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "runtime_execution_enabled": False,
        "preflight_write_enabled": False,
        "graph_write_enabled": False,
        "store_write_enabled": False,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage158_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage158":
        report = _load_report(root, "stage157_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage157_release_gate(root)


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
    keep = ("status", "stage", "baseline_stage", "title", "issues", "mode", "packet_count", "dependency_count", "conflict_count", "boundary_violation_count", "preflight_checksum", "stage159_execution_dry_run_trace_ready", "runtime_execution_enabled", "generation_runtime_enabled", "provider_execution_enabled", "memory_write_enabled", "execution_write_enabled", "store_write_enabled", "graph_write_enabled", "preflight_write_enabled", "canon_mutation_enabled", "auto_repair_apply_enabled", "runtime_training_enabled", "model_weight_update_count", "canon_auto_resolution_count", "auto_repair_mutation_count", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "raw_manuscript_provider_leakage", "raw_manuscript_cross_project_leakage", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage158.md",
        "docs/proposals/stage158_dependency_conflict_preflight_proposal.md",
        "docs/architecture/stage158_dependency_conflict_preflight_blueprint.md",
        "docs/development/stage158_developer_handoff.md",
        "manifests/stage158_manifest.json",
        "manifests/stage158_dependency_conflict_preflight_manifest.json",
        "manifests/stage158_branchpoint_trace_manifest.json",
        "manifests/live_core_stage158_overlay.json",
        "release/current/stage158_release_asset_manifest.json",
        "release/current/stage158_dependency_conflict_preflight_report.json",
        "release/current/stage158_release_gate_report.json",
        "release/current/stage158_dependency_conflict_preflight_pack/dependency_order_preflight.json",
        "release/current/stage158_dependency_conflict_preflight_pack/conflict_matrix.json",
        "release/current/stage158_dependency_conflict_preflight_pack/packet_boundary_preflight.json",
        "release/current/stage158_dependency_conflict_preflight_pack/blocked_operation_registry.json",
        "release/current/stage158_dependency_conflict_preflight_pack/node2_conflict_projection_matrix.json",
        "release/current/stage158_dependency_conflict_preflight_pack/graph_integrity_snapshot.json",
        "release/current/stage158_dependency_conflict_preflight_pack/preflight_step15_connectivity_matrix.json",
        "release/current/stage158_dependency_conflict_preflight_pack/regression_snapshot.json",
    ])


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage158", "run_stage158_dependency_conflict_preflight.py", "run_stage158_release_gate.py"])
