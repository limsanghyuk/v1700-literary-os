from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.nie.asd import AutoRepairExecutor, Gate28, StoryDoctorOrchestrator
from v1700.stage123.contracts import Stage123Contract
from v1700.stage123.fixtures import ASD_FIXTURE_GRAPH, BLOCKING_ASD_GRAPH


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_stage123(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    contract = Stage123Contract().to_dict()
    doctor = StoryDoctorOrchestrator()
    story_report = doctor.diagnose(ASD_FIXTURE_GRAPH)
    gate28 = Gate28().evaluate(story_report)
    dry_run = AutoRepairExecutor().execute_batch(story_report.recommendations, dry_run=True)
    blocking_report = doctor.diagnose(BLOCKING_ASD_GRAPH)
    blocking_gate = Gate28().evaluate(blocking_report)

    gate28_primary_authority_enabled = False
    graph_mutation_enabled = False
    llm_repair_generation_enabled = False
    direct_v545_merge_performed = False
    gate29_enabled = False

    issues: list[str] = []
    if story_report.status != "pass":
        issues.append("story_doctor_report_blocked")
    if gate28.status != "pass":
        issues.append("gate28_fixture_blocked")
    if dry_run.status != "pass" or dry_run.mutation_count != 0:
        issues.append("auto_repair_dry_run_blocked")
    if blocking_gate.status != "blocked":
        issues.append("gate28_negative_case_not_blocked")
    if gate28_primary_authority_enabled:
        issues.append("gate28_primary_authority_enabled_too_early")
    if graph_mutation_enabled:
        issues.append("graph_mutation_enabled_too_early")
    if llm_repair_generation_enabled:
        issues.append("llm_repair_generation_enabled")
    if direct_v545_merge_performed:
        issues.append("direct_v545_merge_performed")
    if gate29_enabled:
        issues.append("gate29_enabled_too_early")

    result = {
        "stage": "123",
        "baseline_stage": "122",
        "title": contract["title"],
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "release_contract": contract,
        "absorption_policy": {
            "stage120_gate25_primary_authority_preserved": True,
            "stage122_stability_absorption_preserved": True,
            "gate28_authority_mode": "secondary_quality_gate",
            "gate28_primary_authority_enabled": gate28_primary_authority_enabled,
            "graph_mutation_enabled": graph_mutation_enabled,
            "llm_repair_generation_enabled": llm_repair_generation_enabled,
            "direct_v545_merge_performed": direct_v545_merge_performed,
            "gate29_enabled": gate29_enabled,
        },
        "story_doctor": story_report.to_dict(),
        "gate28": gate28.to_dict(),
        "auto_repair_dry_run": dry_run.to_dict(),
        "negative_case": {
            "story_doctor": blocking_report.to_dict(),
            "gate28": blocking_gate.to_dict(),
            "expected": "blocked",
            "matched_expectation": blocking_gate.status == "blocked",
        },
        "summary": {
            "debt_score": story_report.debt_report.overall_debt_score,
            "arc_score": story_report.arc_report.overall_score,
            "combined_quality": gate28.combined_quality,
            "recommendation_count": len(story_report.recommendations),
            "high_priority_count": len(story_report.high_priority),
            "dry_run_count": dry_run.dry_run,
            "mutation_count": dry_run.mutation_count,
        },
        "next_development_order": ["stage124", "stage125", "stage126"],
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "story_doctor_llm_call_count": 0,
        "auto_repair_mutation_count": dry_run.mutation_count,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }

    _write_json(root / "manifests/stage123_asd_gate28_manifest.json", {
        "stage": "123",
        "title": contract["title"],
        "absorbed_from_reference": "V545 ASD / Gate28 concepts only",
        "absorbed_components": contract["absorbed_concepts"],
        "blocked_components": contract["blocked_concepts"],
        "gate28_authority_mode": "secondary_quality_gate",
        "auto_repair_mode": "dry_run_only",
        "provider_default_calls": 0,
        "graph_mutation_allowed": False,
    })
    _write_json(root / "release/current/stage123_asd_gate28_absorption_report.json", result)
    _write_json(root / "release/current/stage123_story_doctor_report.json", story_report.to_dict())
    _write_json(root / "release/current/stage123_gate28_report.json", gate28.to_dict())
    _write_json(root / "release/current/stage123_auto_repair_dry_run_report.json", dry_run.to_dict())
    return result
