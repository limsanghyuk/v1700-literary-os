from __future__ import annotations

from .contracts import SceneBeat


def build_scene_beat_board() -> list[SceneBeat]:
    return [
        SceneBeat(
            beat_id="beat-001",
            scene_id="ep01-sc001",
            beat_function="visual_inciting_pressure",
            visible_action="The lead notices a missing ledger page before anyone speaks.",
            conflict_vector="truth_vs_institutional_silence",
            emotional_pressure_delta=0.18,
            reveal_state="SETUP",
            production_note="Hold on the empty page, then cut before explanation.",
            microplot_id="microplot-investigation-01",
            payoff_debt_id="payoff-ledger-page",
        ),
        SceneBeat(
            beat_id="beat-002",
            scene_id="ep01-sc002",
            beat_function="agency_choice_under_pressure",
            visible_action="The lead hides the page copy and chooses to question the nurse off record.",
            conflict_vector="public_role_vs_private_doubt",
            emotional_pressure_delta=0.22,
            reveal_state="DELAY",
            production_note="Action must carry the decision; avoid exposition.",
            microplot_id="microplot-investigation-01",
            payoff_debt_id="payoff-ledger-page",
        ),
        SceneBeat(
            beat_id="beat-003",
            scene_id="ep01-sc003",
            beat_function="prop_reveal_setup",
            visible_action="A cracked watch appears on the antagonist's desk.",
            conflict_vector="memory_object_vs_denial",
            emotional_pressure_delta=0.12,
            reveal_state="SETUP",
            production_note="Prop enters frame before dialogue names it.",
            microplot_id="microplot-antagonist-pressure-01",
            payoff_debt_id="payoff-cracked-watch",
        ),
    ]


def scene_beat_board_report(beats: list[SceneBeat]) -> dict:
    issues = []
    for beat in beats:
        if not beat.microplot_id or not beat.payoff_debt_id:
            issues.append(f"{beat.beat_id}:missing_microplot_or_payoff_anchor")
    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "scene_beat_count": len(beats),
        "beats": [beat.to_dict() for beat in beats],
    }

