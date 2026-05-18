from __future__ import annotations

from .contracts import ScenarioRoomPlan


def build_scenario_room_plan(scene_beat_count: int, action_count: int, dialogue_count: int, prop_count: int, reveal_budget_safe: bool) -> ScenarioRoomPlan:
    return ScenarioRoomPlan(
        series_id="stage101-scenario-room-fixture",
        episode_id="ep01",
        mode="SCENARIO",
        scene_beat_count=scene_beat_count,
        action_movement_count=action_count,
        dialogue_silence_cue_count=dialogue_count,
        prop_reveal_cue_count=prop_count,
        reveal_budget_safe=reveal_budget_safe,
        node2_raw_reveal_access=0,
        provider_call_count=0,
    )

