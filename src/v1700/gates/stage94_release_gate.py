from __future__ import annotations

from pathlib import Path

from v1700.gates.stage93_release_gate import run_stage93_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.provider_evaluation.harness import run_stage94_provider_evaluation_smoke

_STAGE94_CACHE: dict[str, dict] = {}


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_stage94_release_gate(root: Path | None = None) -> dict:
    root = root or _project_root()
    cache_key = str(root.resolve())
    if cache_key in _STAGE94_CACHE:
        return _STAGE94_CACHE[cache_key]

    stage93 = run_stage93_release_gate(root)
    provider_evaluation = run_stage94_provider_evaluation_smoke()
    trace_gate = run_symbol_to_branchpoint_trace_gate(root)
    checks = {
        "stage93_release_gate": stage93,
        "stage94_provider_evaluation": provider_evaluation,
        "symbol_to_branchpoint_trace_gate": trace_gate,
    }
    issues = [name for name, report in checks.items() if report.get("status") != "pass"]
    if provider_evaluation.get("provider_count") != 4:
        issues.append("provider_count_not_4")
    if provider_evaluation.get("prompt_count", 0) < 2:
        issues.append("prompt_count_below_2")
    if provider_evaluation.get("live_call_count") != 0:
        issues.append("live_call_count_not_zero")
    if provider_evaluation.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if provider_evaluation.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")
    if provider_evaluation.get("credential_secret_value_leaked"):
        issues.append("credential_secret_value_leaked")
    if provider_evaluation.get("normalized_schema_fail_count") != 0:
        issues.append("normalized_schema_fail_count_not_zero")

    result = {
        "stage": "94",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage94 compares Ollama/GPT/Claude/Gemini provider responses through a release-safe dry-run evaluation harness while preserving provider-zero gates.",
        "checks": checks,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
        "live_call_count": 0,
    }
    _STAGE94_CACHE[cache_key] = result
    return result
