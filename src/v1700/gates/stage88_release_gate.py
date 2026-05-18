from __future__ import annotations

from pathlib import Path

from v1700.agent_benchmark.harness import run_stage88_agent_benchmark_smoke
from v1700.gates.stage87_release_gate import run_stage87_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_stage88_release_gate(root: Path | None = None) -> dict:
    root = root or _project_root()
    stage87 = run_stage87_release_gate(root)
    agent_benchmark = run_stage88_agent_benchmark_smoke()
    trace_gate = run_symbol_to_branchpoint_trace_gate(root)
    checks = {
        "stage87_release_gate": stage87,
        "agent_blind_benchmark_smoke": agent_benchmark,
        "symbol_to_branchpoint_trace_gate": trace_gate,
    }
    issues = [name for name, report in checks.items() if report.get("status") != "pass"]
    if agent_benchmark.get("agent_count", 0) < 6:
        issues.append("agent_panel_below_minimum_6")
    if agent_benchmark.get("sample_count", 0) < 16:
        issues.append("blind_sample_count_below_minimum_16")
    if agent_benchmark.get("consensus_score", 0.0) < 8.0:
        issues.append("agent_consensus_score_below_8")
    if agent_benchmark.get("min_agent_average", 0.0) < 8.0:
        issues.append("agent_min_average_below_8")
    if agent_benchmark.get("min_sample_average", 0.0) < 8.0:
        issues.append("sample_min_average_below_8")
    if agent_benchmark.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if agent_benchmark.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")
    return {
        "stage": "88",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage88 proves AI-agent editor/reader blind benchmark evidence on top of Stage87 8-16 episode scale-up evidence.",
        "checks": checks,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
