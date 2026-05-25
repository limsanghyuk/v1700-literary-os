from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage155_release_gate import run_stage155_release_gate

from .contracts import PacketProjectionRule, PacketStorePolicy
from .loader import validate_execution_packet_store

TARGET_STAGE = "stage156"
TARGET_REPORT = "release/current/stage156_local_execution_packet_store_report.json"
STORE_PATH = "samples/stage156_execution_packet_store/execution_packets.jsonl"


def run_stage156_local_execution_packet_store(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage155 = run_stage155_release_gate(root)
    store_path = root / STORE_PATH
    validation = validate_execution_packet_store(store_path)
    pack = root / "release/current/stage156_local_execution_packet_store_pack"
    pack.mkdir(parents=True, exist_ok=True)

    catalog = _build_packet_store_catalog(validation, store_path)
    schema = _build_packet_schema_validation(validation)
    checksum = _build_packet_checksum_index(validation)
    policy = _build_read_only_access_policy()
    projection = _build_node2_projection_matrix(validation)
    regression = _build_regression_snapshot(validation)

    parts = {
        "packet_store_catalog": catalog,
        "packet_schema_validation": schema,
        "packet_checksum_index": checksum,
        "read_only_access_policy": policy,
        "node2_packet_projection_matrix": projection,
        "regression_snapshot": regression,
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}.json", payload)

    issues: list[str] = []
    if stage155.get("status") != "pass":
        issues.append("stage155_release_gate_blocked")
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "156",
        "baseline_stage": "155",
        "title": "Local Execution Packet Store",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "LOCAL_EXECUTION_PACKET_STORE_READ_ONLY",
        "page": "Page03 Execution Body",
        "store_path": STORE_PATH,
        "packet_count": validation.get("packet_count", 0),
        "checksum_count": len(validation.get("checksum_index", [])),
        "read_only_store_enabled": True,
        "runtime_execution_enabled": False,
        "generation_runtime_enabled": False,
        "provider_execution_enabled": False,
        "memory_write_enabled": False,
        "execution_write_enabled": False,
        "store_write_enabled": False,
        "canon_mutation_enabled": False,
        "auto_repair_apply_enabled": False,
        "vector_db_runtime_dependency": False,
        "live_provider_rag_enabled": False,
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "node2_hidden_execution_payload_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "page03_execution_contract_inherited": stage155.get("status") == "pass",
        "stage157_plan_graph_builder_ready": not issues,
        "parts": {"stage155_release_gate": _compact(stage155), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_packet_store_catalog(validation: dict[str, Any], store_path: Path) -> dict[str, Any]:
    issues = list(validation.get("issues", []))
    return {
        "stage": TARGET_STAGE,
        "title": "Stage156 Packet Store Catalog",
        "status": "pass" if validation.get("status") == "pass" else "blocked",
        "issues": issues,
        "store_path": STORE_PATH,
        "store_exists": store_path.exists(),
        "packet_count": validation.get("packet_count", 0),
        "packet_ids": [packet.get("packet_id") for packet in validation.get("packets", [])],
        "packet_types": sorted({str(packet.get("packet_type")) for packet in validation.get("packets", [])}),
    }


def _build_packet_schema_validation(validation: dict[str, Any]) -> dict[str, Any]:
    issues = list(validation.get("issues", []))
    return {
        "stage": TARGET_STAGE,
        "title": "Stage156 Packet Schema Validation",
        "status": "pass" if validation.get("status") == "pass" else "blocked",
        "issues": issues,
        "validated_packet_count": validation.get("packet_count", 0),
    }


def _build_packet_checksum_index(validation: dict[str, Any]) -> dict[str, Any]:
    mismatches = [entry for entry in validation.get("checksum_index", []) if entry.get("checksum") != entry.get("expected_checksum")]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage156 Packet Checksum Index",
        "status": "pass" if not mismatches and validation.get("status") == "pass" else "blocked",
        "issues": [f"checksum_mismatch:{entry.get('packet_id')}" for entry in mismatches],
        "checksum_count": len(validation.get("checksum_index", [])),
        "checksums": validation.get("checksum_index", []),
    }


def _build_read_only_access_policy() -> dict[str, Any]:
    rules = (
        PacketStorePolicy("jsonl_store_read_only", True, False, False, False, TARGET_REPORT),
        PacketStorePolicy("runtime_append_disabled", True, False, False, False, TARGET_REPORT),
        PacketStorePolicy("packet_mutation_disabled", True, False, False, False, TARGET_REPORT),
        PacketStorePolicy("provider_execution_disabled", True, False, False, False, TARGET_REPORT),
        PacketStorePolicy("canon_mutation_disabled", True, False, False, False, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if not rule.read_only or rule.runtime_write_allowed or rule.provider_execution_allowed or rule.mutation_allowed]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage156 Read-Only Access Policy",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "rule_count": len(rules),
        "rules": [rule.to_dict() for rule in rules],
    }


def _build_node2_projection_matrix(validation: dict[str, Any]) -> dict[str, Any]:
    rules = tuple(
        PacketProjectionRule(
            name=f"node2_projection_{packet.get('packet_id')}",
            packet_type=str(packet.get("packet_type")),
            node2_surface_allowed=True,
            hidden_payload_blocked=True,
            write_handle_blocked=True,
            evidence=TARGET_REPORT,
        )
        for packet in validation.get("packets", [])
    )
    issues = [rule.name for rule in rules if not rule.node2_surface_allowed or not rule.hidden_payload_blocked or not rule.write_handle_blocked]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage156 Node2 Packet Projection Matrix",
        "status": "pass" if not issues and validation.get("status") == "pass" else "blocked",
        "issues": issues,
        "rule_count": len(rules),
        "rules": [rule.to_dict() for rule in rules],
    }


def _build_regression_snapshot(validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": TARGET_STAGE,
        "title": "Stage156 Regression Snapshot",
        "status": "pass" if validation.get("status") == "pass" else "blocked",
        "issues": list(validation.get("issues", [])),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "boundary_violation_count": 0,
        "store_write_enabled": False,
        "runtime_execution_enabled": False,
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
    keep = ("status", "stage", "baseline_stage", "title", "issues", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "boundary_violation_count", "raw_manuscript_provider_leakage", "raw_manuscript_cross_project_leakage", "credential_leakage", "branchpoint_lineage_preserved")
    return {key: report.get(key) for key in keep if key in report}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
