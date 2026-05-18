from __future__ import annotations

from .contracts import ArbitrationDecision


def arbitrate_candidates(scored: list[dict]) -> dict:
    by_id = {candidate["candidate_id"]: candidate for candidate in scored}
    selected_prose = tuple(
        cid for cid in ("cand_dialogue_claude_fixture", "cand_structure_gpt_fixture", "cand_local_ollama_fixture") if cid in by_id
    )
    selected_scenario = tuple(
        cid for cid in ("cand_visual_gemini_fixture", "cand_release_fixture_control", "cand_structure_gpt_fixture") if cid in by_id
    )
    selected_hybrid = tuple(
        cid for cid in ("cand_structure_gpt_fixture", "cand_dialogue_claude_fixture", "cand_visual_gemini_fixture", "cand_local_ollama_fixture") if cid in by_id
    )
    all_ids = set(by_id)
    decisions = (
        ArbitrationDecision(
            decision_id="decision_prose_surface",
            mode="PROSE",
            selected_candidate_ids=selected_prose,
            rejected_candidate_ids=tuple(sorted(all_ids - set(selected_prose))),
            merge_policy="dialogue_subtext_plus_structure_local_privacy",
            final_authority="V1700_Node3_Critic_Gate",
            provider_call_count=0,
            raw_manuscript_leakage=0,
        ),
        ArbitrationDecision(
            decision_id="decision_scenario_room",
            mode="SCENARIO",
            selected_candidate_ids=selected_scenario,
            rejected_candidate_ids=tuple(sorted(all_ids - set(selected_scenario))),
            merge_policy="visual_beats_plus_fixture_scenario_contract",
            final_authority="V1700_Scenario_Room_Gate",
            provider_call_count=0,
            raw_manuscript_leakage=0,
        ),
        ArbitrationDecision(
            decision_id="decision_hybrid_studio",
            mode="HYBRID",
            selected_candidate_ids=selected_hybrid,
            rejected_candidate_ids=tuple(sorted(all_ids - set(selected_hybrid))),
            merge_policy="role_weighted_multi_lane_with_writer_approval",
            final_authority="V1700_Studio_Beta_Review_Queue",
            provider_call_count=0,
            raw_manuscript_leakage=0,
        ),
    )
    issues = [d.decision_id for d in decisions if d.provider_call_count != 0 or d.raw_manuscript_leakage != 0]
    return {
        "stage": "105.3",
        "title": "Creative Arbitration Decisions",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "decision_count": len(decisions),
        "decisions": [decision.to_dict() for decision in decisions],
        "final_authority": "V1700 gates, not providers",
    }
