from v1700.studio_beta.scenario_board import build_scenario_board

def test_scenario_board_has_actionable_beats():
    board = build_scenario_board()
    assert board["status"] == "pass"
    assert board["mode"] == "SCENARIO"
    assert any("beat" in card for card in board["cards"])
