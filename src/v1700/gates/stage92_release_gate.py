from __future__ import annotations

from pathlib import Path

from v1700.gates.stage91_release_gate import run_stage91_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.provider_adapters.router import run_stage92_multi_adapter_smoke
from v1700.provider_adapters.studio_bridge import run_stage92_studio_bridge_smoke

_STAGE92_CACHE: dict[str, dict] = {}


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_stage92_release_gate(root: Path | None = None) -> dict:
    root = root or _project_root()
    cache_key = str(root.resolve())
    if cache_key in _STAGE92_CACHE:
        return _STAGE92_CACHE[cache_key]

    stage91 = run_stage91_release_gate(root)
    adapter = run_stage92_multi_adapter_smoke()
    studio_bridge = run_stage92_studio_bridge_smoke()
    trace_gate = run_symbol_to_branchpoint_trace_gate(root)
    checks = {
        "stage91_release_gate": stage91,
        "stage92_multi_adapter_smoke": adapter,
        "stage92_studio_bridge_smoke": studio_bridge,
        "symbol_to_branchpoint_trace_gate": trace_gate,
    }
    issues = [name for name, report in checks.items() if report.get("status") != "pass"]
    if adapter.get("configured_provider_count") != 4:
        issues.append("configured_provider_count_not_4")
    if set(adapter.get("provider_kinds", [])) != {"ollama", "gpt", "claude", "gemini"}:
        issues.append("provider_kind_set_not_ollama_gpt_claude_gemini")
    if adapter.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if adapter.get("live_call_count") != 0:
        issues.append("live_call_count_not_zero")
    if adapter.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")
    if studio_bridge.get("provider_panel_item_count") != 4:
        issues.append("studio_provider_panel_item_count_not_4")

    result = {
        "stage": "92",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage92 adds a local multi-provider adapter runtime for Ollama, GPT, Claude, and Gemini while preserving provider-zero release execution.",
        "checks": checks,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
    _STAGE92_CACHE[cache_key] = result
    return result
