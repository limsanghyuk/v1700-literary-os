from pathlib import Path

from v1700.studio_workflow.episode_board import build_episode_board
from v1700.studio_workflow.project_ingest import ingest_studio_project
from v1700.studio_workflow.publishing_package import build_publishing_package
from v1700.studio_workflow.review_package import build_review_package
from v1700.studio_workflow.revision_queue import build_revision_queue

ROOT = Path(__file__).resolve().parents[1]


def test_stage98_publishing_package_defaults_to_feature_only():
    project = ingest_studio_project(ROOT)
    board = build_episode_board(project)
    review = build_review_package(project.project_id, build_revision_queue(board))
    package = build_publishing_package(ROOT, project, review)
    assert package.includes_full_text is False
    assert package.includes_feature_reports is True
    assert package.includes_release_evidence is True
