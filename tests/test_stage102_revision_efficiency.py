from pathlib import Path

from v1700.stage102.orchestrator import run_stage102_3_revision_efficiency

ROOT = Path(__file__).resolve().parents[1]


def test_stage102_revision_efficiency_reduces_time_and_issues():
    report = run_stage102_3_revision_efficiency(ROOT)
    assert report["status"] == "pass"
    assert report["revision_time_reduction_ratio"] >= 0.30
    assert report["issue_reduction_ratio"] >= 0.50
    assert report["plot_consistency_status"] == "PASS"
    assert report["payoff_debt_status"] == "PASS"
    assert report["scene_necessity_status"] == "PASS"
