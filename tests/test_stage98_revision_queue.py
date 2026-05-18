from pathlib import Path

from v1700.studio_workflow.episode_board import build_episode_board
from v1700.studio_workflow.project_ingest import ingest_studio_project
from v1700.studio_workflow.revision_queue import build_revision_queue, revision_queue_report, writer_approval_guard

ROOT = Path(__file__).resolve().parents[1]


def test_stage98_revision_queue_contains_warn_and_guard_passes():
    board = build_episode_board(ingest_studio_project(ROOT))
    items = build_revision_queue(board)
    report = revision_queue_report(items)
    assert report["warn_count"] >= 1
    assert report["block_count"] == 0
    assert writer_approval_guard(items)["status"] == "pass"
    assert report["node2_raw_reveal_access"] == 0
