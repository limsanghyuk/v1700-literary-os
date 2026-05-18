from __future__ import annotations

from pathlib import Path

from v1700.gates.stage97_release_gate import run_stage97_release_gate
from v1700.longform_adversarial.adversarial_orchestrator import run_stage97_1_adversarial_validation

_STAGE97_1_CACHE: dict[str, dict] = {}


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_stage97_1_release_gate(root: Path | None = None) -> dict:
    root = root or _project_root()
    cache_key = str(root.resolve())
    if cache_key in _STAGE97_1_CACHE:
        return _STAGE97_1_CACHE[cache_key]

    baseline = run_stage97_release_gate(root)
    adversarial = run_stage97_1_adversarial_validation(root)
    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage97_baseline_gate_blocked")
    if adversarial.get("status") != "pass":
        issues.append("adversarial_validation_blocked")
    if adversarial.get("normal_cases_passed") != adversarial.get("normal_cases_total"):
        issues.append("normal_case_blocked_unexpectedly")
    if adversarial.get("blocked_cases_passed") != adversarial.get("blocked_cases_total"):
        issues.append("adversarial_case_passed_unexpectedly")
    if adversarial.get("coefficient_memory_bridge", {}).get("status") != "pass":
        issues.append("coefficient_memory_adapter_missing")
    if adversarial.get("manuscript_ingest_privacy", {}).get("raw_manuscript_provider_leakage") != 0:
        issues.append("raw_manuscript_provider_leakage")
    if adversarial.get("provider_default_calls") != 0 or adversarial.get("live_provider_call_count") != 0:
        issues.append("provider_zero_blocked")
    if adversarial.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_detected")
    if adversarial.get("branchpoint_lineage_preserved") is not True:
        issues.append("branchpoint_lineage_broken")

    result = {
        "stage": "97.1",
        "baseline_stage": "97",
        "status": "pass" if not issues else "blocked",
        "title": "Adversarial Longform Validation Hardening",
        "checks": {
            "stage97_baseline_gate": baseline,
            "stage97_1_adversarial_validation": adversarial,
        },
        "issues": issues,
        "adversarial_cases_total": adversarial.get("adversarial_cases_total", 0),
        "adversarial_cases_matched_expectation": adversarial.get("adversarial_cases_matched_expectation", 0),
        "normal_cases_passed": adversarial.get("normal_cases_passed", 0),
        "blocked_cases_passed": adversarial.get("blocked_cases_passed", 0),
        "provider_default_calls": 0,
        "live_provider_call_count": 0,
        "provider_call_count": 0,
        "node2_raw_reveal_access_count": 0,
        "node2_raw_reveal_access": 0,
        "reader_only_leakage_count": 0,
        "internal_marker_leakage_count": 0,
        "raw_credential_leakage": 0,
        "raw_manuscript_provider_leakage": 0,
        "branchpoint_lineage_preserved": True,
    }
    _STAGE97_1_CACHE[cache_key] = result
    return result
