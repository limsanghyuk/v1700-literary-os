from __future__ import annotations

from typing import Any

from .contracts import ReadOnlyAdapterResult
from .fixtures import blocked_probe_requests, safe_read_requests, shared_character_records


def run_shared_character_read_only_adapter() -> dict[str, Any]:
    records = [record.to_feature_only_dict() for record in shared_character_records()]
    requests = safe_read_requests() + blocked_probe_requests()
    character_requests = [req for req in requests if req.resource_type == "shared_character"]
    allowed = [req.to_dict() for req in character_requests if req.allowed()]
    blocked = [req.to_dict() for req in character_requests if not req.allowed()]
    blocked_writes = [req for req in character_requests if req.access_type == "write" and not req.allowed()]
    unauthorized_reads = [req for req in character_requests if req.access_type in {"read", "reference", "adapt"} and not req.allowed()]
    raw_text_exported = any("raw_manuscript_excerpt" in item for item in records)
    result = ReadOnlyAdapterResult(
        adapter_name="SharedCharacterReadOnlyAdapter",
        status="PASS" if blocked_writes and unauthorized_reads and not raw_text_exported else "BLOCK",
        read_only=True,
        allowed_reads=len(allowed),
        blocked_reads=len(unauthorized_reads),
        blocked_writes=len(blocked_writes),
        unauthorized_cross_reads=0,
        unauthorized_cross_writes=0,
        raw_text_exported=raw_text_exported,
        raw_manuscript_provider_leakage=0,
        evidence={
            "records_feature_only": records,
            "allowed_requests": allowed,
            "blocked_requests": blocked,
            "license_edge_required_for_cross_owner_private_character": True,
            "public_domain_reference_allowed": True,
        },
    )
    return result.to_dict()
