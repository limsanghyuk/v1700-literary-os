from __future__ import annotations

from typing import Any, Literal

from .contracts import CanonGovernorDecision
from .fixtures import canon_conflict_fixtures


def canon_conflict_score(*, timeline_conflict: float, world_rule_conflict: float, character_identity_conflict: float, relationship_conflict: float) -> float:
    score = (
        timeline_conflict * 0.35
        + world_rule_conflict * 0.30
        + character_identity_conflict * 0.20
        + relationship_conflict * 0.15
    )
    return round(score, 6)


def canon_status(score: float) -> Literal["PASS", "WARN", "BLOCK"]:
    if score <= 0.30:
        return "PASS"
    if score <= 0.60:
        return "WARN"
    return "BLOCK"


def _decision(conflict) -> CanonGovernorDecision:
    score = canon_conflict_score(
        timeline_conflict=conflict.timeline_conflict,
        world_rule_conflict=conflict.world_rule_conflict,
        character_identity_conflict=conflict.character_identity_conflict,
        relationship_conflict=conflict.relationship_conflict,
    )
    status = canon_status(score)
    action = "allow" if status == "PASS" else "warn" if status == "WARN" else "block"
    return CanonGovernorDecision(
        conflict_id=conflict.conflict_id,
        score=score,
        status=status,
        action=action,
        auto_resolution_allowed=False,
        human_review_required=status in {"WARN", "BLOCK"},
    )


def run_cross_work_canon_governor() -> dict[str, Any]:
    conflicts = canon_conflict_fixtures()
    decisions = [_decision(conflict) for conflict in conflicts]
    blocked = [d for d in decisions if d.status == "BLOCK"]
    warned = [d for d in decisions if d.status == "WARN"]
    auto_resolutions = [d for d in decisions if d.auto_resolution_allowed]
    issues: list[str] = []
    if auto_resolutions:
        issues.append("canon_auto_resolution_enabled")
    if not blocked:
        issues.append("missing_block_fixture")
    return {
        "status": "pass" if not issues else "blocked",
        "title": "Cross-Work Canon Governor",
        "formula": "CanonConflictScore = timeline_conflict*0.35 + world_rule_conflict*0.30 + character_identity_conflict*0.20 + relationship_conflict*0.15",
        "thresholds": {"PASS": "score <= 0.30", "WARN": "0.30 < score <= 0.60", "BLOCK": "score > 0.60"},
        "conflicts_total": len(conflicts),
        "pass_count": len([d for d in decisions if d.status == "PASS"]),
        "warn_count": len(warned),
        "block_count": len(blocked),
        "canon_auto_resolution_count": len(auto_resolutions),
        "human_review_required_count": len([d for d in decisions if d.human_review_required]),
        "project_local_canon_preserved": True,
        "cross_work_canon_merge_allowed": False,
        "conflicts": [c.to_dict() for c in conflicts],
        "decisions": [d.to_dict() for d in decisions],
        "issues": issues,
    }
