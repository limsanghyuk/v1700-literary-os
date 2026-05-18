from __future__ import annotations

from pathlib import Path

from v1700.episode_scaleup.evidence import run_stage87_episode_scaleup_smoke
from v1700.gates.stage86_release_gate import run_stage86_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_stage87_release_gate(root: Path | None = None) -> dict:
    root = root or _project_root()
    stage86 = run_stage86_release_gate(root)
    scaleup = run_stage87_episode_scaleup_smoke()
    trace_gate = run_symbol_to_branchpoint_trace_gate(root)
    checks = {
        "stage86_release_gate": stage86,
        "episode_scaleup_smoke": scaleup,
        "symbol_to_branchpoint_trace_gate": trace_gate,
    }
    issues = [name for name, report in checks.items() if report.get("status") != "pass"]
    eight = scaleup["eight_episode_evidence"]
    sixteen = scaleup["sixteen_episode_evidence"]
    if eight.get("episode_count") < 8 or eight.get("total_scene_count") < 80:
        issues.append("eight_episode_evidence_below_scale")
    if sixteen.get("episode_count") != 16 or sixteen.get("total_scene_count") < 160:
        issues.append("sixteen_episode_evidence_below_scale")
    if sixteen.get("blocked_direct_reveal_count", 0) <= 0:
        issues.append("sixteen_episode_reveal_budget_not_exercised")
    if sixteen.get("knowledge_constraint_count", 0) <= 0:
        issues.append("sixteen_episode_knowledge_constraints_not_exercised")
    if sixteen.get("min_quality_score", 0.0) < 8.0:
        issues.append("sixteen_episode_quality_floor_below_8")
    if scaleup.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if scaleup.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")
    return {
        "stage": "87",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage87 proves 8-16 episode scale-up evidence while preserving Stage86 Arc-Reveal-Knowledge and Stage85 traceability.",
        "checks": checks,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
