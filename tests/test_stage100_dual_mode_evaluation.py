from pathlib import Path

from v1700.stage100.dual_mode_evaluator import run_stage100_dual_mode_evaluation

ROOT = Path(__file__).resolve().parents[1]


def test_stage100_dual_mode_evaluation_separates_prose_and_scenario():
    report = run_stage100_dual_mode_evaluation(ROOT)
    assert report["status"] == "pass"
    assert report["prose_evaluation_status"] == "pass"
    assert report["scenario_evaluation_status"] == "pass"
    assert report["evaluation_type"] == "fixture_contract_validation"
    assert report["actual_generation_benchmark"] is False
    assert report["prose_scenario_metric_conflation"] is False
    assert set(report["prose"]["score_breakdown"]) & set(report["scenario"]["score_breakdown"]) == set()
