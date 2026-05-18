from __future__ import annotations

from .contracts import WriterDecision


def build_writer_decisions() -> dict:
    decisions = (
        WriterDecision("decision-001", "rev-001", "APPROVED", "writer accepts prop-led revision", True),
        WriterDecision("decision-002", "rev-002", "DEFERRED", "orientation note deferred to next pass", False),
    )
    return {
        "status": "pass",
        "decisions": [decision.to_dict() for decision in decisions],
        "approved_revision_ids": [d.revision_id for d in decisions if d.approved_by_writer],
    }
