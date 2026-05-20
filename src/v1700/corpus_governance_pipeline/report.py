from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.stage138 import run_stage138

from .gate import CORPUS_GOVERNANCE_MODE, build_corpus_governance_pipeline
from .preflight import run_stage139_preflight


def run_stage139_corpus_governance_pipeline(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    pack = root / "release/current/stage139_corpus_governance_pipeline_pack"
    pack.mkdir(parents=True, exist_ok=True)
    stage138_report = run_stage138(root)
    pipeline = build_corpus_governance_pipeline(stage138_report)
    preflight = run_stage139_preflight(root)
    issues = list(pipeline.issues)
    if preflight.get("status") != "pass":
        issues.append("stage139_preflight_blocked")
    total_items = (
        pipeline.counters.get("governance_profile_count", 0)
        + pipeline.counters.get("case_packet_count", 0)
        + pipeline.counters.get("review_queue_packet_count", 0)
    )
    result = {
        "stage": "139",
        "baseline_stage": "138",
        "title": "Corpus Governance Pipeline & Stage140 Release Readiness",
        "status": "pass" if not issues and pipeline.status == "pass" else "blocked",
        "issues": issues,
        "mode": CORPUS_GOVERNANCE_MODE,
        "corpus_governance_pipeline_only": True,
        "governance_profile_count": pipeline.counters.get("governance_profile_count", 0),
        "case_packet_count": pipeline.counters.get("case_packet_count", 0),
        "review_queue_packet_count": pipeline.counters.get("review_queue_packet_count", 0),
        "governed_case_count": pipeline.counters.get("governed_case_count", 0),
        "review_required_case_count": pipeline.counters.get("review_required_case_count", 0),
        "retention_ready_count": pipeline.counters.get("retention_ready_count", 0),
        "audit_trail_ready_count": pipeline.counters.get("audit_trail_ready_count", 0),
        "stage140_release_ready_count": pipeline.counters.get("stage140_release_ready_count", 0),
        "execution_blocked_count": pipeline.counters.get("execution_blocked_count", 0),
        "rollback_ready_count": pipeline.counters.get("rollback_ready_count", 0),
        "policy_binding_count": pipeline.counters.get("policy_binding_count", 0),
        "unique_profile_count": pipeline.counters.get("unique_profile_count", 0),
        "total_pipeline_items": total_items,
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
            "stage138_report": _compact_stage138(stage138_report),
            "corpus_governance_pipeline": pipeline.to_dict(),
            "preflight": preflight,
        },
    }
    _write_json(pack / "governance_pipeline.json", pipeline.to_dict())
    _write_json(pack / "namespace_governance_profiles.json", {"profiles": [profile.to_dict() for profile in pipeline.governance_profiles]})
    _write_json(pack / "corpus_case_packets.json", {"case_packets": [packet.to_dict() for packet in pipeline.case_packets]})
    _write_json(pack / "review_queue_packets.json", {"review_queue_packets": [packet.to_dict() for packet in pipeline.review_queue_packets]})
    _write_json(pack / "stage138_input_summary.json", _compact_stage138(stage138_report))
    _write_json(pack / "stage139_preflight_report.json", preflight)
    _write_json(root / "release/current/stage139_corpus_governance_pipeline_report.json", result)
    return result


def _compact_stage138(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": report.get("stage"),
        "status": report.get("status"),
        "mode": report.get("mode"),
        "storage_contract_catalog_only": report.get("storage_contract_catalog_only"),
        "schema_contract_count": report.get("schema_contract_count"),
        "binding_route_count": report.get("binding_route_count"),
        "approval_lane_count": report.get("approval_lane_count"),
        "governance_ready_count": report.get("governance_ready_count"),
        "rollback_ready_count": report.get("rollback_ready_count"),
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved"),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
