from __future__ import annotations

from .contracts import DialogueSilenceCue


def build_dialogue_silence_cues() -> list[DialogueSilenceCue]:
    return [
        DialogueSilenceCue(
            cue_id="dlg-001",
            scene_id="ep01-sc002",
            speaker_id="supporting_witness",
            speech_level="formal_avoidant",
            silence_function="withhold_direct_accusation",
            subtext="She knows the missing page matters but fears naming the person who took it.",
            forbidden_reveal=["actual_thief_identity", "finale_payoff_detail"],
            node2_surface_only=True,
        ),
        DialogueSilenceCue(
            cue_id="dlg-002",
            scene_id="ep01-sc003",
            speaker_id="antagonist",
            speech_level="polite_control",
            silence_function="turn_question_into_debt",
            subtext="The antagonist answers with courtesy to regain hierarchy.",
            forbidden_reveal=["watch_owner_backstory"],
            node2_surface_only=True,
        ),
    ]


def dialogue_silence_report(cues: list[DialogueSilenceCue]) -> dict:
    issues = []
    for cue in cues:
        if not cue.node2_surface_only:
            issues.append(f"{cue.cue_id}:node2_surface_only_false")
        if not cue.forbidden_reveal:
            issues.append(f"{cue.cue_id}:missing_forbidden_reveal")
    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "dialogue_silence_cue_count": len(cues),
        "node2_raw_reveal_access": 0,
        "cues": [cue.to_dict() for cue in cues],
    }

