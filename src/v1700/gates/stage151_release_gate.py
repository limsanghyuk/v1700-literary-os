from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage150_release_gate import run_stage150_release_gate
from v1700.stage151 import run_stage151

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage151_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    if _active_version(root) != "stage151":
        existing = _load_report(root, "stage151_release_gate_report.json")
        if existing is not None and existing.get("status") == "pass":
            _CACHE[key] = existing
            return existing

    baseline = _baseline_gate(root)
    stage = run_stage151(root)
    parts = stage.get("parts", {})
    validation = parts.get("record_validation_report", {})
    store_spec = parts.get("store_spec", {})
    checksum_index = parts.get("checksum_index", {})
    access_policy = parts.get("read_only_access_policy", {})
    projection = parts.get("node2_projection_index", {})

    checks = {
        "stage150_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "stage151_report_pass": _check(stage.get("status") == "pass"),
        "local_store_mode_pass": _check(stage.get("mode") == "LOCAL_READ_ONLY_MEMORY_STORE" and stage.get("read_only_store_enabled") is True),
        "store_spec_pass": _check(store_spec.get("status") == "pass"),
        "record_validation_pass": _check(validation.get("status") == "pass" and validation.get("record_count", 0) >= 5),
        "checksum_index_pass": _check(checksum_index.get("status") == "pass" and checksum_index.get("entry_count") == validation.get("record_count")),
        "read_only_access_policy_pass": _check(access_policy.get("status") == "pass" and stage.get("store_write_enabled") is False),
        "node2_projection_index_pass": _check(projection.get("status") == "pass" and stage.get("node2_raw_reveal_access") == 0),
        "memory_write_blocked": _check(stage.get("memory_write_enabled") is False),
        "query_runtime_deferred": _check(stage.get("query_runtime_enabled") is False and stage.get("ranking_runtime_enabled") is False),
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
        "stage": "151",
        "baseline_stage": "150",
        "title": "Local Read-Only Memory Store",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage151": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "memory_write_enabled": False,
        "store_write_enabled": False,
        "runtime_training_enabled": False,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage151_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _baseline_gate(root: Path) -> dict[str, Any]:
    if _active_version(root) != "stage151":
        report = _load_report(root, "stage150_release_gate_report.json")
        if report is not None and report.get("status") == "pass":
            return report
    return run_stage150_release_gate(root)


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
        "read_only_store_enabled", "store_write_enabled", "record_count",
        "checksum_index_count", "node2_blocked_projection_count",
        "stage152_deterministic_query_ready", "query_runtime_enabled",
        "ranking_runtime_enabled", "vector_db_runtime_dependency", "live_provider_rag_enabled",
        "memory_write_enabled", "runtime_training_enabled", "provider_default_calls",
        "live_provider_call_count_in_release_gate", "node2_raw_reveal_access",
        "hidden_reveal_projection_count", "private_note_projection_count",
        "write_handle_projection_count", "raw_manuscript_provider_leakage",
        "raw_manuscript_cross_project_leakage", "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all(
        (root / rel).exists()
        for rel in [
            "docs/stages/stage151.md",
            "docs/proposals/stage151_local_read_only_memory_store_proposal.md",
            "docs/architecture/stage151_local_read_only_memory_store_blueprint.md",
            "docs/development/stage151_developer_handoff.md",
            "manifests/stage151_manifest.json",
            "manifests/stage151_local_read_only_memory_store_manifest.json",
            "release/current/stage151_local_read_only_memory_store_report.json",
            "release/current/stage151_release_gate_report.json",
            "release/current/stage151_local_read_only_memory_store_pack/store_spec.json",
            "release/current/stage151_local_read_only_memory_store_pack/record_validation_report.json",
            "release/current/stage151_local_read_only_memory_store_pack/checksum_index.json",
            "release/current/stage151_local_read_only_memory_store_pack/read_only_access_policy.json",
            "release/current/stage151_local_read_only_memory_store_pack/node2_projection_index.json",
            "samples/stage151_memory_store/project_memory_records.jsonl",
        ]
    )


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [root / "README.md", root / "RELEASE_NOTES.md", root / "package_manifest.json"]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in ["stage151", "run_stage151_local_read_only_memory_store.py", "run_stage151_release_gate.py"])
