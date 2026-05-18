from __future__ import annotations

from pathlib import Path

from v1700.arc_reveal_knowledge.stage86_smoke import run_stage86_arc_reveal_knowledge_smoke
from v1700.gates.stage85_release_gate import run_stage85_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_stage86_release_gate(root: Path | None = None) -> dict:
    root = root or _project_root()
    stage85 = run_stage85_release_gate(root)
    arc_reveal_knowledge = run_stage86_arc_reveal_knowledge_smoke()
    trace_gate = run_symbol_to_branchpoint_trace_gate(root)
    checks = {
        "stage85_release_gate": stage85,
        "arc_reveal_knowledge_smoke": arc_reveal_knowledge,
        "symbol_to_branchpoint_trace_gate": trace_gate,
    }
    issues = [
        name
        for name, report in checks.items()
        if report.get("status") != "pass"
    ]
    if arc_reveal_knowledge.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if arc_reveal_knowledge.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")
    if arc_reveal_knowledge["series_arc"]["act_structure"]["episode_count"] != 16:
        issues.append("series_arc_not_16_episodes")
    if arc_reveal_knowledge["series_arc"]["edge_counts"].get("causal", 0) < 15:
        issues.append("causal_plot_graph_under_connected")
    return {
        "stage": "86",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": (
            "Stage86 absorbs V380 Arc-Reveal-Knowledge concepts into V1700 as "
            "live, test-guarded branchpoint logic."
        ),
        "checks": checks,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
