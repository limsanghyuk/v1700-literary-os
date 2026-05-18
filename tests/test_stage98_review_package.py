from pathlib import Path

from v1700.studio_workflow.episode_board import build_episode_board
from v1700.studio_workflow.project_ingest import ingest_studio_project
from v1700.studio_workflow.review_package import build_review_package, review_package_report
from v1700.studio_workflow.revision_queue import build_revision_queue

ROOT = Path(__file__).resolve().parents[1]


def test_stage98_review_package_is_publishable_without_unresolved_blocks():
    board = build_episode_board(ingest_studio_project(ROOT))
    package = build_review_package(board.project_id, build_revision_queue(board))
    report = review_package_report(package)
    assert package.unresolved_block_count == 0
    assert package.warn_count >= 1
    assert report["status"] == "pass"
    assert report["stage97_1_adversarial_block_evidence_preserved"] is True
