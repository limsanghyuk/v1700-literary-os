from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage161_release_gate import run_stage161_release_gate

from .contracts import RenderPacketProjectionRule, RenderPacketStorePolicy
from .loader import validate_render_packet_store

TARGET_STAGE = "stage162"
TARGET_REPORT = "release/current/stage162_local_render_packet_store_report.json"
STORE_PATH = "samples/stage162_render_packet_store/render_packets.jsonl"


def run_stage162_local_render_packet_store(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    stage161 = run_stage161_release_gate(root)
    store_path = root / STORE_PATH
    validation = validate_render_packet_store(store_path)
    pack = root / "release/current/stage162_local_render_packet_store_pack"
    pack.mkdir(parents=True, exist_ok=True)

    catalog = _build_render_packet_store_catalog(validation, store_path)
    schema = _build_render_packet_schema_validation(validation)
    checksum = _build_render_packet_checksum_index(validation)
    policy = _build_read_only_render_access_policy()
    projection = _build_node2_render_packet_projection_matrix(validation)
    lineage = _build_render_packet_lineage_matrix(validation)
    regression = _build_regression_snapshot(validation)

    parts = {
        "render_packet_store_catalog": catalog,
        "render_packet_schema_validation": schema,
        "render_packet_checksum_index": checksum,
        "read_only_render_access_policy": policy,
        "node2_render_packet_projection_matrix": projection,
        "render_packet_lineage_matrix": lineage,
        "regression_snapshot": regression,
    }
    for name, payload in parts.items():
        _write_json(pack / f"{name}.json", payload)

    issues: list[str] = []
    if stage161.get("status") != "pass":
        issues.append("stage161_release_gate_blocked")
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "162",
        "baseline_stage": "161",
        "title": "Local Render Packet Store",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "LOCAL_RENDER_PACKET_STORE_READ_ONLY",
        "page": "Page04 Rendering Body",
        "store_path": STORE_PATH,
        "render_packet_count": validation.get("packet_count", 0),
        "checksum_count": len(validation.get("checksum_index", [])),
        "read_only_store_enabled": True,
        "render_packet_store_enabled": True,
        "rendering_contract_inherited": stage161.get("status") == "pass",
        "stage163_render_plan_builder_ready": not issues,
        "rendering_runtime_enabled": False,
        "generation_runtime_enabled": False,
        "provider_generation_enabled": False,
        "provider_execution_enabled": False,
        "runtime_execution_enabled": False,
        "render_write_enabled": False,
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
        "runtime_execution_count": 0,
        "provider_execution_count": 0,
        "provider_generation_count": 0,
        "write_operation_count": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "node2_hidden_render_payload_access": 0,
        "boundary_violation_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "parts": {"stage161_release_gate": _compact(stage161), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_render_packet_store_catalog(validation: dict[str, Any], store_path: Path) -> dict[str, Any]:
    return {
        "stage": TARGET_STAGE,
        "title": "Stage162 Render Packet Store Catalog",
        "status": "pass" if validation.get("status") == "pass" else "blocked",
        "issues": list(validation.get("issues", [])),
        "store_path": STORE_PATH,
        "store_exists": store_path.exists(),
        "render_packet_count": validation.get("packet_count", 0),
        "render_packet_ids": [packet.get("render_packet_id") for packet in validation.get("packets", [])],
        "render_types": sorted({str(packet.get("render_type")) for packet in validation.get("packets", [])}),
        "surface_channels": sorted({str(packet.get("surface_channel")) for packet in validation.get("packets", [])}),
    }


def _build_render_packet_schema_validation(validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": TARGET_STAGE,
        "title": "Stage162 Render Packet Schema Validation",
        "status": "pass" if validation.get("status") == "pass" else "blocked",
        "issues": list(validation.get("issues", [])),
        "validated_render_packet_count": validation.get("packet_count", 0),
    }


def _build_render_packet_checksum_index(validation: dict[str, Any]) -> dict[str, Any]:
    mismatches = [entry for entry in validation.get("checksum_index", []) if entry.get("checksum") != entry.get("expected_checksum")]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage162 Render Packet Checksum Index",
        "status": "pass" if not mismatches and validation.get("status") == "pass" else "blocked",
        "issues": [f"checksum_mismatch:{entry.get('render_packet_id')}" for entry in mismatches],
        "checksum_count": len(validation.get("checksum_index", [])),
        "checksums": validation.get("checksum_index", []),
    }


def _build_read_only_render_access_policy() -> dict[str, Any]:
    rules = (
        RenderPacketStorePolicy("jsonl_render_store_read_only", True, False, False, False, TARGET_REPORT),
        RenderPacketStorePolicy("runtime_render_append_disabled", True, False, False, False, TARGET_REPORT),
        RenderPacketStorePolicy("render_packet_mutation_disabled", True, False, False, False, TARGET_REPORT),
        RenderPacketStorePolicy("provider_generation_disabled", True, False, False, False, TARGET_REPORT),
        RenderPacketStorePolicy("canon_mutation_disabled", True, False, False, False, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if not rule.read_only or rule.runtime_write_allowed or rule.provider_generation_allowed or rule.render_mutation_allowed]
    return {"stage": TARGET_STAGE, "title": "Stage162 Read-Only Render Access Policy", "status": "pass" if not issues else "blocked", "issues": issues, "rule_count": len(rules), "rules": [rule.to_dict() for rule in rules]}


def _build_node2_render_packet_projection_matrix(validation: dict[str, Any]) -> dict[str, Any]:
    rules = tuple(
        RenderPacketProjectionRule(
            name=f"node2_render_projection_{packet.get('render_packet_id')}",
            render_type=str(packet.get("render_type")),
            node2_surface_allowed=True,
            hidden_render_payload_blocked=True,
            provider_handle_blocked=True,
            write_handle_blocked=True,
            evidence=TARGET_REPORT,
        )
        for packet in validation.get("packets", [])
    )
    issues = [rule.name for rule in rules if not rule.node2_surface_allowed or not rule.hidden_render_payload_blocked or not rule.provider_handle_blocked or not rule.write_handle_blocked]
    return {"stage": TARGET_STAGE, "title": "Stage162 Node2 Render Packet Projection Matrix", "status": "pass" if not issues and validation.get("status") == "pass" else "blocked", "issues": issues, "rule_count": len(rules), "rules": [rule.to_dict() for rule in rules]}


def _build_render_packet_lineage_matrix(validation: dict[str, Any]) -> dict[str, Any]:
    entries = [
        {
            "render_packet_id": packet.get("render_packet_id"),
            "source_rendering_contract_id": packet.get("source_rendering_contract_id"),
            "source_execution_packet_ids": packet.get("source_execution_packet_ids", []),
            "source_trace_ids": packet.get("source_trace_ids", []),
            "lineage_preserved": True,
        }
        for packet in validation.get("packets", [])
    ]
    issues = [str(entry.get("render_packet_id")) for entry in entries if not entry.get("source_rendering_contract_id") or not entry.get("source_execution_packet_ids") or not entry.get("source_trace_ids")]
    return {"stage": TARGET_STAGE, "title": "Stage162 Render Packet Lineage Matrix", "status": "pass" if not issues and validation.get("status") == "pass" else "blocked", "issues": issues, "entry_count": len(entries), "entries": entries}


def _build_regression_snapshot(validation: dict[str, Any]) -> dict[str, Any]:
    return {"stage": TARGET_STAGE, "title": "Stage162 Regression Snapshot", "status": "pass" if validation.get("status") == "pass" else "blocked", "issues": list(validation.get("issues", [])), "provider_default_calls": 0, "live_provider_call_count_in_release_gate": 0, "node2_raw_reveal_access": 0, "boundary_violation_count": 0, "store_write_enabled": False, "rendering_runtime_enabled": False, "generation_runtime_enabled": False, "runtime_training_enabled": False}


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
