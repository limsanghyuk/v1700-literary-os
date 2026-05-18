from __future__ import annotations

from .contracts import PropRevealCue


def build_prop_reveal_cues() -> list[PropRevealCue]:
    return [
        PropRevealCue(
            cue_id="prop-001",
            prop_id="missing-ledger-page",
            first_appearance_scene="ep01-sc001",
            reveal_budget_slot="RB-EP01-SETUP-02",
            payoff_episode="ep04",
            status="SETUP",
        ),
        PropRevealCue(
            cue_id="prop-002",
            prop_id="cracked-watch",
            first_appearance_scene="ep01-sc003",
            reveal_budget_slot="RB-EP01-SETUP-04",
            payoff_episode="ep08",
            status="ACTIVE",
        ),
    ]


def prop_reveal_report(cues: list[PropRevealCue]) -> dict:
    issues = []
    for cue in cues:
        if not cue.reveal_budget_slot:
            issues.append(f"{cue.cue_id}:missing_reveal_budget_slot")
        if not cue.payoff_episode:
            issues.append(f"{cue.cue_id}:missing_payoff_episode")
    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "prop_reveal_cue_count": len(cues),
        "reveal_budget_safe": not issues,
        "cues": [cue.to_dict() for cue in cues],
    }

