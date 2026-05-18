from v1700.longform_endurance.episode_planner import build_endurance_episode_plan
from v1700.longform_endurance.load_balancing import evaluate_dramatic_load


def test_stage97_dramatic_load_balancing_detects_no_blocking_sag():
    report = evaluate_dramatic_load(build_endurance_episode_plan(16))
    assert report["status"] == "pass"
    assert report["mid_season_sag_risk"] <= 0.18
    assert len(report["load_curve"]) == 16
