from pathlib import Path
from v1700.stage104.orchestrator import run_stage104_2_unified_board
ROOT = Path(__file__).resolve().parents[1]

def test_unified_board_keeps_prose_scenario_distinct():
    report = run_stage104_2_unified_board(ROOT)
    assert report["status"] == "pass"
    assert report["checks"]["metric_conflation_prevented"] is True
