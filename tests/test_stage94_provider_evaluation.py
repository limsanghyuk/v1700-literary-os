from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage94_release_gate import run_stage94_release_gate
from v1700.provider_evaluation.harness import ProviderEvaluationHarness, run_stage94_provider_evaluation_smoke
from v1700.provider_evaluation.prompt_suite import build_stage94_prompt_suite


def test_stage94_prompt_suite_contains_branchpoint_safe_common_prompts():
    prompts = build_stage94_prompt_suite()

    assert len(prompts) >= 2
    assert all(prompt.branchpoint_requirements for prompt in prompts)
    assert any("node2_surface_only" in prompt.branchpoint_requirements for prompt in prompts)


def test_stage94_provider_evaluation_runs_four_providers_without_live_calls():
    report = run_stage94_provider_evaluation_smoke()

    assert report["status"] == "pass"
    assert report["provider_count"] == 4
    assert report["prompt_count"] == 3
    assert report["evaluation_count"] == 12
    assert report["live_call_count"] == 0
    assert report["provider_default_calls"] == 0
    assert report["node2_raw_reveal_access_count"] == 0


def test_stage94_provider_scores_include_required_axes_and_profiles():
    report = ProviderEvaluationHarness().evaluate().to_dict()

    assert len(report["provider_profiles"]) == 4
    assert report["best_provider_id"]
    for score in report["scores"]:
        assert score["normalized_schema_pass"] is True
        assert score["latency_ms"] > 0
        assert score["input_tokens"] > 0
        assert score["output_tokens"] > 0
        assert score["safety_score"] >= 9.0
        assert score["literary_quality_score"] >= 8.0
        assert score["branchpoint_compliance_score"] >= 9.0


def test_stage94_evaluation_keeps_credentials_and_normalized_schema_safe():
    report = run_stage94_provider_evaluation_smoke()

    assert report["credential_secret_value_leaked"] is False
    assert report["normalized_schema_fail_count"] == 0


def test_stage94_release_gate_passes_and_inherits_stage93():
    gate = run_stage94_release_gate()

    assert gate["status"] == "pass"
    assert gate["checks"]["stage93_release_gate"]["status"] == "pass"
    assert gate["provider_default_calls"] == 0
    assert gate["live_call_count"] == 0


def test_main_release_gate_includes_stage94_when_active():
    result = run_release_gate()

    assert result["status"] == "pass"
    assert result["stage94_release_gate"]["status"] == "pass"
