from __future__ import annotations

from .contracts import CreativeCandidate
from .role_matrix import build_provider_role_matrix


def build_candidate_lanes() -> dict:
    matrix = build_provider_role_matrix()
    candidates = (
        CreativeCandidate(
            candidate_id="cand_structure_gpt_fixture",
            provider_id="gpt_reasoning_lane",
            task="STRUCTURE",
            mode="HYBRID",
            payload_kind="fixture_summary",
            score=8.7,
            rationale="Strong outline synthesis without live provider call.",
        ),
        CreativeCandidate(
            candidate_id="cand_dialogue_claude_fixture",
            provider_id="claude_long_context_lane",
            task="DIALOGUE",
            mode="PROSE",
            payload_kind="feature_only",
            score=8.9,
            rationale="Subtext and silence cue handling from feature-only context.",
        ),
        CreativeCandidate(
            candidate_id="cand_visual_gemini_fixture",
            provider_id="gemini_visual_lane",
            task="VISUAL",
            mode="SCENARIO",
            payload_kind="feature_only",
            score=8.8,
            rationale="Visual beat and production-space planning.",
        ),
        CreativeCandidate(
            candidate_id="cand_local_ollama_fixture",
            provider_id="ollama_local_privacy_lane",
            task="LOCAL_PRIVACY",
            mode="HYBRID",
            payload_kind="fixture_summary",
            score=8.4,
            rationale="Local-first privacy-preserving draft lane.",
        ),
        CreativeCandidate(
            candidate_id="cand_release_fixture_control",
            provider_id="fixture_release_lane",
            task="SCENARIO_BEAT",
            mode="SCENARIO",
            payload_kind="fixture_summary",
            score=8.6,
            rationale="Deterministic release baseline for scenario beat contracts.",
        ),
    )
    issues = [c.candidate_id for c in candidates if c.contains_raw_manuscript or c.live_call_count != 0]
    return {
        "stage": "105.2",
        "title": "Provider Candidate Lanes",
        "status": "pass" if matrix.get("status") == "pass" and not issues else "blocked",
        "issues": issues,
        "candidate_count": len(candidates),
        "candidates": [candidate.to_dict() for candidate in candidates],
        "payload_policy": "feature_only_or_fixture_summary",
        "live_provider_call_count_in_release": 0,
        "raw_manuscript_provider_leakage": 0,
    }
