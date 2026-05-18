from __future__ import annotations

from v1700.provider_evaluation.harness import run_stage94_provider_evaluation_smoke


def build_stage94_provider_evaluation_manifest() -> dict:
    report = run_stage94_provider_evaluation_smoke()
    return {
        "stage": "94",
        "status": report["status"],
        "title": "Live Provider Evaluation Harness",
        "provider_count": report["provider_count"],
        "prompt_count": report["prompt_count"],
        "evaluation_count": report["evaluation_count"],
        "best_provider_id": report["best_provider_id"],
        "live_call_count": report["live_call_count"],
        "provider_default_calls": report["provider_default_calls"],
        "node2_raw_reveal_access_count": report["node2_raw_reveal_access_count"],
        "acceptance": {
            "four_provider_adapter_contract": report["provider_count"] == 4,
            "dry_run_fixture_evaluation_pass": report["status"] == "pass",
            "credential_raw_value_leak_count_zero": report["credential_secret_value_leaked"] is False,
            "normalized_provider_response_schema_pass": report["normalized_schema_fail_count"] == 0,
        },
    }
