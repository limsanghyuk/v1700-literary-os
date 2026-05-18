from __future__ import annotations

from typing import Any


def canon_conflict_score(*, timeline_conflict: float, world_rule_conflict: float, character_identity_conflict: float, relationship_conflict: float) -> float:
    return round(
        timeline_conflict * 0.35
        + world_rule_conflict * 0.30
        + character_identity_conflict * 0.20
        + relationship_conflict * 0.15,
        4,
    )


def density_status(score: float) -> str:
    if score <= 0.30:
        return "PASS"
    if score <= 0.60:
        return "WARN"
    return "BLOCK"


def run_shared_world_audit() -> dict[str, Any]:
    samples = [
        {"world_id": "canon_alpha", "timeline_conflict": 0.0, "world_rule_conflict": 0.0, "character_identity_conflict": 0.0, "relationship_conflict": 0.0},
        {"world_id": "canon_beta_probe", "timeline_conflict": 0.20, "world_rule_conflict": 0.10, "character_identity_conflict": 0.00, "relationship_conflict": 0.20},
        {"world_id": "blocked_canon_collision", "timeline_conflict": 1.0, "world_rule_conflict": 1.0, "character_identity_conflict": 0.5, "relationship_conflict": 0.6},
    ]
    assessed = []
    hard_blocks = 0
    for sample in samples:
        score = canon_conflict_score(
            timeline_conflict=sample["timeline_conflict"],
            world_rule_conflict=sample["world_rule_conflict"],
            character_identity_conflict=sample["character_identity_conflict"],
            relationship_conflict=sample["relationship_conflict"],
        )
        status = density_status(score)
        if status == "BLOCK":
            hard_blocks += 1
        assessed.append({**sample, "canon_conflict_score": score, "density_status": status})
    # A preflight is healthy when the synthetic blocked collision is detected, not silently allowed.
    blocked_fixture_detected = any(x["world_id"] == "blocked_canon_collision" and x["density_status"] == "BLOCK" for x in assessed)
    return {
        "status": "pass" if blocked_fixture_detected else "blocked",
        "assessed_worlds": assessed,
        "shared_world_conflicts": hard_blocks,
        "blocking_conflicts_detected": hard_blocks,
        "canon_conflict_report_required": True,
    }
