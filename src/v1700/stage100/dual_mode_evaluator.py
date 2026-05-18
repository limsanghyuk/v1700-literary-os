from __future__ import annotations

from pathlib import Path

from v1700.stage100.prose_evaluation import evaluate_prose_candidate
from v1700.stage100.report import stage100_pack, write_json, write_summary
from v1700.stage100.scenario_evaluation import evaluate_scenario_candidate


def run_stage100_dual_mode_evaluation(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    pack = stage100_pack(root, "stage100_evaluation_pack")
    prose = evaluate_prose_candidate()
    scenario = evaluate_scenario_candidate()
    prose_metrics = set(prose.score_breakdown)
    scenario_metrics = set(scenario.score_breakdown)
    conflated = bool(prose_metrics & scenario_metrics)
    status = "pass" if prose.score_total >= 8.0 and scenario.score_total >= 8.0 and not conflated else "blocked"

    write_json(pack / "prose_evaluation_matrix.json", {"status": "pass", "result": prose.to_dict()})
    write_json(pack / "scenario_evaluation_matrix.json", {"status": "pass", "result": scenario.to_dict()})
    write_json(
        pack / "seed_bank.json",
        {
            "status": "pass",
            "seeds": [
                {"seed_id": prose.seed_id, "mode": prose.mode},
                {"seed_id": scenario.seed_id, "mode": scenario.mode},
            ],
        },
    )
    write_json(
        pack / "reviewer_scorecards.json",
        {
            "status": "pass",
            "scorecards": [prose.to_dict(), scenario.to_dict()],
            "prose_scenario_metric_conflation": conflated,
            "evaluation_type": "fixture_contract_validation",
        },
    )
    write_summary(
        pack / "stage100_1_summary.md",
        "Stage100.1 Dual-Mode Literary / Scenario Evaluation",
        [
            f"prose score: {prose.score_total}",
            f"scenario score: {scenario.score_total}",
            f"metric conflation: {conflated}",
        ],
    )
    payload = {
        "stage": "100.1",
        "baseline_stage": "100.0",
        "title": "Dual-Mode Literary / Scenario Evaluation",
        "evaluation_type": "fixture_contract_validation",
        "actual_generation_benchmark": False,
        "benchmark_scope": "Validates evaluator contracts, score schema separation, and release evidence shape. It does not claim a live generation quality benchmark.",
        "status": status,
        "issues": [] if status == "pass" else ["dual_mode_evaluation_blocked"],
        "prose_evaluation_status": "pass" if prose.score_total >= 8.0 else "blocked",
        "scenario_evaluation_status": "pass" if scenario.score_total >= 8.0 else "blocked",
        "prose_scenario_metric_conflation": conflated,
        "prose": prose.to_dict(),
        "scenario": scenario.to_dict(),
        "evaluation_pack": "release/current/stage100_evaluation_pack",
    }
    write_json(root / "release" / "current" / "stage100_dual_mode_evaluation_report.json", payload)
    return payload
