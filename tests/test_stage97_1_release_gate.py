from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage97_1_release_gate import run_stage97_1_release_gate
from v1700.longform_adversarial.adversarial_orchestrator import run_stage97_1_adversarial_validation

ROOT = Path(__file__).resolve().parents[1]


def test_stage97_1_adversarial_validation_matches_all_expectations():
    report = run_stage97_1_adversarial_validation(ROOT)
    assert report["status"] == "pass"
    assert report["adversarial_cases_total"] >= 19
    assert report["adversarial_cases_matched_expectation"] == report["adversarial_cases_total"]
    assert report["normal_cases_passed"] == report["normal_cases_total"]
    assert report["blocked_cases_passed"] == report["blocked_cases_total"]
    assert report["provider_default_calls"] == 0
    assert report["node2_raw_reveal_access_count"] == 0
    assert report["raw_manuscript_provider_leakage"] == 0


def test_stage97_1_release_gate_inherits_stage97_and_preserves_boundaries():
    gate = run_stage97_1_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["stage97_baseline_gate"]["status"] == "pass"
    assert gate["provider_call_count"] == 0
    assert gate["node2_raw_reveal_access"] == 0
    assert gate["raw_manuscript_provider_leakage"] == 0


def test_main_release_gate_includes_stage97_1_when_active():
    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage97_release_gate"]["status"] == "pass"
    assert result["stage97_1_release_gate"]["status"] == "pass"
