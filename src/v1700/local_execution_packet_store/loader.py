from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = (
    "packet_id",
    "project_id",
    "packet_type",
    "source_execution_contract_id",
    "source_memory_record_ids",
    "dependency_ids",
    "boundary_level",
    "visibility",
    "execution_mode",
    "payload_summary",
    "node2_projection_summary",
    "created_from",
    "checksum",
    "write_policy",
)

FORBIDDEN_NODE2_TOKENS = (
    "hidden_reveal_payload",
    "private_note",
    "provider_payload",
    "write_handle",
    "canon_mutation_command",
    "learning_payload",
    "raw_manuscript_payload",
    "credential",
)


def canonical_packet_payload(packet: dict[str, Any]) -> dict[str, Any]:
    payload = dict(packet)
    payload.pop("checksum", None)
    return payload


def compute_packet_checksum(packet: dict[str, Any]) -> str:
    body = json.dumps(canonical_packet_payload(packet), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def load_execution_packets(path: Path) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            packet = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid_jsonl_line:{line_no}:{exc.msg}") from exc
        if not isinstance(packet, dict):
            raise ValueError(f"invalid_packet_shape:{line_no}")
        packets.append(packet)
    return packets


def validate_execution_packet_store(path: Path) -> dict[str, Any]:
    issues: list[str] = []
    if not path.exists():
        return {"status": "blocked", "issues": [f"missing_store:{path.as_posix()}"], "packet_count": 0, "packets": [], "checksum_index": []}

    packets = load_execution_packets(path)
    seen: set[str] = set()
    checksum_index: list[dict[str, str]] = []
    for index, packet in enumerate(packets, start=1):
        missing = [field for field in REQUIRED_FIELDS if field not in packet]
        if missing:
            issues.append(f"packet_{index}_missing:{','.join(missing)}")
            continue
        packet_id = str(packet["packet_id"])
        if packet_id in seen:
            issues.append(f"duplicate_packet_id:{packet_id}")
        seen.add(packet_id)
        expected = compute_packet_checksum(packet)
        if packet.get("checksum") != expected:
            issues.append(f"checksum_mismatch:{packet_id}")
        if packet.get("write_policy") != "READ_ONLY_DISABLED_WRITE":
            issues.append(f"write_policy_not_disabled:{packet_id}")
        if packet.get("execution_mode") not in {"DRY_RUN_ONLY", "PLAN_ONLY"}:
            issues.append(f"runtime_execution_mode_enabled:{packet_id}")
        surface = json.dumps(packet.get("node2_projection_summary", ""), ensure_ascii=False).lower()
        for token in FORBIDDEN_NODE2_TOKENS:
            if token in surface:
                issues.append(f"node2_forbidden_token:{packet_id}:{token}")
        checksum_index.append({"packet_id": packet_id, "checksum": str(packet.get("checksum", "")), "expected_checksum": expected})

    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "packet_count": len(packets),
        "packets": packets,
        "checksum_index": checksum_index,
    }
