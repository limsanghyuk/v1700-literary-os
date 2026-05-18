from v1700.scenario_room.scene_beat_board import build_scene_beat_board, scene_beat_board_report


def test_stage101_scene_beat_board_anchors_microplot_and_payoff():
    beats = build_scene_beat_board()
    report = scene_beat_board_report(beats)
    assert report["status"] == "pass"
    assert report["scene_beat_count"] >= 3
    assert all(beat.microplot_id and beat.payoff_debt_id for beat in beats)

