from v1700.studio_workflow.contracts import RevisionItem
from v1700.studio_workflow.revision_queue import writer_approval_guard


def test_stage98_writer_approval_guard_blocks_unapproved_applied_revision():
    item = RevisionItem(
        revision_id="rev-test",
        project_id="project",
        episode_id="ep-01",
        source_gate="stage97",
        severity="WARN",
        issue_type="test",
        diagnosis="test",
        recommended_action="test",
        writer_decision="PENDING",
        evidence_path="release/current/stage97_release_gate_report.json",
        applied=True,
    )
    assert writer_approval_guard([item])["status"] == "blocked"
