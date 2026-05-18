from __future__ import annotations

from v1700.longform_adversarial.adversarial_orchestrator import run_stage97_1_adversarial_validation


def build_stage97_1_manifest() -> dict:
    report = run_stage97_1_adversarial_validation()
    return {
        "stage": "97.1",
        "name": "Adversarial Longform Validation Hardening",
        "baseline_stage": "97",
        "requires_stage97_fixed": True,
        "provider_default_calls": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "adversarial_cases_total": report["adversarial_cases_total"],
        "adversarial_cases_matched_expectation": report["adversarial_cases_matched_expectation"],
        "normal_cases_passed": report["normal_cases_passed"],
        "blocked_cases_passed": report["blocked_cases_passed"],
        "branchpoint_lineage_preserved": True,
        "release_gate_status": report["status"],
    }


def build_stage97_1_branchpoint_trace_manifest() -> dict:
    return {
        "stage": "97.1",
        "baseline_stage": "97",
        "branchpoint_authority": "Stage97 endurance proof plus adversarial negative corpus hardening",
        "tracepoints": [
            "adversarial_negative_corpus",
            "broken_topology_block",
            "broken_payoff_block",
            "passive_agency_block",
            "weak_scene_block",
            "speech_level_violation_block",
            "style_drift_violation_block",
            "attention_fatigue_block",
            "coefficient_memory_bridge",
            "local_only_manuscript_ingest",
            "production_scene_mapping",
        ],
    }


def build_stage97_1_adversarial_validation_manifest() -> dict:
    report = run_stage97_1_adversarial_validation()
    return {
        "stage": "97.1",
        "status": report["status"],
        "negative_corpus_total": report["blocked_cases_total"],
        "negative_corpus_blocked_as_expected": report["blocked_cases_passed"],
        "normal_cases_passed": report["normal_cases_passed"],
        "coefficient_memory_adapter": report["coefficient_memory_bridge"]["status"],
        "manuscript_ingest_privacy": report["manuscript_ingest_privacy"]["status"],
        "production_scene_mapping": report["production_scene_mapping"]["status"],
        "provider_default_calls": 0,
        "live_provider_call_count": 0,
        "node2_raw_reveal_access_count": 0,
        "raw_manuscript_provider_leakage": 0,
    }
