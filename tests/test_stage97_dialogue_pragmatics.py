from v1700.longform_endurance.dialogue_pragmatics import evaluate_dialogue_pragmatics
from v1700.longform_endurance.episode_planner import build_endurance_episode_plan


def test_stage97_dialogue_pragmatics_has_no_speech_level_inconsistency():
    report = evaluate_dialogue_pragmatics(build_endurance_episode_plan(16))
    assert report["status"] == "pass"
    assert report["speech_level_inconsistency_count"] == 0
    assert report["explanatory_dialogue_ratio_max"] <= 0.2
