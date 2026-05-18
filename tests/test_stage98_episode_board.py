from pathlib import Path

from v1700.studio_workflow.episode_board import build_episode_board, episode_board_report
from v1700.studio_workflow.project_ingest import ingest_studio_project

ROOT = Path(__file__).resolve().parents[1]


def test_stage98_episode_board_has_24_ready_cards():
    board = build_episode_board(ingest_studio_project(ROOT))
    report = episode_board_report(board)
    assert board.board_status == "READY"
    assert report["status"] == "pass"
    assert report["episode_count"] == 24
    assert report["production_scene_count_estimate"] >= 160
