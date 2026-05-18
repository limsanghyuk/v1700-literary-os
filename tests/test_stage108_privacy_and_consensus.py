from pathlib import Path
from v1700.editorial_board.board_orchestrator import run_editorial_board

ROOT = Path(__file__).resolve().parents[1]

def test_stage108_consensus_has_no_blockers():
    board = run_editorial_board(ROOT)
    assert board["editorial_consensus"]["blocker_count"] == 0
    assert board["average_score"] >= 8.0

def test_stage108_privacy_pack_is_feature_only():
    board = run_editorial_board(ROOT)
    assert board["raw_manuscript_provider_leakage"] == 0
    assert board["credential_leakage"] == 0
    assert board["raw_response_stored"] is False
