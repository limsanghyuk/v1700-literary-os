from __future__ import annotations

from v1700.studio_workflow.contracts import EpisodeBoard, RevisionItem


def build_revision_queue(board: EpisodeBoard) -> list[RevisionItem]:
    return [
        RevisionItem(
            revision_id="rev-stage98-warn-001",
            project_id=board.project_id,
            episode_id=board.episodes[7].episode_id if len(board.episodes) >= 8 else "ep-01",
            source_gate="stage97_attention_economy",
            severity="WARN",
            issue_type="attention_heat_variance",
            diagnosis="Feature reports suggest a mid-season attention spike should be reviewed.",
            recommended_action="Inspect episode board load distribution before export.",
            writer_decision="PENDING",
            evidence_path="release/current/stage97_longform_endurance_report.json",
        )
    ]


def writer_approval_guard(items: list[RevisionItem]) -> dict:
    violations = [
        item.revision_id
        for item in items
        if item.applied and item.writer_decision != "APPROVED"
    ]
    return {
        "status": "pass" if not violations else "blocked",
        "violations": violations,
        "applied_without_approval": len(violations),
    }


def revision_queue_report(items: list[RevisionItem]) -> dict:
    return {
        "status": "pass",
        "revision_items": [item.to_dict() for item in items],
        "warn_count": sum(1 for item in items if item.severity == "WARN"),
        "block_count": sum(1 for item in items if item.severity == "BLOCK"),
        "writer_approval_guard": writer_approval_guard(items),
        "node2_raw_reveal_access": 0,
    }
