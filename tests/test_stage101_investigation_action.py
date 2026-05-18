from v1700.scenario_room.investigation_action import build_investigation_action_beats, investigation_action_report


def test_stage101_investigation_action_preserves_agency_and_scene_necessity():
    beats = build_investigation_action_beats()
    report = investigation_action_report(beats)
    assert report["status"] == "pass"
    assert report["action_movement_count"] >= 2
    assert all(beat.agency_delta > 0 for beat in beats)
    assert all(beat.scene_necessity_anchor for beat in beats)

