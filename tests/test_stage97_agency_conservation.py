from v1700.longform_endurance.agency_conservation import evaluate_agency_conservation
from v1700.longform_endurance.episode_planner import build_endurance_episode_plan


def test_stage97_agency_conservation_preserves_protagonist_floor():
    report = evaluate_agency_conservation(build_endurance_episode_plan(16))
    assert report["status"] == "pass"
    assert report["agency_floor_status"] == "pass"
    assert report["protagonist_agency_floor"] >= 0.55
