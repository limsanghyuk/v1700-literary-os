from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage135_release_gate import run_stage135_release_gate
from v1700.stage136 import run_stage136

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage136_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    baseline = run_stage135_release_gate(root)
    stage = run_stage136(root)
    registry = stage.get("parts", {}).get("schema_registry", {})
    bindings = registry.get("bindings", [])
    preflight = stage.get("parts", {}).get("preflight", {})
    checks = {
        "stage135_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "schema_registry_report_pass": _check(stage.get("status") == "pass"),
        "schema_registry_pass": _check(registry.get("status") == "pass"),
        "schema_catalog_present": _check(len(registry.get("schemas", [])) >= 3),
        "all_candidates_bound_pass": _check(stage.get("binding_count") == stage.get("validated_candidate_count") and stage.get("binding_count", 0) >= 1),
        "review_only_binding_pass": _check(any(binding.get("decision") == "REVIEW_ONLY" for binding in bindings)),
        "migration_ready_metadata_pass": _check(stage.get("migration_ready_count") == stage.get("binding_count")),
        "storage_contract_ready_metadata_pass": _check(stage.get("storage_contract_ready_count") == stage.get("binding_count")),
        "preflight_pass": _check(preflight.get("status") == "pass" and preflight.get("python_fallback", {}).get("status") == "PASS"),
        "losdb_write_blocked": _check(stage.get("losdb_write_enabled") is False and stage.get("storage_contract_write_enabled") is False),
        "migration_execution_blocked": _check(stage.get("migration_execution_enabled") is False),
        "provider_zero_pass": _check(stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_zero": _check(stage.get("raw_manuscript_provider_leakage") == 0 and stage.get("raw_manuscript_cross_project_leakage") == 0),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "136",
        "baseline_stage": "135",
        "title": "SchemaRegistry Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage136": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage136_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status",
        "stage",
        "baseline_stage",
        "title",
        "issues",
        "mode",
        "schema_registry_only",
        "schema_count",
        "binding_count",
        "validated_candidate_count",
        "accepted_binding_count",
        "rejected_binding_count",
        "review_only_binding_count",
        "migration_ready_count",
        "storage_contract_ready_count",
        "losdb_write_enabled",
        "migration_execution_enabled",
        "storage_contract_write_enabled",
        "provider_default_calls",
        "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access",
        "raw_manuscript_provider_leakage",
        "raw_manuscript_cross_project_leakage",
        "credential_leakage",
        "cross_project_write_allowed",
        "canon_auto_resolution_count",
        "auto_repair_mutation_count",
        "branchpoint_lineage_preserved",
    )
    return {key: stage.get(key) for key in keep if key in stage}


def _docs_manifest_ok(root: Path) -> bool:
    return all((root / rel).exists() for rel in [
        "docs/stages/stage136.md",
        "docs/proposals/stage136_proposal.md",
        "docs/architecture/stage136_blueprint.md",
        "docs/development/stage136_developer_handoff.md",
        "manifests/stage136_manifest.json",
        "manifests/stage136_schema_registry_manifest.json",
        "manifests/stage136_branchpoint_trace_manifest.json",
        "manifests/live_core_stage136_overlay.json",
        "release/current/stage136_schema_registry_report.json",
        "release/current/stage136_release_gate_report.json",
        "release/current/stage136_schema_registry_pack/schema_registry.json",
        "release/current/stage136_schema_registry_pack/stage136_preflight_report.json",
    ])


def _procedure_alignment_ok(root: Path) -> bool:
    targets = [
        root / ".github/workflows/ci-core.yml",
        root / ".github/workflows/cd-dry-run.yml",
        root / ".github/workflows/release.yml",
        root / "RELEASE_NOTES.md",
        root / "package_manifest.json",
    ]
    if not all(path.exists() for path in targets):
        return False
    contents = "\n".join(path.read_text(encoding="utf-8") for path in targets)
    return all(token in contents for token in [
        "stage136",
        "run_stage136_schema_registry.py",
        "run_stage136_release_gate.py",
    ])
