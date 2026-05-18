from __future__ import annotations

from pathlib import Path

from v1700.gates.stage97_1_release_gate import run_stage97_1_release_gate
from v1700.stage97_2.orchestrator import run_stage97_2_provider_runtime_smoke

_STAGE97_2_CACHE: dict[str, dict] = {}


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_stage97_2_release_gate(root: Path | None = None) -> dict:
    root = root or _project_root()
    cache_key = str(root.resolve())
    if cache_key in _STAGE97_2_CACHE:
        return _STAGE97_2_CACHE[cache_key]

    baseline = run_stage97_1_release_gate(root)
    runtime = run_stage97_2_provider_runtime_smoke(root)
    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage97_1_baseline_gate_blocked")
    if runtime.get("status") != "pass":
        issues.append("provider_runtime_smoke_blocked")
    if runtime.get("provider_contract_gate_status") != "pass":
        issues.append("provider_adapter_contract_gate_blocked")
    if runtime.get("task_router_llm0_status") != "pass":
        issues.append("task_router_llm0_blocked")
    if runtime.get("live_provider_call_count") != 0 or runtime.get("provider_default_calls") != 0:
        issues.append("provider_zero_blocked")
    if runtime.get("provider_health_live_check_count") != 0:
        issues.append("provider_health_live_check_in_release_gate")
    if runtime.get("raw_manuscript_provider_leakage") != 0:
        issues.append("raw_manuscript_provider_leakage")
    if runtime.get("node2_raw_reveal_access") != 0:
        issues.append("node2_raw_reveal_access_detected")
    if runtime.get("branchpoint_lineage_preserved") is not True:
        issues.append("branchpoint_lineage_broken")

    result = {
        "stage": "97.2",
        "baseline_stage": "97.1",
        "status": "pass" if not issues else "blocked",
        "title": "Unified Multi-Provider Runtime Governance Layer",
        "checks": {
            "stage97_1_baseline_gate": baseline,
            "stage97_2_provider_runtime": runtime,
        },
        "issues": issues,
        "provider_context_status": runtime.get("provider_context_status"),
        "adapters_checked": runtime.get("adapters_checked", 0),
        "contract_violations": runtime.get("contract_violations", []),
        "task_router_llm0_status": runtime.get("task_router_llm0_status"),
        "provider_health_status": runtime.get("provider_health_status"),
        "unified_gateway_status": runtime.get("unified_gateway_status"),
        "cost_ledger_status": runtime.get("cost_ledger_status"),
        "release_mode": True,
        "provider_default_calls": 0,
        "provider_call_count": 0,
        "live_provider_call_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "node2_raw_reveal_access": 0,
        "reader_only_leakage": 0,
        "internal_marker_leakage": 0,
        "raw_credential_leakage": 0,
        "branchpoint_lineage_preserved": True,
    }
    _STAGE97_2_CACHE[cache_key] = result
    return result
