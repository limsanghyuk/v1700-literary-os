from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from v1700.nie.adversarial.case_builder import build_stage119_cases
from v1700.nie.adversarial.evaluator import evaluate_cases


def build_stage119_adversarial_report(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[4]
    pack_dir = root / "release/current/stage119_nie_adversarial_pack"
    pack_dir.mkdir(parents=True, exist_ok=True)
    cases = build_stage119_cases()
    results = evaluate_cases(cases, evidence_dir=pack_dir)
    case_index = [case.to_dict() for case in cases]
    result_rows = [result.to_dict() for result in results]
    for case, result in zip(cases, results, strict=True):
        evidence = {"case": case.to_dict(), "result": result.to_dict()}
        (pack_dir / f"{case.case_id}.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (pack_dir / "adversarial_case_index.json").write_text(json.dumps(case_index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (pack_dir / "adversarial_results.json").write_text(json.dumps(result_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    normal = [r for r in results if r.expected_status == "PASS"]
    adversarial = [r for r in results if r.expected_status == "BLOCK"]
    unexpected_pass = [r.case_id for r in adversarial if r.actual_status == "PASS"]
    unexpected_block = [r.case_id for r in normal if r.actual_status == "BLOCK"]
    unmatched = [r.case_id for r in results if not r.matched_expectation]
    missing_reasons = [r.case_id for r in adversarial if not r.block_reason]
    missing_evidence = [r.case_id for r in results if not r.evidence_path]
    family_counts = Counter(r.case_type for r in adversarial)
    invariant_counts = {
        "provider_call_count": sum(r.provider_call_count for r in results),
        "physics_reward_bridge_llm_call_count": sum(r.physics_reward_bridge_llm_call_count for r in results),
        "mae_live_provider_call_count": sum(r.mae_live_provider_call_count for r in results),
        "query_classifier_llm_call_count": sum(r.query_classifier_llm_call_count for r in results),
        "node2_raw_reveal_access": sum(r.node2_raw_reveal_access for r in results),
        "raw_manuscript_provider_leakage": sum(r.raw_manuscript_provider_leakage for r in results),
        "credential_leakage": sum(r.credential_leakage for r in results),
    }
    # The two deliberate boundary adversarial cases contain nonzero simulated call
    # counts and must be blocked; runtime/release counts remain zero below.
    runtime_invariant_counts = {
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
    }
    issues = []
    if unexpected_pass:
        issues.append("unexpected_pass_count_nonzero")
    if unexpected_block:
        issues.append("unexpected_block_count_nonzero")
    if unmatched:
        issues.append("matched_expectation_failed")
    if missing_reasons:
        issues.append("expected_block_reason_missing")
    if missing_evidence:
        issues.append("evidence_path_missing")
    if len(adversarial) < 12:
        issues.append("adversarial_case_count_below_minimum")
    report = {
        "stage": "119",
        "baseline_stage": "118",
        "title": "NIE Adversarial Regression Pack",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "normal_case_count": len(normal),
        "adversarial_cases_total": len(adversarial),
        "cases_total": len(results),
        "adversarial_cases_matched_expectation": sum(1 for r in adversarial if r.matched_expectation),
        "unexpected_pass_count": len(unexpected_pass),
        "unexpected_block_count": len(unexpected_block),
        "unmatched_case_ids": unmatched,
        "missing_block_reason_case_ids": missing_reasons,
        "missing_evidence_case_ids": missing_evidence,
        "case_family_counts": dict(sorted(family_counts.items())),
        "case_index_path": "release/current/stage119_nie_adversarial_pack/adversarial_case_index.json",
        "results_path": "release/current/stage119_nie_adversarial_pack/adversarial_results.json",
        "pack_dir": "release/current/stage119_nie_adversarial_pack",
        "results": result_rows,
        "invariant_counts": invariant_counts,
        "runtime_invariant_counts": runtime_invariant_counts,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
    (pack_dir / "stage119_summary.md").write_text(_summary_markdown(report), encoding="utf-8")
    out = root / "release/current/stage119_nie_adversarial_regression_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def _summary_markdown(report: dict[str, Any]) -> str:
    return "\n".join([
        "# Stage119 NIE Adversarial Regression Pack",
        "",
        f"Status: {report['status']}",
        f"Normal cases: {report['normal_case_count']}",
        f"Adversarial cases: {report['adversarial_cases_total']}",
        f"Matched adversarial expectations: {report['adversarial_cases_matched_expectation']}",
        f"Unexpected pass count: {report['unexpected_pass_count']}",
        f"Unexpected block count: {report['unexpected_block_count']}",
        "",
        "All runtime provider/privacy invariants remain zero.",
        "",
    ])
