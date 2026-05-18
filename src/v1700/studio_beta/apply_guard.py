from __future__ import annotations

from .contracts import RevisionApplyGuardResult
from .review_queue_panel import build_review_queue_panel
from .writer_decision import build_writer_decisions


def run_revision_apply_guard() -> dict:
    queue = build_review_queue_panel()
    decisions = build_writer_decisions()
    approved = set(decisions.get("approved_revision_ids", []))
    applied = [item for item in queue.get("items", []) if item["revision_id"] in approved]
    unauthorized = [item for item in queue.get("items", []) if item.get("writer_decision") == "APPLIED" and item["revision_id"] not in approved]
    blocked = [item for item in queue.get("items", []) if item.get("severity") == "BLOCK" and item["revision_id"] not in approved]
    issues = []
    if unauthorized:
        issues.append("unauthorized_revision_apply")
    if blocked:
        issues.append("unresolved_block_revision")
    result = RevisionApplyGuardResult(
        status="pass" if not issues else "blocked",
        applied_revision_count=len(applied),
        blocked_revision_count=len(blocked),
        writer_approval_required=True,
        unauthorized_apply_count=len(unauthorized),
        issues=tuple(issues),
    )
    payload = result.to_dict()
    payload["approved_revision_ids"] = sorted(approved)
    return payload
