from v1700.scenario_room.dialogue_silence_cue import build_dialogue_silence_cues, dialogue_silence_report


def test_stage101_dialogue_silence_cues_remain_surface_only():
    cues = build_dialogue_silence_cues()
    report = dialogue_silence_report(cues)
    assert report["status"] == "pass"
    assert report["node2_raw_reveal_access"] == 0
    assert all(cue.node2_surface_only for cue in cues)
    assert all(cue.forbidden_reveal for cue in cues)

