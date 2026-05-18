from v1700.longform_endurance.episode_planner import build_endurance_episode_plan
from v1700.longform_endurance.voice_manifold import evaluate_voice_manifold


def test_stage97_voice_manifold_allows_evolution_without_blocked_drift():
    report = evaluate_voice_manifold(build_endurance_episode_plan(16))
    assert report["status"] == "pass"
    assert report["max_style_drift"] <= 0.18
    assert report["style_drift_summary"] == "permitted evolution only"
