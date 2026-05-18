from v1700.longform_endurance.attention_economy import evaluate_attention_economy
from v1700.longform_endurance.episode_planner import build_endurance_episode_plan


def test_stage97_attention_economy_stays_below_fatigue_threshold():
    report = evaluate_attention_economy(build_endurance_episode_plan(16))
    assert report["status"] == "pass"
    assert report["attention_fatigue_risk"] <= 0.45
