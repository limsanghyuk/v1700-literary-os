from pathlib import Path

from v1700.studio_workflow.episode_board import build_episode_board
from v1700.studio_workflow.microplot_matrix_editor import build_microplot_matrix_editor_report
from v1700.studio_workflow.project_ingest import ingest_studio_project

ROOT = Path(__file__).resolve().parents[1]


def test_stage98_microplot_matrix_preserves_branchpoints_without_raw_text():
    board = build_episode_board(ingest_studio_project(ROOT))
    report = build_microplot_matrix_editor_report(board)
    assert report["status"] == "pass"
    assert report["row_count"] == 24
    assert all(row["branchpoint_lineage_preserved"] for row in report["rows"])
    assert all(row["raw_text_cell"] is False for row in report["rows"])
