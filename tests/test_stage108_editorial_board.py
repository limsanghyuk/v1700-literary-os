from pathlib import Path
from v1700.stage108.orchestrator import run_stage108
from v1700.gates.stage108_release_gate import run_stage108_release_gate

ROOT = Path(__file__).resolve().parents[1]

def test_stage108_editorial_board_runs():
    report = run_stage108(ROOT)
    assert report["status"] == "pass"
    board = report["stage108_1_editorial_board"]
    assert board["reviewer_count"] >= 6
    assert board["scorecard_count"] >= 24
    assert board["raw_manuscript_provider_leakage"] == 0

def test_stage108_release_gate_passes():
    result = run_stage108_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["live_provider_call_count_in_release_gate"] == 0
    assert result["raw_manuscript_provider_leakage"] == 0
