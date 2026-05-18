from __future__ import annotations

from typing import Any

from .shared_world_adapter import canon_conflict_score, canon_status


def run_canon_conflict_report() -> dict[str, Any]:
    rows = [
        {"conflict_id": "canon_safe_001", "world_id": "world_alpha_city", "timeline_conflict": 0.0, "world_rule_conflict": 0.0, "character_identity_conflict": 0.0, "relationship_conflict": 0.0, "recommended_action": "allow read-only projection"},
        {"conflict_id": "canon_warn_001", "world_id": "world_beta_port", "timeline_conflict": 0.35, "world_rule_conflict": 0.20, "character_identity_conflict": 0.0, "relationship_conflict": 0.10, "recommended_action": "warn and defer authority to Stage129"},
        {"conflict_id": "canon_block_001", "world_id": "blocked_canon_collision", "timeline_conflict": 1.0, "world_rule_conflict": 1.0, "character_identity_conflict": 0.5, "relationship_conflict": 0.6, "recommended_action": "block write/truth promotion; require Stage129 Canon Governor"},
    ]
    assessed=[]
    for row in rows:
        score=canon_conflict_score(
            timeline_conflict=row["timeline_conflict"],
            world_rule_conflict=row["world_rule_conflict"],
            character_identity_conflict=row["character_identity_conflict"],
            relationship_conflict=row["relationship_conflict"],
        )
        assessed.append({**row, "canon_conflict_score": score, "status": canon_status(score)})
    return {
        "status": "pass" if any(x["status"] == "BLOCK" for x in assessed) else "blocked",
        "canon_conflicts": assessed,
        "blocking_conflicts_detected": len([x for x in assessed if x["status"] == "BLOCK"]),
        "shared_world_source_of_truth_promotion_allowed": False,
        "stage129_canon_governor_required": True,
    }
