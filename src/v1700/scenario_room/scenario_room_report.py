from __future__ import annotations

from pathlib import Path

from v1700.stage100.report import write_json, write_summary


def write_scenario_room_pack(root: Path, report: dict) -> None:
    pack = root / "release" / "current" / "stage101_scenario_room_pack"
    pack.mkdir(parents=True, exist_ok=True)
    write_json(pack / "scenario_room_plan.json", {"status": report["status"], "plan": report["plan"]})
    write_json(pack / "scene_beat_board.json", report["scene_beat_board"])
    write_json(pack / "investigation_action_beats.json", report["investigation_action"])
    write_json(pack / "dialogue_silence_cues.json", report["dialogue_silence"])
    write_json(pack / "prop_reveal_cues.json", report["prop_reveal"])
    write_summary(
        pack / "scenario_room_summary.md",
        "Stage101 Scenario Room Summary",
        [
            f"scenario room status: {report['status']}",
            f"scene beats: {report['plan']['scene_beat_count']}",
            f"provider calls: {report['provider_call_count']}",
            f"Node2 raw reveal access: {report['node2_raw_reveal_access']}",
        ],
    )

