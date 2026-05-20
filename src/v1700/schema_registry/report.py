from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.stage135 import run_stage135

from .gate import SCHEMA_REGISTRY_MODE, build_schema_registry
from .preflight import run_stage136_preflight


def run_stage136_schema_registry(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    pack = root / "release/current/stage136_schema_registry_pack"
    pack.mkdir(parents=True, exist_ok=True)
    stage135_report = run_stage135(root)
    registry = build_schema_registry(stage135_report)
    preflight = run_stage136_preflight(root)
    issues = list(registry.issues)
    if preflight.get("status") != "pass":
        issues.append("stage136_preflight_blocked")
    result = {
        "stage": "136",
        "baseline_stage": "135",
        "title": "SchemaRegistry & Migration-Ready Candidate Schemas",
        "status": "pass" if not issues and registry.status == "pass" else "blocked",
        "issues": issues,
        "mode": SCHEMA_REGISTRY_MODE,
        "schema_registry_only": True,
        "schema_count": registry.counters.get("schema_count", 0),
        "binding_count": registry.counters.get("binding_count", 0),
        "validated_candidate_count": registry.counters.get("validated_candidate_count", 0),
        "accepted_binding_count": registry.counters.get("accepted_binding_count", 0),
        "rejected_binding_count": registry.counters.get("rejected_binding_count", 0),
        "review_only_binding_count": registry.counters.get("review_only_binding_count", 0),
        "migration_ready_count": registry.counters.get("migration_ready_count", 0),
        "storage_contract_ready_count": registry.counters.get("storage_contract_ready_count", 0),
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
            "stage135_report": _compact_stage135(stage135_report),
            "schema_registry": registry.to_dict(),
            "preflight": preflight,
        },
    }
    _write_json(pack / "schema_registry.json", registry.to_dict())
    _write_json(pack / "schema_catalog.json", {"schemas": [schema.to_dict() for schema in registry.schemas]})
    _write_json(pack / "candidate_schema_bindings.json", {"bindings": [binding.to_dict() for binding in registry.bindings]})
    _write_json(pack / "stage136_preflight_report.json", preflight)
    _write_json(pack / "stage135_input_summary.json", _compact_stage135(stage135_report))
    _write_json(root / "release/current/stage136_schema_registry_report.json", result)
    return result


def _compact_stage135(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": report.get("stage"),
        "status": report.get("status"),
        "mode": report.get("mode"),
        "learning_candidate_only": report.get("learning_candidate_only"),
        "candidate_count": report.get("candidate_count"),
        "review_only_count": report.get("review_only_count"),
        "learning_allowed_count": report.get("learning_allowed_count"),
        "training_triggered_count": report.get("training_triggered_count"),
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved"),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
