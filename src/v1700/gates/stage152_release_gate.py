
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage151_release_gate import run_stage151_release_gate
from v1700.stage152 import run_stage152

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage152_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage152":
        existing = _load_report(root, "stage152_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage152(root)
    parts = stage.get("parts", {})
    checks = {
        "stage151_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage152_report_pass": _check(stage.get("status") == "pass"),
        "query_api_catalog_pass": _check(parts.get("query_api_catalog", {}).get("status") == "pass" and stage.get("api_count", 0) >= 10),
        "query_policy_pass": _check(parts.get("query_policy", {}).get("status") == "pass"),
        "intent_query_pass": _check(parts.get("intent_query_result", {}).get("status") == "pass" and stage.get("candidate_count", 0) > 0),
        "type_query_pass": _check(parts.get("type_query_results", {}).get("status") == "pass"),
        "ranking_pass": _check(parts.get("ranking_report", {}).get("status") == "pass" and stage.get("ranked_candidate_count", 0) > 0),
        "node2_projection_pass": _check(parts.get("node2_projection_report", {}).get("status") == "pass" and stage.get("node2_raw_reveal_access") == 0),
        "local_deterministic_query_enabled": _check(stage.get("query_runtime_enabled") is True and stage.get("ranking_runtime_enabled") is True),
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
        "stage": "152",
        "baseline_stage": "151",
        "title": "Deterministic Local Query / Ranking",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage152": _compact(stage),
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
    out = root / "release/current/stage152_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage152":
        report = _load_report(root, "stage151_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage151_release_gate(root)


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
        "query_runtime_enabled", "ranking_runtime_enabled", "query_write_enabled",
        "memory_write_enabled", "store_write_enabled", "candidate_count",
        "ranked_candidate_count", "node2_projected_count", "node2_blocked_projection_count",
        "stage153_memory_health_monitor_ready", "vector_db_runtime_dependency", "live_provider_rag_enabled",
        "runtime_training_enabled", "provider_default_calls", "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access", "hidden_reveal_projection_count", "raw_manuscript_provider_leakage",
        "raw_manuscript_cross_project_leakage", "credential_leakage", "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    required = [
        "docs/stages/stage152.md",
        "docs/proposals/stage152_memory_query_interface_proposal.md",
        "docs/architecture/stage152_memory_query_interface_blueprint.md",
        "docs/development/stage152_developer_handoff.md",
        "manifests/stage152_manifest.json",
        "manifests/stage152_memory_query_interface_manifest.json",
        "manifests/stage152_branchpoint_trace_manifest.json",
        "manifests/live_core_stage152_overlay.json",
        "release/current/stage152_memory_query_interface_report.json",
        "release/current/stage152_release_gate_report.json",
        "release/current/stage152_release_asset_manifest.json",
        "release/current/stage152_memory_query_interface_pack/query_api_catalog.json",
        "release/current/stage152_memory_query_interface_pack/query_policy.json",
        "release/current/stage152_memory_query_interface_pack/intent_query_result.json",
        "release/current/stage152_memory_query_interface_pack/type_query_results.json",
        "release/current/stage152_memory_query_interface_pack/ranking_report.json",
        "release/current/stage152_memory_query_interface_pack/node2_projection_report.json",
    ]
    return all((root / rel).exists() for rel in required)


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage152", "run_stage152_memory_query_interface.py", "run_stage152_release_gate.py"])
