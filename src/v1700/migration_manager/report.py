from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.stage136 import run_stage136

from .gate import MIGRATION_MANAGER_MODE, build_migration_plan
from .preflight import run_stage137_preflight


def run_stage137_migration_manager(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    pack = root / "release/current/stage137_migration_manager_pack"
    pack.mkdir(parents=True, exist_ok=True)
    stage136_report = run_stage136(root)
    plan = build_migration_plan(stage136_report)
    preflight = run_stage137_preflight(root)
    issues = list(plan.issues)
    if preflight.get("status") != "pass":
        issues.append("stage137_preflight_blocked")
    result = {
        "stage": "137",
        "baseline_stage": "136",
        "title": "MigrationManager & Dry-Run Migration Plan",
        "status": "pass" if not issues and plan.status == "pass" else "blocked",
        "issues": issues,
        "mode": MIGRATION_MANAGER_MODE,
        "migration_plan_only": True,
        "migration_step_count": plan.counters.get("migration_step_count", 0),
        "schema_step_count": plan.counters.get("schema_step_count", 0),
        "binding_step_count": plan.counters.get("binding_step_count", 0),
        "approval_checkpoint_count": plan.counters.get("approval_checkpoint_count", 0),
        "review_only_checkpoint_count": plan.counters.get("review_only_checkpoint_count", 0),
        "covered_binding_count": plan.counters.get("covered_binding_count", 0),
        "rollback_ready_count": plan.counters.get("rollback_ready_count", 0),
        "execution_blocked_count": plan.counters.get("execution_blocked_count", 0),
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "losdb_write_enabled": False,
        "migration_execution_enabled": False,
        "storage_contract_write_enabled": False,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "cross_project_write_allowed": False,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "branchpoint_lineage_preserved": not issues,
        "parts": {
            "stage136_report": _compact_stage136(stage136_report),
            "migration_plan": plan.to_dict(),
            "preflight": preflight,
        },
    }
    _write_json(pack / "migration_plan.json", plan.to_dict())
    _write_json(pack / "migration_steps.json", {"steps": [step.to_dict() for step in plan.steps]})
    _write_json(pack / "approval_checkpoint_index.json", {"steps": [step.to_dict() for step in plan.steps if step.scope == "checkpoint"]})
    _write_json(pack / "stage136_input_summary.json", _compact_stage136(stage136_report))
    _write_json(pack / "stage137_preflight_report.json", preflight)
    _write_json(root / "release/current/stage137_migration_manager_report.json", result)
    return result


def _compact_stage136(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": report.get("stage"),
        "status": report.get("status"),
        "mode": report.get("mode"),
        "schema_registry_only": report.get("schema_registry_only"),
        "schema_count": report.get("schema_count"),
        "binding_count": report.get("binding_count"),
        "migration_ready_count": report.get("migration_ready_count"),
        "storage_contract_ready_count": report.get("storage_contract_ready_count"),
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved"),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
