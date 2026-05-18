from v1700.longform_production.production_calendar import build_production_calendar


def test_stage107_production_calendar_32_episode_target():
    report = build_production_calendar()
    assert report["status"] == "pass"
    assert report["episode_count"] == 32
    assert report["scene_target_total"] == 320
