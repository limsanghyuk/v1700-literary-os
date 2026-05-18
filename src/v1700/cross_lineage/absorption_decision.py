from __future__ import annotations


def build_absorption_decisions(source_probe: dict | None = None) -> dict:
    source_probe = source_probe or {}
    source_status = source_probe.get("source_status", "MISSING")
    candidates = [
        {
            "candidate_id": "V430_SCENARIO_ROOM_PIPELINE",
            "source_status": source_status,
            "value_area": "SCENARIO_ROOM",
            "v1700_overlap": "Stage98 Studio Workflow + Stage100 Scenario Evaluation",
            "branchpoint_risk": "MEDIUM",
            "proposed_action": "ADAPT",
            "decision_reason": "Scenario-room orchestration is valuable, but must be recompiled as V1700 contracts before runtime promotion.",
            "required_branchpoints": ["BP_STAGE101_CROSS_LINEAGE_PREFLIGHT", "BP_STAGE101_SCENARIO_ROOM_CONTRACT"],
            "required_tests": ["tests/test_stage101_scenario_room_contract.py"],
        },
        {
            "candidate_id": "V430_INVESTIGATIVE_ACTION_BEATS",
            "source_status": source_status,
            "value_area": "INVESTIGATION_ACTION",
            "v1700_overlap": "Stage97 agency conservation + Stage100 scenario scoring",
            "branchpoint_risk": "LOW",
            "proposed_action": "ADAPT",
            "decision_reason": "Action movement can strengthen scenario mode if each beat remains tied to agency and scene necessity.",
            "required_branchpoints": ["BP_STAGE101_SCENARIO_CUE_INTEGRATION"],
            "required_tests": ["tests/test_stage101_investigation_action.py"],
        },
        {
            "candidate_id": "V430_DIALOGUE_SILENCE_CUE",
            "source_status": source_status,
            "value_area": "DIALOGUE_SILENCE",
            "v1700_overlap": "Stage97 dialogue pragmatics + Node2 surface-only boundary",
            "branchpoint_risk": "MEDIUM",
            "proposed_action": "ADAPT",
            "decision_reason": "Dialogue and silence cues are useful only if forbidden reveal and surface-only contracts remain explicit.",
            "required_branchpoints": ["BP_STAGE101_SCENARIO_CUE_INTEGRATION"],
            "required_tests": ["tests/test_stage101_dialogue_silence_cue.py"],
        },
        {
            "candidate_id": "V430_PROP_LED_REVEAL",
            "source_status": source_status,
            "value_area": "PROP_REVEAL",
            "v1700_overlap": "Stage86 EpisodeRevealBudget + Stage97 payoff debt",
            "branchpoint_risk": "MEDIUM",
            "proposed_action": "ADAPT",
            "decision_reason": "Prop reveals are allowed only when every cue is bound to a reveal-budget slot and payoff episode.",
            "required_branchpoints": ["BP_STAGE101_SCENARIO_CUE_INTEGRATION"],
            "required_tests": ["tests/test_stage101_prop_reveal.py"],
        },
        {
            "candidate_id": "V430_PRODUCT_PIPELINE_API",
            "source_status": source_status,
            "value_area": "PRODUCT_PIPELINE",
            "v1700_overlap": "Stage89-98 Studio and publishing package",
            "branchpoint_risk": "MEDIUM",
            "proposed_action": "DEFER",
            "decision_reason": "Product/API expansion belongs after scenario-room safety, most likely Stage103 deployment hardening.",
            "required_branchpoints": ["BP_STAGE101_CROSS_LINEAGE_PREFLIGHT"],
            "required_tests": ["tests/test_stage101_absorption_matrix.py"],
        },
    ]
    return {
        "status": "pass",
        "source_status": source_status,
        "absorption_mode": source_probe.get("absorption_mode", "fixture_contract_validation"),
        "v430_untraced_merge": False,
        "candidates": candidates,
        "allowed_actions": ["ADAPT", "DEFER"],
        "blocked_actions": ["UNTRACED_MERGE", "DIRECT_RUNTIME_IMPORT"],
    }

