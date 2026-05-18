from v1700.scenario_room.prop_reveal import build_prop_reveal_cues, prop_reveal_report


def test_stage101_prop_reveal_requires_budget_slot_and_payoff():
    cues = build_prop_reveal_cues()
    report = prop_reveal_report(cues)
    assert report["status"] == "pass"
    assert report["reveal_budget_safe"] is True
    assert all(cue.reveal_budget_slot and cue.payoff_episode for cue in cues)

