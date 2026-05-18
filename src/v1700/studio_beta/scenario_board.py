from __future__ import annotations

from .contracts import BoardReport


def build_scenario_board() -> dict:
    cards = (
        {"card_id": "scenario-001", "scene_id": "scene-001", "beat": "investigator_enters_closed_station", "action": "records_rain_mismatch", "production_note": "single_location"},
        {"card_id": "scenario-002", "scene_id": "scene-002", "beat": "prop_led_reveal", "prop": "dead_timetable_board", "cue": "date_appears"},
        {"card_id": "scenario-003", "scene_id": "scene-002", "beat": "silence_cue", "dialogue_function": "subtext_not_exposition", "cue": "unanswered_question"},
    )
    return BoardReport(status="pass", board_id="stage104-scenario-board", mode="SCENARIO", cards=cards).to_dict()
