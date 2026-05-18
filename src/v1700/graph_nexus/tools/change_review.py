from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.tools.concept_impact import analyze_concept_impact


def build_change_review_packet(root: Path, change_intent: str, affected_paths: tuple[str, ...]) -> dict:
    impacts = [analyze_concept_impact(root, path) for path in affected_paths]
    high_risk = any(impact.get("risk") == "high" for impact in impacts)
    return {
        "status": "pass",
        "change_intent": change_intent,
        "affected_paths": list(affected_paths),
        "concept_impacts": impacts,
        "required_decision": "restore_or_review_first" if high_risk else "standard_review",
        "required_checks": [
            "pre_stage40_survival_gate",
            "release_gate",
            "pytest",
            "provider_default_calls_0",
            "node2_raw_reveal_access_0",
        ],
    }
