from __future__ import annotations

from pathlib import Path

from v1700.provider_ensemble.candidate_normalizer import normalize_candidates
from v1700.provider_ensemble.candidate_pool import build_fixture_candidate_pool
from v1700.provider_ensemble.contracts import ArbitrationDecision, ProviderCandidate
from v1700.provider_ensemble.merge_policy import build_directive_level_merge
from v1700.provider_ensemble.narrative_physics_scorer import score_candidate
from v1700.provider_ensemble.rejection_policy import rejection_reasons
from v1700.provider_evaluation.harness import run_stage94_provider_evaluation_smoke


def run_provider_ensemble_arbitration(
    root: Path | None = None,
    stage95_report: dict | None = None,
    optimization: dict | None = None,
) -> dict:
    provider_eval = run_stage94_provider_evaluation_smoke()
    candidates = normalize_candidates(build_fixture_candidate_pool(tuple(provider_eval["provider_profiles"])))
    stage95_report = stage95_report or {}
    optimization = optimization or {}
    scored = [(candidate, score_candidate(candidate, stage95_report, optimization)) for candidate in candidates]
    decisions = _decide(scored)
    selected = tuple(candidate for candidate, score in scored if any(d.candidate_id == candidate.candidate_id and d.decision == "SELECT" for d in decisions))
    if len(selected) >= 2:
        directive = build_directive_level_merge(selected[:2])
        decisions.append(
            ArbitrationDecision(
                candidate_id="stage96-directive-merge",
                provider_id="v1700-local-arbiter",
                decision="MERGE",
                arbitration_score=round(sum(d.arbitration_score for d in decisions if d.decision == "SELECT") / len(selected), 3),
                reasons=("directive_level_merge_only", "text_concatenation_forbidden"),
                directive=directive,
            )
        )
    issues = []
    if not any(decision.decision in {"SELECT", "MERGE"} for decision in decisions):
        issues.append("missing_select_or_merge_decision")
    if not any(decision.decision == "REJECT" for decision in decisions):
        issues.append("missing_reject_decision")
    return {
        "stage": "96C",
        "status": "pass" if not issues else "blocked",
        "mode": "dry_run_fixture_candidates",
        "provider_count": 4,
        "candidate_count": len(candidates),
        "candidates": [candidate.to_dict() for candidate in candidates],
        "scores": [score for _, score in scored],
        "decisions": [decision.to_dict() for decision in decisions],
        "live_provider_call_count": 0,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
        "issues": issues,
    }


def _decide(scored: list[tuple[ProviderCandidate, dict]]) -> list[ArbitrationDecision]:
    decisions: list[ArbitrationDecision] = []
    clean = []
    for candidate, score in scored:
        reasons = rejection_reasons(candidate, score)
        if reasons:
            decisions.append(
                ArbitrationDecision(
                    candidate_id=candidate.candidate_id,
                    provider_id=candidate.provider_id,
                    decision="REJECT",
                    arbitration_score=score["arbitration_score"],
                    reasons=reasons,
                    directive="Reject provider candidate before merge or surface rendering.",
                )
            )
        else:
            clean.append((candidate, score))
    for candidate, score in sorted(clean, key=lambda item: item[1]["arbitration_score"], reverse=True)[:2]:
        decisions.append(
            ArbitrationDecision(
                candidate_id=candidate.candidate_id,
                provider_id=candidate.provider_id,
                decision="SELECT",
                arbitration_score=score["arbitration_score"],
                reasons=("narrative_physics_guard_pass", "branchpoint_guard_pass", "surface_guard_pass"),
                directive="Use as a source for V1700-local refinement directive, not as final authority.",
            )
        )
    return decisions
