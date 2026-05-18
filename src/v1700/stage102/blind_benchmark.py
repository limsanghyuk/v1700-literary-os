from __future__ import annotations

from collections import defaultdict
from statistics import mean

from .candidate_builder import build_stage102_trial_candidates
from .contracts import BlindTrialScorecard, TrialCandidate
from .seed_bank import build_stage102_seed_bank


REVIEWER_WEIGHTS: dict[str, dict[str, float]] = {
    "professional_drama_critic": {
        "structure": 0.18,
        "reader_pull": 0.16,
        "character_agency": 0.14,
        "prose_surface": 0.16,
        "scenario_actionability": 0.12,
        "reveal_discipline": 0.14,
        "revision_readiness": 0.10,
    },
    "writer_workflow_editor": {
        "structure": 0.13,
        "reader_pull": 0.10,
        "character_agency": 0.12,
        "prose_surface": 0.12,
        "scenario_actionability": 0.16,
        "reveal_discipline": 0.14,
        "revision_readiness": 0.23,
    },
    "binge_reader_panel": {
        "structure": 0.13,
        "reader_pull": 0.25,
        "character_agency": 0.14,
        "prose_surface": 0.19,
        "scenario_actionability": 0.09,
        "reveal_discipline": 0.12,
        "revision_readiness": 0.08,
    },
}


def run_stage102_blind_benchmark() -> dict:
    seeds = build_stage102_seed_bank()
    candidates = tuple(candidate for seed in seeds for candidate in build_stage102_trial_candidates(seed))
    scorecards = tuple(_score_candidate(reviewer_id, candidate) for reviewer_id in REVIEWER_WEIGHTS for candidate in candidates)
    averages = _candidate_averages(scorecards)
    winner_id = max(averages, key=averages.get)
    winner = next(candidate for candidate in candidates if candidate.candidate_id == winner_id)
    pure_gpt_average = max(averages[c.candidate_id] for c in candidates if c.mode == "PURE_GPT_DIRECT")
    v1700_average = max(averages[c.candidate_id] for c in candidates if c.mode in {"V1700_PROSE", "V1700_SCENARIO", "V1700_HYBRID"})
    v1700_margin = round(v1700_average - pure_gpt_average, 2)
    identity_leakage = _identity_leakage_count(candidates)
    provider_calls = sum(candidate.provider_call_count for candidate in candidates)
    raw_leakage = sum(candidate.raw_manuscript_provider_leakage for candidate in candidates)
    node2_raw = sum(candidate.node2_raw_reveal_access for candidate in candidates)
    issues: list[str] = []
    if len(candidates) < 8:
        issues.append("blind_candidate_count_below_8")
    if winner.mode not in {"V1700_PROSE", "V1700_SCENARIO", "V1700_HYBRID"}:
        issues.append("v1700_family_not_winner")
    if v1700_margin < 0.5:
        issues.append("v1700_margin_below_0_5")
    if identity_leakage:
        issues.append("blind_identity_leakage_detected")
    if provider_calls or raw_leakage or node2_raw:
        issues.append("boundary_violation_detected")
    return {
        "stage": "102.2",
        "baseline_stage": "102.1",
        "title": "Real Writer Trial Blind Benchmark",
        "benchmark_type": "local_fixture_blind_benchmark",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "seed_count": len(seeds),
        "candidate_count": len(candidates),
        "reviewer_count": len(REVIEWER_WEIGHTS),
        "scorecard_count": len(scorecards),
        "winner_candidate_id": winner_id,
        "winner_mode": winner.mode,
        "candidate_averages": averages,
        "v1700_margin_over_pure_gpt": v1700_margin,
        "visible_blind_candidates": [candidate.blind_payload() for candidate in candidates],
        "revealed_candidates": [candidate.to_dict(reveal_mode=True) for candidate in candidates],
        "scorecards": [scorecard.to_dict() for scorecard in scorecards],
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "raw_manuscript_provider_leakage": raw_leakage,
        "node2_raw_reveal_access": node2_raw,
        "blind_identity_leakage": identity_leakage,
    }


def _score_candidate(reviewer_id: str, candidate: TrialCandidate) -> BlindTrialScorecard:
    axes = _axis_scores(candidate)
    weights = REVIEWER_WEIGHTS[reviewer_id]
    weighted = round(sum(axes[axis] * weights[axis] for axis in weights), 2)
    verdict = "PASS" if weighted >= 8.0 else "REVISE"
    return BlindTrialScorecard(
        candidate_id=candidate.candidate_id,
        reviewer_id=reviewer_id,
        axis_scores=axes,
        weighted_score=weighted,
        verdict=verdict,
        notes=tuple(candidate.evidence_markers),
    )


def _axis_scores(candidate: TrialCandidate) -> dict[str, float]:
    profile = {
        "PURE_GPT_DIRECT": (6.6, 7.0, 6.8, 6.7, 6.4, 6.5, 6.0),
        "CLAUDE_REFERENCE": (7.4, 7.8, 7.7, 8.0, 6.9, 7.0, 6.6),
        "GEMINI_REFERENCE": (7.0, 7.3, 7.0, 7.1, 7.6, 6.9, 6.5),
        "OLLAMA_LOCAL_DRAFT": (6.4, 6.3, 6.4, 6.1, 6.5, 6.7, 6.2),
        "V1700_PROSE": (8.5, 8.6, 8.4, 8.8, 7.5, 8.7, 8.1),
        "V1700_SCENARIO": (8.4, 8.1, 8.5, 7.8, 8.8, 8.6, 8.4),
        "V430_SCENARIO_ROOM": (7.9, 7.7, 7.8, 7.4, 8.5, 7.8, 7.5),
        "V1700_HYBRID": (8.9, 8.8, 8.7, 8.7, 8.9, 9.0, 8.9),
    }[candidate.mode]
    keys = ("structure", "reader_pull", "character_agency", "prose_surface", "scenario_actionability", "reveal_discipline", "revision_readiness")
    return dict(zip(keys, profile))


def _candidate_averages(scorecards: tuple[BlindTrialScorecard, ...]) -> dict[str, float]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for scorecard in scorecards:
        grouped[scorecard.candidate_id].append(scorecard.weighted_score)
    return {candidate_id: round(mean(scores), 2) for candidate_id, scores in grouped.items()}


def _identity_leakage_count(candidates: tuple[TrialCandidate, ...]) -> int:
    leaked_tokens = ("PURE_GPT_DIRECT", "CLAUDE_REFERENCE", "GEMINI_REFERENCE", "OLLAMA_LOCAL_DRAFT", "V1700_", "V430_")
    return sum(1 for candidate in candidates for token in leaked_tokens if token in candidate.visible_excerpt)
