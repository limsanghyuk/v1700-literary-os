from v1700.longform_endurance.episode_planner import build_endurance_episode_plan
from v1700.longform_endurance.scene_necessity import evaluate_scene_necessity


def test_stage97_scene_necessity_keeps_weak_scene_ratio_below_floor():
    report = evaluate_scene_necessity(build_endurance_episode_plan(16))
    assert report["status"] == "pass"
    assert report["scene_count"] >= 160
    assert report["weak_scene_ratio"] <= 0.08
