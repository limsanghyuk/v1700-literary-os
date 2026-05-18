from __future__ import annotations

from .contracts import InvestigationActionBeat


def build_investigation_action_beats() -> list[InvestigationActionBeat]:
    return [
        InvestigationActionBeat(
            beat_id="act-001",
            scene_id="ep01-sc001",
            actor_id="protagonist",
            action_goal="Confirm whether the ledger page was removed before the audit.",
            clue_or_obstacle="The timestamp stamp is missing from the scan.",
            agency_delta=0.16,
            scene_necessity_anchor="changes_information_and_goal",
        ),
        InvestigationActionBeat(
            beat_id="act-002",
            scene_id="ep01-sc002",
            actor_id="supporting_witness",
            action_goal="Signal fear without direct confession.",
            clue_or_obstacle="She leaves the room only after hearing the antagonist's name.",
            agency_delta=0.11,
            scene_necessity_anchor="changes_relationship_and_risk",
        ),
    ]


def investigation_action_report(beats: list[InvestigationActionBeat]) -> dict:
    issues = []
    for beat in beats:
        if beat.agency_delta <= 0:
            issues.append(f"{beat.beat_id}:non_positive_agency_delta")
        if not beat.scene_necessity_anchor:
            issues.append(f"{beat.beat_id}:missing_scene_necessity_anchor")
    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "action_movement_count": len(beats),
        "beats": [beat.to_dict() for beat in beats],
    }

