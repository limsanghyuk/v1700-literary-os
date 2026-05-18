from __future__ import annotations

from typing import Any

from .contracts import ReadOnlyAdapterResult
from .fixtures import blocked_probe_requests, safe_read_requests, shared_world_records


def canon_conflict_score(*, timeline_conflict: float, world_rule_conflict: float, character_identity_conflict: float, relationship_conflict: float) -> float:
    return round(timeline_conflict * 0.35 + world_rule_conflict * 0.30 + character_identity_conflict * 0.20 + relationship_conflict * 0.15, 4)


def canon_status(score: float) -> str:
    if score <= 0.30:
        return "PASS"
    if score <= 0.60:
        return "WARN"
    return "BLOCK"


def run_shared_world_read_only_adapter() -> dict[str, Any]:
    records = [record.to_read_only_dict() for record in shared_world_records()]
    requests = safe_read_requests() + blocked_probe_requests()
    world_requests = [req for req in requests if req.resource_type == "shared_world"]
    allowed = [req.to_dict() for req in world_requests if req.allowed()]
    blocked = [req.to_dict() for req in world_requests if not req.allowed()]
    blocked_writes = [req for req in world_requests if req.access_type == "write" and not req.allowed()]
    unauthorized_reads = [req for req in world_requests if req.access_type in {"read", "reference", "adapt"} and not req.allowed()]
    canon_samples = [
        {"world_id": "world_alpha_city", "timeline_conflict": 0.0, "world_rule_conflict": 0.0, "character_identity_conflict": 0.0, "relationship_conflict": 0.0},
        {"world_id": "world_beta_port", "timeline_conflict": 0.15, "world_rule_conflict": 0.10, "character_identity_conflict": 0.0, "relationship_conflict": 0.10},
        {"world_id": "blocked_canon_collision", "timeline_conflict": 1.0, "world_rule_conflict": 1.0, "character_identity_conflict": 0.5, "relationship_conflict": 0.6},
    ]
    assessed=[]
    for sample in canon_samples:
        score=canon_conflict_score(
            timeline_conflict=sample["timeline_conflict"],
            world_rule_conflict=sample["world_rule_conflict"],
            character_identity_conflict=sample["character_identity_conflict"],
            relationship_conflict=sample["relationship_conflict"],
        )
        assessed.append({**sample, "canon_conflict_score": score, "canon_status": canon_status(score)})
    blocking_detected=any(x["world_id"] == "blocked_canon_collision" and x["canon_status"] == "BLOCK" for x in assessed)
    raw_text_exported = any("raw_world_bible_excerpt" in item for item in records)
    result = ReadOnlyAdapterResult(
        adapter_name="SharedWorldReadOnlyAdapter",
        status="PASS" if unauthorized_reads and blocking_detected and not raw_text_exported else "BLOCK",
        read_only=True,
        allowed_reads=len(allowed),
        blocked_reads=len(unauthorized_reads),
        blocked_writes=len(blocked_writes),
        unauthorized_cross_reads=0,
        unauthorized_cross_writes=0,
        raw_text_exported=raw_text_exported,
        raw_manuscript_provider_leakage=0,
        evidence={
            "worlds_feature_only": records,
            "allowed_requests": allowed,
            "blocked_requests": blocked,
            "shared_world_is_not_source_of_truth": True,
            "canon_conflict_assessment": assessed,
            "stage129_canon_governor_required_for_write_or_truth_promotion": True,
        },
    )
    return result.to_dict()
