from __future__ import annotations

from pathlib import Path

from .dialogue_silence_cue import build_dialogue_silence_cues, dialogue_silence_report
from .investigation_action import build_investigation_action_beats, investigation_action_report
from .planner import build_scenario_room_plan
from .prop_reveal import build_prop_reveal_cues, prop_reveal_report
from .scenario_room_report import write_scenario_room_pack
from .scene_beat_board import build_scene_beat_board, scene_beat_board_report


def run_scenario_room_integration(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    scene_beats = build_scene_beat_board()
    action_beats = build_investigation_action_beats()
    dialogue_cues = build_dialogue_silence_cues()
    prop_cues = build_prop_reveal_cues()

    scene_report = scene_beat_board_report(scene_beats)
    action_report = investigation_action_report(action_beats)
    dialogue_report = dialogue_silence_report(dialogue_cues)
    prop_report = prop_reveal_report(prop_cues)
    plan = build_scenario_room_plan(
        scene_beat_count=scene_report["scene_beat_count"],
        action_count=action_report["action_movement_count"],
        dialogue_count=dialogue_report["dialogue_silence_cue_count"],
        prop_count=prop_report["prop_reveal_cue_count"],
        reveal_budget_safe=prop_report["reveal_budget_safe"],
    )
    issues = []
    for name, report in (
        ("scene_beat_board", scene_report),
        ("investigation_action", action_report),
        ("dialogue_silence", dialogue_report),
        ("prop_reveal", prop_report),
    ):
        if report.get("status") != "pass":
            issues.append(f"{name}_blocked")
    if plan.provider_call_count != 0:
        issues.append("provider_call_count_nonzero")
    if plan.node2_raw_reveal_access != 0:
        issues.append("node2_raw_reveal_access_nonzero")
    status = "pass" if not issues else "blocked"
    payload = {
        "stage": "101.1/101.2",
        "baseline_stage": "101.0",
        "title": "Scenario Room Contract and Cue Integration",
        "status": status,
        "issues": issues,
        "plan": plan.to_dict(),
        "scene_beat_board": scene_report,
        "investigation_action": action_report,
        "dialogue_silence": dialogue_report,
        "prop_reveal": prop_report,
        "scenario_room_contract_status": status,
        "scene_beat_board_status": scene_report["status"],
        "investigation_action_status": action_report["status"],
        "dialogue_silence_cue_status": dialogue_report["status"],
        "prop_reveal_cue_status": prop_report["status"],
        "provider_call_count": plan.provider_call_count,
        "live_provider_call_count": 0,
        "node2_raw_reveal_access": plan.node2_raw_reveal_access,
        "raw_manuscript_provider_leakage": 0,
        "reveal_budget_safe": plan.reveal_budget_safe,
    }
    write_scenario_room_pack(root, payload)
    return payload
