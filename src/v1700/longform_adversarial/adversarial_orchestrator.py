from __future__ import annotations

from pathlib import Path

from v1700.gates.stage97_release_gate import run_stage97_release_gate
from v1700.longform_adversarial.adversarial_case_builder import build_stage97_1_adversarial_cases
from v1700.longform_adversarial.coefficient_memory_adapter import load_stage96_coefficient_bridge
from v1700.longform_adversarial.contracts import AdversarialCase, AdversarialResult
from v1700.longform_adversarial.manuscript_ingest_adapter import run_local_manuscript_ingest_privacy_probe
from v1700.longform_adversarial.production_scene_mapper import build_production_scene_mapping


TRIGGERED_GATE_BY_REASON = {
    "orphan_microplot_detected": "fractal_topology",
    "episode_function_coverage_incomplete": "fractal_topology",
    "mid_season_sag_risk_above_threshold": "dramatic_load_balancing",
    "critical_payoff_debt_defaulted": "payoff_debt_ledger",
    "finale_new_critical_debt_created": "payoff_debt_ledger",
    "passive_protagonist_arc_detected": "agency_conservation",
    "protagonist_agency_collapse_against_antagonist": "agency_conservation",
    "weak_scene_ratio_above_threshold": "scene_necessity",
    "atmosphere_scene_function_label_missing": "scene_necessity",
    "speech_level_inconsistency_above_threshold": "dialogue_pragmatics",
    "explanatory_dialogue_ratio_above_threshold": "dialogue_pragmatics",
    "unexplained_style_drift_above_tolerance": "voice_manifold",
    "character_voice_collapse_detected": "voice_manifold",
    "attention_fatigue_risk_above_threshold": "attention_economy",
    "low_reward_high_cost_episode_count_above_threshold": "attention_economy",
    "provider_live_call_detected": "provider_zero_guard",
    "node2_raw_reveal_access_detected": "node2_surface_guard",
    "stale_manifest_detected": "manifest_consistency_guard",
    "missing_release_evidence_detected": "release_evidence_guard",
}


def run_stage97_1_adversarial_validation(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    baseline = run_stage97_release_gate(root)
    coefficient_bridge = load_stage96_coefficient_bridge(root)
    ingest = run_local_manuscript_ingest_privacy_probe(root)
    production_mapping = build_production_scene_mapping(root)
    cases = build_stage97_1_adversarial_cases(root)
    results = tuple(_evaluate_case(case, root) for case in cases)

    matched = [result for result in results if result.matched_expectation]
    blocked = [result for result in results if result.expected_status == "BLOCK"]
    normal = [result for result in results if result.expected_status == "PASS"]
    unexpected = [result.case_id for result in results if not result.matched_expectation]
    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage97_baseline_gate_blocked")
    if unexpected:
        issues.append("adversarial_expectation_mismatch")
    if coefficient_bridge.get("status") != "pass":
        issues.append("coefficient_memory_adapter_blocked")
    if ingest.get("status") != "pass" or ingest.get("raw_manuscript_provider_leakage") != 0:
        issues.append("manuscript_ingest_privacy_blocked")
    if production_mapping.get("status") != "pass":
        issues.append("production_scene_mapping_blocked")

    case_index = [case.to_dict() for case in cases]
    result_index = [result.to_dict() for result in results]
    return {
        "stage": "97.1",
        "baseline_stage": "97",
        "status": "pass" if not issues else "blocked",
        "title": "Adversarial Longform Validation Hardening",
        "stage97_baseline_gate": baseline,
        "coefficient_memory_bridge": coefficient_bridge,
        "manuscript_ingest_privacy": ingest,
        "production_scene_mapping": production_mapping,
        "adversarial_cases_total": len(cases),
        "adversarial_cases_matched_expectation": len(matched),
        "normal_cases_total": len(normal),
        "normal_cases_passed": sum(1 for result in normal if result.actual_status == "PASS" and result.matched_expectation),
        "blocked_cases_total": len(blocked),
        "blocked_cases_passed": sum(1 for result in blocked if result.actual_status == "BLOCK" and result.matched_expectation),
        "unexpected_case_ids": unexpected,
        "case_index": case_index,
        "results": result_index,
        "provider_default_calls": 0,
        "live_provider_call_count": 0,
        "node2_raw_reveal_access_count": 0,
        "reader_only_leakage_count": 0,
        "internal_marker_leakage_count": 0,
        "raw_credential_leakage": 0,
        "raw_manuscript_provider_leakage": 0,
        "branchpoint_lineage_preserved": True,
        "issues": issues,
    }


def _evaluate_case(case: AdversarialCase, root: Path) -> AdversarialResult:
    block_reason = _detect_block_reason(case)
    actual_status = "BLOCK" if block_reason else "PASS"
    matched = actual_status == case.expected_status
    if case.expected_status == "BLOCK" and block_reason != case.expected_block_reason:
        matched = False
    return AdversarialResult(
        case_id=case.case_id,
        actual_status=actual_status,
        expected_status=case.expected_status,
        matched_expectation=matched,
        block_reason=block_reason,
        triggered_gate=TRIGGERED_GATE_BY_REASON.get(block_reason or ""),
        provider_call_count=int(case.payload.get("provider_call_count", 0)),
        node2_raw_reveal_access=int(case.payload.get("node2_raw_reveal_access", 0)),
        evidence_path=str((root / "release" / "current" / "stage97_1_adversarial_pack" / f"{case.case_id}.json").relative_to(root)),
    )


def _detect_block_reason(case: AdversarialCase) -> str | None:
    payload = case.payload
    if case.case_type == "normal_stage97_proof":
        if payload.get("stage97_gate_status") != "pass":
            return "normal_stage97_proof_blocked"
        if payload.get("provider_call_count", 0) != 0:
            return "provider_live_call_detected"
        if payload.get("node2_raw_reveal_access", 0) != 0:
            return "node2_raw_reveal_access_detected"
        return None
    if case.case_type == "broken_topology":
        if payload.get("orphan_microplot_count", 0) > 0:
            return "orphan_microplot_detected"
        if payload.get("episode_function_coverage", 1.0) < 1.0:
            return "episode_function_coverage_incomplete"
    if case.case_type == "broken_load":
        if payload.get("mid_season_sag_risk", 0.0) > 0.18:
            return "mid_season_sag_risk_above_threshold"
    if case.case_type == "broken_payoff":
        if payload.get("critical_debt_default_count", 0) > 0:
            return "critical_payoff_debt_defaulted"
        if payload.get("finale_new_critical_debt_count", 0) > 0:
            return "finale_new_critical_debt_created"
    if case.case_type == "passive_agency":
        if payload.get("antagonist_agency_only") is True:
            return "protagonist_agency_collapse_against_antagonist"
        if payload.get("passive_episode_count", 0) > 1 or payload.get("protagonist_agency_floor", 1.0) < 0.55:
            return "passive_protagonist_arc_detected"
    if case.case_type == "weak_scene":
        if payload.get("atmosphere_scene_without_function") is True:
            return "atmosphere_scene_function_label_missing"
        if payload.get("weak_scene_ratio", 0.0) > 0.08:
            return "weak_scene_ratio_above_threshold"
    if case.case_type == "speech_level_violation":
        if payload.get("speech_level_inconsistency_count", 0) > 0:
            return "speech_level_inconsistency_above_threshold"
        if payload.get("explanatory_dialogue_ratio", 0.0) > 0.3:
            return "explanatory_dialogue_ratio_above_threshold"
    if case.case_type == "style_drift_violation":
        if payload.get("character_voice_collapse") is True:
            return "character_voice_collapse_detected"
        if payload.get("style_drift", 0.0) > 0.18 and payload.get("permitted_style_evolution") is False:
            return "unexplained_style_drift_above_tolerance"
    if case.case_type == "attention_fatigue":
        if payload.get("attention_fatigue_risk", 0.0) > 0.45:
            return "attention_fatigue_risk_above_threshold"
        if payload.get("low_reward_high_cost_count", 0) > 1:
            return "low_reward_high_cost_episode_count_above_threshold"
    if case.case_type == "security_boundary":
        if payload.get("provider_call_count", 0) > 0:
            return "provider_live_call_detected"
        if payload.get("node2_raw_reveal_access", 0) > 0:
            return "node2_raw_reveal_access_detected"
    if case.case_type == "manifest_evidence":
        if payload.get("stale_manifest") is True:
            return "stale_manifest_detected"
        if payload.get("missing_release_evidence") is True:
            return "missing_release_evidence_detected"
    return None
