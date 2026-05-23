from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = (
    "record_id",
    "project_id",
    "record_type",
    "source_stage",
    "source_state_id",
    "visibility",
    "boundary_level",
    "created_from",
    "checksum",
    "write_policy",
)

NODE2_BLOCKED_BOUNDARIES = {"PLANNER_PRIVATE", "HIDDEN_REVEAL", "PRIVATE_NOTE", "WRITE_HANDLE"}


def stable_record_checksum(record: dict[str, Any]) -> str:
    payload = {key: value for key, value in record.items() if key != "checksum"}
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def load_memory_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        records.append(json.loads(line))
    return records


def validate_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    ids = [str(record.get("record_id", "")) for record in records]
    missing_required = [record.get("record_id", "<unknown>") for record in records if any(field not in record for field in REQUIRED_FIELDS)]
    checksum_mismatches = [record.get("record_id", "<unknown>") for record in records if record.get("checksum") != stable_record_checksum(record)]
    write_enabled = [record.get("record_id", "<unknown>") for record in records if record.get("write_policy") != "DISABLED_BY_DEFAULT"]
    duplicates = sorted({record_id for record_id in ids if ids.count(record_id) > 1})
    hidden_payload_leaks = [
        record.get("record_id", "<unknown>")
        for record in records
        if any(key in record for key in ("hidden_reveal_payload", "private_note", "write_handle", "raw_manuscript_payload"))
    ]
    issues = []
    for name, values in {
        "missing_required_fields": missing_required,
        "checksum_mismatches": checksum_mismatches,
        "write_policy_enabled": write_enabled,
        "duplicate_record_ids": duplicates,
        "hidden_payload_leaks": hidden_payload_leaks,
    }.items():
        if values:
            issues.append(f"{name}:{','.join(map(str, values))}")
    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "record_count": len(records),
        "required_fields": list(REQUIRED_FIELDS),
        "missing_required_fields": missing_required,
        "checksum_mismatches": checksum_mismatches,
        "write_policy_enabled": write_enabled,
        "duplicate_record_ids": duplicates,
        "hidden_payload_leaks": hidden_payload_leaks,
    }


def node2_projection_for(record: dict[str, Any]) -> str:
    boundary = str(record.get("boundary_level", ""))
    if boundary in NODE2_BLOCKED_BOUNDARIES:
        return "blocked"
    return "surface_safe"
