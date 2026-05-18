from pathlib import Path

from v1700.stage100.v430_comparison_bridge import run_stage100_v430_comparison_bridge

ROOT = Path(__file__).resolve().parents[1]


def test_stage100_v430_bridge_is_comparison_only():
    report = run_stage100_v430_comparison_bridge(ROOT)
    assert report["status"] == "pass"
    assert report["immediate_absorption_allowed"] is False
    assert report["v430_code_merged"] is False
    assert report["next_absorption_stage"] == "Stage101"

