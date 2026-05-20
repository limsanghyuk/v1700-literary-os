from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.stage136 import run_stage136
from v1700.stage137 import run_stage137

from .gate import LOSDB_STORAGE_CONTRACT_MODE, build_storage_contract_catalog
from .preflight import run_stage138_preflight


def run_stage138_losdb_storage_contracts(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    pack = root / "release/current/stage138_losdb_storage_contracts_pack"
    pack.mkdir(parents=True, exist_ok=True)
    stage136_report = run_stage136(root)
    stage137_report = run_stage137(root)
    catalog = build_storage_contract_catalog(stage136_report, stage137_report)
    preflight = run_stage138_preflight(root)
    issues = list(catalog.issues)
    if preflight.get("status") != "pass":
        issues.append("stage138_preflight_blocked")
    total_items = (
        catalog.counters.get("schema_contract_count", 0)
        + catalog.counters.get("binding_route_count", 0)
        + catalog.counters.get("approval_lane_count", 0)
    )
    result = {
        "stage": "138",
        "baseline_stage": "137",
        "title": "LOSDB Storage Contracts & Governance-Ready Catalog",
        "status": "pass" if not issues and catalog.status == "pass" else "blocked",
        "issues": issues,
        "mode": LOSDB_STORAGE_CONTRACT_MODE,
        "storage_contract_catalog_only": True,
        "schema_contract_count": catalog.counters.get("schema_contract_count", 0),
        "binding_route_count": catalog.counters.get("binding_route_count", 0),
        "approval_lane_count": catalog.counters.get("approval_lane_count", 0),
        "covered_binding_count": catalog.counters.get("covered_binding_count", 0),
        "review_lane_route_count": catalog.counters.get("review_lane_route_count", 0),
        "rollback_ready_count": catalog.counters.get("rollback_ready_count", 0),
        "write_blocked_count": catalog.counters.get("write_blocked_count", 0),
        "governance_ready_count": catalog.counters.get("governance_ready_count", 0),
        "dependency_preserved_count": catalog.counters.get("dependency_preserved_count", 0),
        "unique_namespace_count": catalog.counters.get("unique_namespace_count", 0),
        "unique_contract_count": catalog.counters.get("unique_contract_count", 0),
        "total_contract_items": total_items,
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
            "stage137_report": _compact_stage137(stage137_report),
            "storage_contract_catalog": catalog.to_dict(),
            "preflight": preflight,
        },
    }
    _write_json(pack / "storage_contract_catalog.json", catalog.to_dict())
    _write_json(pack / "namespace_contracts.json", {"contracts": [contract.to_dict() for contract in catalog.contracts]})
    _write_json(pack / "binding_routes.json", {"routes": [route.to_dict() for route in catalog.routes]})
    _write_json(pack / "approval_lane_contracts.json", {"approval_lanes": [lane.to_dict() for lane in catalog.approval_lanes]})
    _write_json(pack / "stage137_input_summary.json", _compact_stage137(stage137_report))
    _write_json(pack / "stage138_preflight_report.json", preflight)
    _write_json(root / "release/current/stage138_losdb_storage_contracts_report.json", result)
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


def _compact_stage137(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": report.get("stage"),
        "status": report.get("status"),
        "mode": report.get("mode"),
        "migration_plan_only": report.get("migration_plan_only"),
        "migration_step_count": report.get("migration_step_count"),
        "covered_binding_count": report.get("covered_binding_count"),
        "approval_checkpoint_count": report.get("approval_checkpoint_count"),
        "rollback_ready_count": report.get("rollback_ready_count"),
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved"),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
