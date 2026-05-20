from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage137_release_gate import run_stage137_release_gate
from v1700.stage138 import run_stage138

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage138_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    baseline = run_stage137_release_gate(root)
    stage = run_stage138(root)
    catalog = stage.get("parts", {}).get("storage_contract_catalog", {})
    total_items = int(stage.get("total_contract_items", 0))
    checks = {
        "stage137_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "storage_contract_report_pass": _check(stage.get("status") == "pass"),
        "storage_contract_catalog_pass": _check(catalog.get("status") == "pass"),
        "contract_mode_pass": _check(
            stage.get("storage_contract_catalog_only") is True
            and stage.get("mode") == "LOSDB_STORAGE_CONTRACTS_READINESS_ONLY"
        ),
        "schema_contracts_present": _check(stage.get("schema_contract_count", 0) >= 3),
        "all_bindings_covered_pass": _check(
            stage.get("covered_binding_count") == stage.get("binding_route_count")
            and stage.get("covered_binding_count", 0) >= 1
        ),
        "approval_lane_preserved_pass": _check(
            stage.get("approval_lane_count", 0) >= 1 and stage.get("review_lane_route_count", 0) >= 1
        ),
        "dependency_preserved_pass": _check(stage.get("dependency_preserved_count") == total_items),
        "unique_namespace_pass": _check(stage.get("unique_namespace_count") == stage.get("schema_contract_count")),
        "unique_contract_id_pass": _check(stage.get("unique_contract_count") == stage.get("schema_contract_count")),
        "rollback_ready_metadata_pass": _check(stage.get("rollback_ready_count") == total_items),
        "governance_ready_pass": _check(stage.get("governance_ready_count") == stage.get("binding_route_count")),
        "storage_write_blocked": _check(
            stage.get("losdb_write_enabled") is False
            and stage.get("storage_contract_write_enabled") is False
            and stage.get("write_blocked_count") == total_items
        ),
        "migration_execution_blocked": _check(stage.get("migration_execution_enabled") is False),
        "provider_zero_pass": _check(
            stage.get("provider_default_calls") == 0 and stage.get("live_provider_call_count_in_release_gate") == 0
        ),
        "node2_boundary_pass": _check(stage.get("node2_raw_reveal_access") == 0),
        "raw_manuscript_leakage_zero": _check(
            stage.get("raw_manuscript_provider_leakage") == 0
            and stage.get("raw_manuscript_cross_project_leakage") == 0
        ),
        "credential_leakage_zero_pass": _check(stage.get("credential_leakage") == 0),
        "branchpoint_survival_pass": _check(stage.get("branchpoint_lineage_preserved") is True),
        "docs_manifest_pass": _check(_docs_manifest_ok(root)),
        "procedure_alignment_pass": _check(_procedure_alignment_ok(root)),
    }
    issues = [name for name, value in checks.items() if value["status"] != "pass"]
    result = {
        "stage": "138",
        "baseline_stage": "137",
        "title": "LOSDB Storage Contracts Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage138": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage138_release_gate_report.json"
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
        "storage_contract_catalog_only",
        "schema_contract_count",
        "binding_route_count",
        "approval_lane_count",
        "covered_binding_count",
        "review_lane_route_count",
        "rollback_ready_count",
        "write_blocked_count",
        "governance_ready_count",
        "dependency_preserved_count",
        "unique_namespace_count",
        "unique_contract_count",
        "total_contract_items",
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
    return all(
        (root / rel).exists()
        for rel in [
            "docs/stages/stage138.md",
            "docs/proposals/stage138_proposal.md",
            "docs/architecture/stage138_blueprint.md",
            "docs/development/stage138_developer_handoff.md",
            "manifests/stage138_manifest.json",
            "manifests/stage138_losdb_storage_contracts_manifest.json",
            "manifests/stage138_branchpoint_trace_manifest.json",
            "manifests/live_core_stage138_overlay.json",
            "release/current/stage138_losdb_storage_contracts_report.json",
            "release/current/stage138_release_gate_report.json",
            "release/current/stage138_losdb_storage_contracts_pack/storage_contract_catalog.json",
            "release/current/stage138_losdb_storage_contracts_pack/stage138_preflight_report.json",
        ]
    )


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
    return all(
        token in contents
        for token in [
            "stage138",
            "run_stage138_losdb_storage_contracts.py",
            "run_stage138_release_gate.py",
        ]
    )
