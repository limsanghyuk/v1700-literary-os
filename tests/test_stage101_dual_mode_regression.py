from pathlib import Path

from v1700.stage101.orchestrator import run_stage101_3_dual_mode_regression

ROOT = Path(__file__).resolve().parents[1]


def test_stage101_dual_mode_regression_keeps_prose_and_scenario_separate():
    report = run_stage101_3_dual_mode_regression(ROOT)
    assert report["status"] == "pass"
    assert report["checks"]["prose_scenario_metric_conflation_false"] is True
    assert report["checks"]["scenario_room_pass"] is True
    assert report["checks"]["provider_zero_pass"] is True

