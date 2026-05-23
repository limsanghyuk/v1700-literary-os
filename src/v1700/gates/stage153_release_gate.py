from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage152_release_gate import run_stage152_release_gate
from v1700.stage153 import run_stage153

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage153_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage153":
        existing = _load_report(root, "stage153_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage153(root)
    parts = stage.get("parts", {})
    checks = {
        "stage152_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage153_report_pass": _check(stage.get("status") == "pass"),
        "record_health_pass": _check(parts.get("record_health_report", {}).get("status") == "pass" and stage.get("health_check_count", 0) >= 6),
        "leakage_scan_pass": _check(parts.get("leakage_boundary_scan", {}).get("status") == "pass" and stage.get("credential_leakage") == 0),
        "node2_leakage_matrix_pass": _check(parts.get("node2_leakage_matrix", {}).get("status") == "pass" and stage.get("node2_raw_reveal_access") == 0),
        "query_boundary_probe_pass": _check(parts.get("query_boundary_probe", {}).get("status") == "pass" and parts.get("query_boundary_probe", {}).get("probe_count", 0) >= 3),
        "health_policy_pass": _check(parts.get("health_policy", {}).get("status") == "pass"),
        "regression_snapshot_pass": _check(parts.get("regression_snapshot", {}).get("status") == "pass"),
        "health_monitor_enabled": _check(stage.get("health_monitor_enabled") is True and stage.get("leakage_boundary_enabled") is True),
        "boundary_violation_zero": _check(stage.get("boundary_violation_count") == 0),
        "query_write_blocked": _check(stage.get("query_write_enabled") is False and stage.get("memory_write_enabled") is False),
        "store_write_blocked": _check(stage.get("store_write_enabled") is False),
        "vector_db_runtime_dependency_blocked": _check(stage.get("vector_db_runtime_dependency") is False),
        "live_provider_rag_blocked": _check(stage.get("live_provider_rag_enabled") is False),
        "runtime_training_blocked": _check(stage.get("runtime_training_enabled") is False),
        "model_weight_update_zero": _check(stage.get("model_weight_update_count") == 0),
        "canon_auto_resolution_zero": _check(stage.get("canon_auto_resolution_count") == 0),
        "auto_repair_mutation_zero": _check(stage.get("auto_repair_mutation_count") == 0),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0 and stage.get("hidden_reveal_projection_count") == 0),
        "raw_manuscript_leakage_zero": _check(stage.get("raw_manuscript_provider_leakage") == 0 and stage.get("raw_manuscript_cross_project_leakage") == 0),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "153",
        "baseline_stage": "152",
        "title": "Memory Health & Leakage Boundary",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage153": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "memory_write_enabled": False,
        "query_write_enabled": False,
        "store_write_enabled": False,
        "runtime_training_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage153_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage153":
        report = _load_report(root, "stage152_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage152_release_gate(root)


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
    keep = (
        "status", "stage", "baseline_stage", "title", "issues", "mode",
        "health_monitor_enabled", "leakage_boundary_enabled", "boundary_violation_count",
        "health_check_count", "health_pass_count", "leakage_rule_count",
        "node2_matrix_entry_count", "query_probe_count", "stage154_page02_release_seal_ready",
        "query_runtime_enabled", "ranking_runtime_enabled", "query_write_enabled",
        "memory_write_enabled", "store_write_enabled", "vector_db_runtime_dependency",
        "live_provider_rag_enabled", "runtime_training_enabled", "provider_default_calls",
        "live_provider_call_count_in_release_gate", "node2_raw_reveal_access",
        "raw_manuscript_provider_leakage", "credential_leakage", "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all(
        (root / rel).exists()
        for rel in [
            "docs/stages/stage153.md",
            "docs/proposals/stage153_memory_health_leakage_boundary_proposal.md",
            "docs/architecture/stage153_memory_health_leakage_boundary_blueprint.md",
            "docs/development/stage153_developer_handoff.md",
            "manifests/stage153_manifest.json",
            "manifests/stage153_memory_health_leakage_boundary_manifest.json",
            "manifests/stage153_branchpoint_trace_manifest.json",
            "release/current/stage153_memory_health_leakage_boundary_report.json",
            "release/current/stage153_release_gate_report.json",
            "release/current/stage153_memory_health_leakage_boundary_pack/record_health_report.json",
            "release/current/stage153_memory_health_leakage_boundary_pack/leakage_boundary_scan.json",
            "release/current/stage153_memory_health_leakage_boundary_pack/node2_leakage_matrix.json",
            "release/current/stage153_memory_health_leakage_boundary_pack/query_boundary_probe.json",
            "release/current/stage153_memory_health_leakage_boundary_pack/health_policy.json",
            "release/current/stage153_memory_health_leakage_boundary_pack/regression_snapshot.json",
        ]
    )


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage153", "run_stage153_memory_health_leakage_boundary.py", "run_stage153_release_gate.py"])
