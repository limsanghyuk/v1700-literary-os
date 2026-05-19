from __future__ import annotations

from typing import Any

from .contracts import Gate26AdvisoryCase


def build_gate26_advisory_cases() -> dict[str, Any]:
    cases = (
        Gate26AdvisoryCase(
            case_id="GIG-TRUE-001",
            conflict_type="true_contradiction",
            description="Two works assert mutually exclusive canon facts without an in-story explanation.",
            advisory_level="REVIEW_REQUIRED",
            recommendation="route_to_writer_review_queue",
            requires_writer_approval=True,
        ),
        Gate26AdvisoryCase(
            case_id="GIG-MYST-001",
            conflict_type="intentional_mystery",
            description="The conflict is deliberately withheld and protected by reveal budget.",
            advisory_level="ALLOW_WITH_LOCK",
            recommendation="preserve_mystery_and_attach_reveal_lock",
            requires_writer_approval=False,
        ),
        Gate26AdvisoryCase(
            case_id="GIG-MIS-001",
            conflict_type="character_misunderstanding",
            description="The inconsistency belongs to a character POV gap, not the canonical trunk.",
            advisory_level="ALLOW_WITH_POV_TAG",
            recommendation="tag_character_knowledge_boundary",
            requires_writer_approval=False,
        ),
        Gate26AdvisoryCase(
            case_id="GIG-DELAY-001",
            conflict_type="reveal_delay",
            description="The truth exists in canon but is intentionally delayed for longform pacing.",
            advisory_level="ALLOW_WITH_REVEAL_BUDGET",
            recommendation="track_in_episode_reveal_budget",
            requires_writer_approval=False,
        ),
    )
    issues: list[str] = []
    if any(case.hard_block_allowed for case in cases):
        issues.append("hard_block_enabled_in_advisory_mode")
    if any(case.canon_auto_resolution_allowed for case in cases):
        issues.append("canon_auto_resolution_enabled")
    if not any(case.conflict_type == "true_contradiction" and case.requires_writer_approval for case in cases):
        issues.append("true_contradiction_writer_review_missing")
    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "cases": [case.to_dict() for case in cases],
        "case_count": len(cases),
        "hard_block_count": sum(1 for case in cases if case.hard_block_allowed),
        "canon_auto_resolution_count": sum(1 for case in cases if case.canon_auto_resolution_allowed),
        "writer_review_required_count": sum(1 for case in cases if case.requires_writer_approval),
    }
