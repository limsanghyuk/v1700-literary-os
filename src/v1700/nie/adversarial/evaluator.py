from __future__ import annotations

from pathlib import Path
from typing import Iterable

from v1700.nie.adversarial.contracts import NIEAdversarialCase, NIEAdversarialResult

REQUIRED_DIMS = {"tension", "sympathy", "dread", "catharsis"}
EXPECTED_BOOSTS = {"CHARACTER_NAMES": 1.5, "EPISODE_TERMS": 1.3, "DRAMA_KEYWORDS": 1.2}


def evaluate_cases(cases: Iterable[NIEAdversarialCase], evidence_dir: Path | None = None) -> tuple[NIEAdversarialResult, ...]:
    return tuple(evaluate_case(case, evidence_dir=evidence_dir) for case in cases)


def evaluate_case(case: NIEAdversarialCase, evidence_dir: Path | None = None) -> NIEAdversarialResult:
    actual_status, reason, gate = _detect(case)
    matched = actual_status == case.expected_status and (case.expected_status == "PASS" or reason == case.expected_block_reason)
    evidence_path = ""
    if evidence_dir is not None:
        evidence_path = (evidence_dir / f"{case.case_id}.json").as_posix()
    return NIEAdversarialResult(
        case_id=case.case_id,
        case_type=case.case_type,
        mutation_type=case.mutation_type,
        expected_status=case.expected_status,
        actual_status=actual_status,
        matched_expectation=matched,
        block_reason=reason,
        triggered_gate=gate,
        severity=case.severity,
        evidence_path=evidence_path,
        provider_call_count=int(case.payload.get("provider_call_count", 0) or 0),
        physics_reward_bridge_llm_call_count=int(case.payload.get("physics_reward_bridge_llm_call_count", 0) or 0),
        mae_live_provider_call_count=int(case.payload.get("mae_live_provider_call_count", 0) or 0),
        query_classifier_llm_call_count=int(case.payload.get("query_classifier_llm_call_count", 0) or 0),
        node2_raw_reveal_access=int(case.payload.get("node2_raw_reveal_access", 0) or 0),
        raw_manuscript_provider_leakage=int(case.payload.get("raw_manuscript_provider_leakage", 0) or 0),
        credential_leakage=int(case.payload.get("credential_leakage", 0) or 0),
    )


def _detect(case: NIEAdversarialCase) -> tuple[str, str | None, str | None]:
    p = case.payload
    if case.expected_status == "PASS":
        nil = p.get("nil_report", {})
        if nil.get("status") == "pass" and nil.get("convergence", {}).get("loop_closure_status") == "pass":
            return "PASS", None, None
        return "BLOCK", "normal_nil_loop_failed", "normal_nil_loop_gate"

    if case.mutation_type == "remove_dimension_score":
        dims = set((p.get("dimension_scores") or {}).keys())
        if not REQUIRED_DIMS.issubset(dims):
            return "BLOCK", "mae_dimension_score_missing", "mae_reward_contract_gate"
    if case.mutation_type == "bridge_attempts_live_provider_call":
        if int(p.get("physics_reward_bridge_llm_call_count", 0) or 0) > 0:
            return "BLOCK", "physics_reward_bridge_llm_call_nonzero", "physics_reward_bridge_no_llm_gate"
    if case.mutation_type == "alpha_exceeds_bounds":
        values = (p.get("alpha_after") or {}).values()
        if any(float(v) < 0.30 or float(v) > 0.80 for v in values):
            return "BLOCK", "amw_alpha_bounds_violation", "amw_alpha_bounds_gate"
    if case.mutation_type == "run_shift_exceeds_limit":
        if float(p.get("run_total_shift", 0.0) or 0.0) > float(p.get("limit", 0.10) or 0.10):
            return "BLOCK", "amw_run_total_shift_exceeded", "amw_drift_guard_gate"
    if case.mutation_type == "matrix_symmetric_only":
        if p.get("matrix_is_asymmetric") is False or int(p.get("asymmetric_pair_count", 0) or 0) <= 0:
            return "BLOCK", "cim_asymmetry_missing", "cim_asymmetric_matrix_gate"
    if case.mutation_type == "triangle_tension_not_computed":
        if int(p.get("triangle_count", 0) or 0) <= 0:
            return "BLOCK", "triangle_tension_missing", "structural_balance_gate"
    if case.mutation_type == "orphan_character_role_tier":
        chars = set(p.get("characters") or [])
        roles = set((p.get("role_tiers") or {}).keys())
        if chars - roles:
            return "BLOCK", "role_tier_orphan_character", "role_tier_assignment_gate"
    if case.mutation_type == "query_classifier_uses_llm":
        if int(p.get("query_classifier_llm_call_count", 0) or 0) > 0:
            return "BLOCK", "query_classifier_llm_call_nonzero", "domain_rag_classifier_no_llm_gate"
    if case.mutation_type == "drama_lexicon_boost_missing":
        boosts = p.get("boosts") or {}
        if any(float(boosts.get(name, 0.0) or 0.0) < expected for name, expected in EXPECTED_BOOSTS.items()):
            return "BLOCK", "drama_lexicon_boost_missing", "drama_lexicon_boost_gate"
    if case.mutation_type == "tension_curve_loss_absent":
        if p.get("tension_loss") is None or p.get("final_loss") is None:
            return "BLOCK", "narrative_tension_loss_missing", "narrative_tension_curve_gate"
    if case.mutation_type == "nil_report_lacks_evidence":
        if not str(p.get("evidence_path") or "").strip():
            return "BLOCK", "nil_evidence_path_missing", "nil_evidence_reproducibility_gate"
    if case.mutation_type == "broken_nie_case_not_detected_by_gate":
        if p.get("simulated_gate_detected") is False or int(p.get("unexpected_pass_count", 0) or 0) > 0:
            return "BLOCK", "gate_detection_failed", "gate25_detection_gate"
    return "PASS", None, None
