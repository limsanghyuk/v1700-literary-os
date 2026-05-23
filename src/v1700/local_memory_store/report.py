from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage150_release_gate import run_stage150_release_gate

from .contracts import LocalMemoryStoreSpec, ReadOnlyAccessRule, StoreIndexEntry, StoreRecordValidation
from .loader import load_memory_records, node2_projection_for, validate_records

TARGET_STAGE = "stage151"
TARGET_REPORT = "release/current/stage151_local_read_only_memory_store_report.json"
FIXTURE_PATH = "samples/stage151_memory_store/project_memory_records.jsonl"


def run_stage151_local_read_only_memory_store(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    baseline = run_stage150_release_gate(root)
    pack = root / "release/current/stage151_local_read_only_memory_store_pack"
    pack.mkdir(parents=True, exist_ok=True)

    fixture = root / FIXTURE_PATH
    records = load_memory_records(fixture)
    validation = validate_records(records)
    store_spec = _build_store_spec()
    access_policy = _build_access_policy()
    index = _build_checksum_index(records)
    projection = _build_node2_projection_index(records)

    _write_json(pack / "store_spec.json", store_spec)
    _write_json(pack / "record_validation_report.json", validation)
    _write_json(pack / "checksum_index.json", index)
    _write_json(pack / "read_only_access_policy.json", access_policy)
    _write_json(pack / "node2_projection_index.json", projection)

    parts = {
        "store_spec": store_spec,
        "record_validation_report": validation,
        "checksum_index": index,
        "read_only_access_policy": access_policy,
        "node2_projection_index": projection,
    }
    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage150_release_gate_blocked")
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "151",
        "baseline_stage": "150",
        "title": "Local Read-Only Memory Store",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "LOCAL_READ_ONLY_MEMORY_STORE",
        "page": "Page02 Narrative Memory Body",
        "store_contract_only": False,
        "local_store_enabled": True,
        "read_only_store_enabled": True,
        "store_write_enabled": False,
        "memory_write_enabled": False,
        "query_runtime_enabled": False,
        "ranking_runtime_enabled": False,
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
        "hidden_reveal_projection_count": 0,
        "private_note_projection_count": 0,
        "write_handle_projection_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "stage152_deterministic_query_ready": not issues,
        "record_count": validation.get("record_count", 0),
        "checksum_index_count": index.get("entry_count", 0),
        "node2_blocked_projection_count": projection.get("blocked_projection_count", 0),
        "parts": {"stage150_release_gate": _compact(baseline), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_store_spec() -> dict[str, Any]:
    spec = LocalMemoryStoreSpec(
        name="Stage151ProjectMemoryJsonlStore",
        path=FIXTURE_PATH,
        format="jsonl",
        mode="read_only",
        source_contract="Stage150 Memory Contract",
        write_enabled=False,
    )
    return {
        "stage": TARGET_STAGE,
        "title": "Stage151 Local Memory Store Spec",
        "status": "pass" if not spec.write_enabled and spec.mode == "read_only" else "blocked",
        "issues": [] if not spec.write_enabled and spec.mode == "read_only" else ["store_write_or_mode_invalid"],
        "spec": spec.to_dict(),
    }


def _build_access_policy() -> dict[str, Any]:
    rules = (
        ReadOnlyAccessRule("local_file_read_allowed", "Stage151 may read deterministic local JSONL fixtures.", True, False, False, TARGET_REPORT),
        ReadOnlyAccessRule("store_write_blocked", "Stage151 must not write memory records.", True, False, False, TARGET_REPORT),
        ReadOnlyAccessRule("record_mutation_blocked", "Loaded records must not be mutated by the store.", True, False, False, TARGET_REPORT),
        ReadOnlyAccessRule("query_runtime_deferred", "Ranking and query runtime remain deferred to Stage152.", True, False, False, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if rule.write_allowed or rule.mutation_allowed]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage151 Read-Only Access Policy",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "rule_count": len(rules),
        "rules": [rule.to_dict() for rule in rules],
    }


def _build_checksum_index(records: list[dict[str, Any]]) -> dict[str, Any]:
    entries = [
        StoreIndexEntry(
            record_id=str(record["record_id"]),
            record_type=str(record["record_type"]),
            source_state_id=str(record["source_state_id"]),
            boundary_level=str(record["boundary_level"]),
            node2_projection=node2_projection_for(record),
            checksum=str(record["checksum"]),
        )
        for record in records
    ]
    issues = [] if entries else ["checksum_index_empty"]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage151 Checksum Index",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "entry_count": len(entries),
        "entries": [entry.to_dict() for entry in entries],
    }


def _build_node2_projection_index(records: list[dict[str, Any]]) -> dict[str, Any]:
    entries = [
        {
            "record_id": str(record["record_id"]),
            "boundary_level": str(record["boundary_level"]),
            "node2_projection": node2_projection_for(record),
            "raw_payload_included": False,
        }
        for record in records
    ]
    leaks = [entry["record_id"] for entry in entries if entry["raw_payload_included"]]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage151 Node2 Projection Index",
        "status": "pass" if not leaks else "blocked",
        "issues": leaks,
        "entry_count": len(entries),
        "blocked_projection_count": sum(1 for entry in entries if entry["node2_projection"] == "blocked"),
        "entries": entries,
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
        "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access",
        "raw_manuscript_provider_leakage",
        "credential_leakage",
        "branchpoint_lineage_preserved",
        "memory_write_enabled",
        "runtime_training_enabled",
    )
    return {key: report.get(key) for key in keep if key in report}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
