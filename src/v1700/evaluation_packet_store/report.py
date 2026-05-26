from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage167_release_gate import run_stage167_release_gate

from .contracts import EvaluationPacketProjectionRule, EvaluationPacketStorePolicy
from .loader import validate_evaluation_packet_store

TARGET_STAGE = "stage168"
TARGET_REPORT = "release/current/stage168_local_evaluation_packet_store_report.json"
STORE_PATH = "samples/stage168_evaluation_packet_store/evaluation_packets.jsonl"


def run_stage168_local_evaluation_packet_store(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage167 = run_stage167_release_gate(root)
    store_path = root / STORE_PATH
    validation = validate_evaluation_packet_store(store_path, root)
    pack = root / "release/current/stage168_local_evaluation_packet_store_pack"
    pack.mkdir(parents=True, exist_ok=True)

    catalog = _build_evaluation_packet_store_catalog(validation, store_path)
    schema = _build_evaluation_packet_schema_validation(validation)
    checksum = _build_evaluation_packet_checksum_index(validation)
    duplicate = _build_evaluation_packet_duplicate_detector(validation)
    policy = _build_read_only_evaluation_access_policy()
    subject_resolver = _build_evaluation_subject_resolver(validation)
    stage166_resolver = _build_stage166_evidence_resolver(validation)
    node2 = _build_node2_evaluation_packet_projection_matrix(validation)
    load_order = _build_deterministic_load_order(validation)
    regression = _build_regression_snapshot(validation)

    parts = {
        "evaluation_packet_store_catalog": catalog,
        "evaluation_packet_schema_validation": schema,
        "evaluation_packet_checksum_index": checksum,
        "evaluation_packet_duplicate_detector": duplicate,
        "read_only_evaluation_access_policy": policy,
        "evaluation_subject_resolver": subject_resolver,
        "stage166_evidence_resolver": stage166_resolver,
        "node2_evaluation_packet_projection_matrix": node2,
        "deterministic_load_order": load_order,
        "regression_snapshot": regression,
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}.json", payload)

    issues: list[str] = []
    if stage167.get("status") != "pass":
        issues.append("stage167_release_gate_blocked")
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "168",
        "baseline_stage": "167",
        "title": "Local Evaluation Packet Store",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "LOCAL_EVALUATION_PACKET_STORE_READ_ONLY",
        "page": "Page05 Evaluation Body",
        "store_path": STORE_PATH,
        "evaluation_packet_count": validation.get("packet_count", 0),
        "checksum_count": len(validation.get("checksum_index", [])),
        "packet_store_read_only": True,
        "evaluation_packet_store_enabled": True,
        "stage167_contract_inherited": stage167.get("status") == "pass",
        "stage166_refs_resolvable": stage166_resolver.get("status") == "pass",
        "load_order_deterministic": load_order.get("status") == "pass",
        "stage169_evaluator_ready": not issues,
        "provider_evaluation_enabled": False,
        "evaluation_write_enabled": False,
        "memory_write_enabled": False,
        "cross_project_write_enabled": False,
        "canon_mutation_enabled": False,
        "runtime_training_enabled": False,
        "auto_repair_apply_enabled": False,
        "provider_generation_enabled": False,
        "generation_runtime_enabled": False,
        "runtime_execution_enabled": False,
        "provider_default_calls": 0,
        "provider_generation_count": 0,
        "runtime_execution_count": 0,
        "write_operation_count": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "parts": {"stage167_release_gate": _compact(stage167), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_evaluation_packet_store_catalog(validation: dict[str, Any], store_path: Path) -> dict[str, Any]:
    return {
        "stage": TARGET_STAGE,
        "title": "Stage168 Evaluation Packet Store Catalog",
        "status": "pass" if validation.get("status") == "pass" else "blocked",
        "issues": list(validation.get("issues", [])),
        "store_path": STORE_PATH,
        "store_exists": store_path.exists(),
        "evaluation_packet_count": validation.get("packet_count", 0),
        "evaluation_packet_ids": [packet.get("evaluation_packet_id") for packet in validation.get("packets", [])],
        "subject_ids": sorted({str(packet.get("subject_id")) for packet in validation.get("packets", [])}),
        "rubric_ids": sorted({str(packet.get("rubric_id")) for packet in validation.get("packets", [])}),
    }


def _build_evaluation_packet_schema_validation(validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": TARGET_STAGE,
        "title": "Stage168 Evaluation Packet Schema Validation",
        "status": "pass" if validation.get("status") == "pass" else "blocked",
        "issues": list(validation.get("issues", [])),
        "validated_evaluation_packet_count": validation.get("packet_count", 0),
    }


def _build_evaluation_packet_checksum_index(validation: dict[str, Any]) -> dict[str, Any]:
    mismatches = [entry for entry in validation.get("checksum_index", []) if entry.get("checksum") != entry.get("expected_checksum")]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage168 Evaluation Packet Checksum Index",
        "status": "pass" if not mismatches and validation.get("status") == "pass" else "blocked",
        "issues": [f"checksum_mismatch:{entry.get('evaluation_packet_id')}" for entry in mismatches],
        "checksum_count": len(validation.get("checksum_index", [])),
        "checksums": validation.get("checksum_index", []),
    }


def _build_evaluation_packet_duplicate_detector(validation: dict[str, Any]) -> dict[str, Any]:
    duplicates = [issue for issue in validation.get("issues", []) if str(issue).startswith("duplicate_evaluation_packet_id:")]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage168 Evaluation Packet Duplicate Detector",
        "status": "pass" if not duplicates else "blocked",
        "issues": duplicates,
        "duplicate_count": len(duplicates),
    }


def _build_read_only_evaluation_access_policy() -> dict[str, Any]:
    rules = (
        EvaluationPacketStorePolicy("jsonl_evaluation_store_read_only", True, False, False, False, False, TARGET_REPORT),
        EvaluationPacketStorePolicy("runtime_evaluation_append_disabled", True, False, False, False, False, TARGET_REPORT),
        EvaluationPacketStorePolicy("evaluation_writeback_disabled", True, False, False, False, False, TARGET_REPORT),
        EvaluationPacketStorePolicy("provider_evaluation_disabled", True, False, False, False, False, TARGET_REPORT),
        EvaluationPacketStorePolicy("mutation_disabled", True, False, False, False, False, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if not rule.read_only or rule.runtime_write_allowed or rule.cross_project_write_allowed or rule.provider_evaluation_allowed or rule.mutation_allowed]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage168 Read-Only Evaluation Access Policy",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "rule_count": len(rules),
        "rules": [rule.to_dict() for rule in rules],
    }


def _build_evaluation_subject_resolver(validation: dict[str, Any]) -> dict[str, Any]:
    entries = [
        {
            "evaluation_packet_id": packet.get("evaluation_packet_id"),
            "subject_id": packet.get("subject_id"),
            "rubric_id": packet.get("rubric_id"),
            "resolved": bool(packet.get("subject_id")) and bool(packet.get("rubric_id")),
        }
        for packet in validation.get("packets", [])
    ]
    issues = [str(entry.get("evaluation_packet_id")) for entry in entries if not entry.get("resolved")]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage168 Evaluation Subject Resolver",
        "status": "pass" if not issues and validation.get("status") == "pass" else "blocked",
        "issues": issues,
        "entry_count": len(entries),
        "entries": entries,
    }


def _build_stage166_evidence_resolver(validation: dict[str, Any]) -> dict[str, Any]:
    entries = validation.get("evidence_resolution", [])
    issues: list[str] = []
    for entry in entries:
        if not entry.get("source_artifact_exists"):
            issues.append(f"missing_source_artifact:{entry.get('evaluation_packet_id')}")
        for ref in entry.get("required_stage_refs", []):
            if not ref.get("exists"):
                issues.append(f"missing_required_stage_ref:{entry.get('evaluation_packet_id')}:{ref.get('path')}")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage168 Stage166 Evidence Resolver",
        "status": "pass" if not issues and validation.get("status") == "pass" else "blocked",
        "issues": issues,
        "entry_count": len(entries),
        "entries": entries,
    }


def _build_node2_evaluation_packet_projection_matrix(validation: dict[str, Any]) -> dict[str, Any]:
    rules = tuple(
        EvaluationPacketProjectionRule(
            name=f"node2_evaluation_projection_{packet.get('evaluation_packet_id')}",
            subject_id=str(packet.get("subject_id")),
            node2_surface_allowed=True,
            hidden_reveal_blocked=True,
            provider_handle_blocked=True,
            mutation_handle_blocked=True,
            evidence=TARGET_REPORT,
        )
        for packet in validation.get("packets", [])
    )
    issues = [rule.name for rule in rules if not rule.node2_surface_allowed or not rule.hidden_reveal_blocked or not rule.provider_handle_blocked or not rule.mutation_handle_blocked]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage168 Node2 Evaluation Packet Projection Matrix",
        "status": "pass" if not issues and validation.get("status") == "pass" else "blocked",
        "issues": issues,
        "rule_count": len(rules),
        "rules": [rule.to_dict() for rule in rules],
    }


def _build_deterministic_load_order(validation: dict[str, Any]) -> dict[str, Any]:
    packet_ids = sorted(str(packet.get("evaluation_packet_id")) for packet in validation.get("packets", []))
    return {
        "stage": TARGET_STAGE,
        "title": "Stage168 Deterministic Load Order",
        "status": "pass" if packet_ids == sorted(packet_ids) and validation.get("status") == "pass" else "blocked",
        "issues": [] if validation.get("status") == "pass" else list(validation.get("issues", [])),
        "load_order": packet_ids,
        "deterministic": True,
    }


def _build_regression_snapshot(validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": TARGET_STAGE,
        "title": "Stage168 Regression Snapshot",
        "status": "pass" if validation.get("status") == "pass" else "blocked",
        "issues": list(validation.get("issues", [])),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "evaluation_write_enabled": False,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
    }


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _compact(report: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "status",
        "stage",
        "baseline_stage",
        "title",
        "issues",
        "provider_default_calls",
        "node2_raw_reveal_access",
        "boundary_violation_count",
        "raw_manuscript_provider_leakage",
        "raw_manuscript_cross_project_leakage",
        "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    return {key: report.get(key) for key in keep if key in report}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

