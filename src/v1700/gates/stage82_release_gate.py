from __future__ import annotations
from pathlib import Path

from v1700.blind_critic import run_blind_critic_benchmark
from v1700.gates.stage81_1_release_gate import run_stage81_1_release_gate


def run_stage82_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    stage81_1 = run_stage81_1_release_gate(root)
    benchmark = run_blind_critic_benchmark()
    issues: list[str] = []
    if stage81_1.get("status") != "pass":
        issues.append("stage81_1_release_gate_blocked")
    if benchmark.get("status") != "pass":
        issues.append("blind_critic_benchmark_blocked")
    if benchmark.get("v1700_margin_over_pure_gpt", 0.0) < 1.0:
        issues.append("v1700_margin_over_pure_gpt_too_low")
    if benchmark.get("reveal_leakage_count", 0) != 0:
        issues.append("blind_candidate_reveal_leakage_detected")
    return {
        "stage": "82",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage82 adds a local-first blind critic evaluation harness comparing V1700 against pure GPT direct-mode and Claude-style reference simulations.",
        "stage81_1_release_gate": stage81_1,
        "blind_critic_benchmark": benchmark,
        "winner_source_label": benchmark.get("winner_source_label"),
        "v1700_margin_over_pure_gpt": benchmark.get("v1700_margin_over_pure_gpt"),
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
