from __future__ import annotations

from pathlib import Path

from v1700.gates.stage92_release_gate import run_stage92_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.provider_adapters.credential_audit import audit_provider_credentials
from v1700.provider_adapters.live_sandbox import run_stage93_live_provider_sandbox
from v1700.provider_adapters.normalization import run_stage93_response_normalization_probe

_STAGE93_CACHE: dict[str, dict] = {}


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_stage93_release_gate(root: Path | None = None) -> dict:
    root = root or _project_root()
    cache_key = str(root.resolve())
    if cache_key in _STAGE93_CACHE:
        return _STAGE93_CACHE[cache_key]

    stage92 = run_stage92_release_gate(root)
    credential_audit = audit_provider_credentials().to_dict()
    normalization = run_stage93_response_normalization_probe().to_dict()
    sandbox = run_stage93_live_provider_sandbox(execution_allowed=False).to_dict()
    trace_gate = run_symbol_to_branchpoint_trace_gate(root)
    checks = {
        "stage92_release_gate": stage92,
        "stage93_credential_audit": credential_audit,
        "stage93_response_normalization": normalization,
        "stage93_live_provider_sandbox": sandbox,
        "symbol_to_branchpoint_trace_gate": trace_gate,
    }
    issues = [name for name, report in checks.items() if report.get("status") != "pass"]
    if credential_audit.get("secret_value_leaked"):
        issues.append("secret_value_leaked")
    if credential_audit.get("plain_secret_preview_count") != 0:
        issues.append("plain_secret_preview_count_not_zero")
    if normalization.get("normalized_provider_count") != 4:
        issues.append("normalized_provider_count_not_4")
    if sandbox.get("configured_provider_count") != 4:
        issues.append("sandbox_configured_provider_count_not_4")
    if sandbox.get("live_call_count") != 0:
        issues.append("sandbox_live_call_count_not_zero")
    if sandbox.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if sandbox.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")

    result = {
        "stage": "93",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage93 adds a live-provider opt-in sandbox, credential redaction audit, and provider response normalization for Ollama/GPT/Claude/Gemini while preserving provider-zero release gates.",
        "checks": checks,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
        "live_call_count": 0,
    }
    _STAGE93_CACHE[cache_key] = result
    return result
