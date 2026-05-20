from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage136_release_gate import run_stage136_release_gate
from v1700.stage137 import run_stage137

_CACHE: dict[str, dict[str, Any]] = {}


def run_stage137_release_gate(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    key = str(root.resolve())
    if key in _CACHE:
        return _CACHE[key]
    baseline = run_stage136_release_gate(root)
    stage = run_stage137(root)
    plan = stage.get("parts", {}).get("migration_plan", {})
    steps = plan.get("steps", [])
    preflight = stage.get("parts", {}).get("preflight", {})
    checks = {
        "stage136_baseline_gate_pass": _check(baseline.get("status") == "pass"),
        "migration_manager_report_pass": _check(stage.get("status") == "pass"),
        "migration_plan_pass": _check(plan.get("status") == "pass"),
        "plan_only_mode_pass": _check(stage.get("migration_plan_only") is True and stage.get("mode") == "MIGRATION_MANAGER_PLAN_ONLY"),
        "ordered_steps_pass": _check(_ordered_steps(steps)),
        "all_bindings_covered_pass": _check(stage.get("covered_binding_count") == stage.get("binding_step_count") and stage.get("covered_binding_count", 0) >= 1),
        "schema_steps_present": _check(stage.get("schema_step_count", 0) >= 3),
        "review_only_checkpoint_pass": _check(stage.get("review_only_checkpoint_count", 0) >= 1),
        "rollback_ready_metadata_pass": _check(stage.get("rollback_ready_count") == stage.get("migration_step_count")),
        "preflight_pass": _check(preflight.get("status") == "pass" and preflight.get("python_fallback", {}).get("status") == "PASS"),
        "migration_execution_blocked": _check(stage.get("migration_execution_enabled") is False and stage.get("execution_blocked_count") == stage.get("migration_step_count")),
        "losdb_write_blocked": _check(stage.get("losdb_write_enabled") is False and stage.get("storage_contract_write_enabled") is False),
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
        "stage": "137",
        "baseline_stage": "136",
        "title": "MigrationManager Gate",
        "status": "pass" if not issues and stage.get("status") == "pass" else "blocked",
        "issues": issues,
        "checks": checks,
        "stage137": _compact(stage),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    out = root / "release/current/stage137_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _CACHE[key] = result
    return result


def _check(condition: bool) -> dict[str, str]:
    return {"status": "pass" if condition else "blocked"}


def _ordered_steps(steps: list[dict[str, Any]]) -> bool:
    orders = [int(step.get("order", 0)) for step in steps]
    return bool(orders) and orders == sorted(orders) and len(set(orders)) == len(orders)


def _compact(stage: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status",
        "stage",
        "baseline_stage",
        "title",
        "issues",
        "mode",
        "migration_plan_only",
        "migration_step_count",
        "schema_step_count",
        "binding_step_count",
        "approval_checkpoint_count",
        "review_only_checkpoint_count",
        "covered_binding_count",
        "rollback_ready_count",
        "execution_blocked_count",
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
        "docs/stages/stage137.md",
        "docs/proposals/stage137_proposal.md",
        "docs/architecture/stage137_blueprint.md",
        "docs/development/stage137_developer_handoff.md",
        "manifests/stage137_manifest.json",
        "manifests/stage137_migration_manager_manifest.json",
        "manifests/stage137_branchpoint_trace_manifest.json",
        "manifests/live_core_stage137_overlay.json",
        "release/current/stage137_migration_manager_report.json",
        "release/current/stage137_release_gate_report.json",
        "release/current/stage137_migration_manager_pack/migration_plan.json",
        "release/current/stage137_migration_manager_pack/stage137_preflight_report.json",
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
        "stage137",
        "run_stage137_migration_manager.py",
        "run_stage137_release_gate.py",
    ])
