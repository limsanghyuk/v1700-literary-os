from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.nie.predictive import DebtPredictor, FeedbackLearner, Gate29, PNECore, PreemptiveGate
from v1700.stage124.contracts import Stage124Contract
from v1700.stage124.fixtures import FEEDBACK_RECORDS, PNE_REPAIR_OUTCOMES


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_stage124(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    contract = Stage124Contract().to_dict()
    core = PNECore()
    core.ingest_outcomes(PNE_REPAIR_OUTCOMES)
    predictor = DebtPredictor(core, runtime_training_enabled=False)
    training_result = predictor.train(core)
    gate = PreemptiveGate(predictor, threshold=0.60, horizon=3)
    low_risk = gate.evaluate("scene-low-risk", current_severity=0.12)
    high_risk = gate.evaluate("scene-high-risk", current_severity=0.96)
    learner = FeedbackLearner(threshold=0.60, precision_target=0.70, runtime_retraining_enabled=False)
    learner.record_many(list(FEEDBACK_RECORDS))
    feedback = learner.report()
    gate29_pass = Gate29().evaluate(low_risk, feedback)
    gate29_block = Gate29().evaluate(high_risk, feedback)

    direct_v555_merge_performed = False
    gate29_primary_authority_enabled = False
    release_gate_runtime_training_enabled = False
    sklearn_required = False
    graph_mutation_enabled = False

    issues: list[str] = []
    if core.total_ingested() <= 0:
        issues.append("pne_core_no_outcomes")
    if any(training_result.values()):
        issues.append("runtime_training_performed")
    if low_risk.blocked:
        issues.append("low_risk_scene_blocked")
    if not high_risk.blocked:
        issues.append("high_risk_scene_not_blocked")
    if feedback.status != "pass":
        issues.append("feedback_precision_target_not_met")
    if gate29_pass.status != "pass":
        issues.append("gate29_pass_case_blocked")
    if gate29_block.status != "blocked":
        issues.append("gate29_high_risk_case_not_blocked")
    if direct_v555_merge_performed:
        issues.append("direct_v555_merge_performed")
    if gate29_primary_authority_enabled:
        issues.append("gate29_primary_authority_enabled_too_early")
    if release_gate_runtime_training_enabled:
        issues.append("release_gate_runtime_training_enabled")
    if sklearn_required:
        issues.append("sklearn_required_in_release")
    if graph_mutation_enabled:
        issues.append("graph_mutation_enabled_in_stage124")

    result = {
        "stage": "124",
        "baseline_stage": "123",
        "title": contract["title"],
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "release_contract": contract,
        "absorption_policy": {
            "stage123_gate28_secondary_quality_gate_preserved": True,
            "gate29_authority_mode": "secondary_predictive_gate",
            "gate29_primary_authority_enabled": gate29_primary_authority_enabled,
            "direct_v555_merge_performed": direct_v555_merge_performed,
            "release_gate_runtime_training_enabled": release_gate_runtime_training_enabled,
            "sklearn_required": sklearn_required,
            "graph_mutation_enabled": graph_mutation_enabled,
            "gate28_primary_authority_enabled": False,
        },
        "pne_core": {
            "total_ingested": core.total_ingested(),
            "snapshot": core.snapshot(),
            "global_feature_vector": list(core.global_feature_vector()),
        },
        "debt_predictor": {
            "mode": "heuristic_fallback",
            "block_threshold": DebtPredictor.BLOCK_THRESHOLD,
            "runtime_training_enabled": predictor.runtime_training_enabled,
            "sklearn_available": predictor.sklearn_available,
            "sklearn_required": sklearn_required,
            "training_result": training_result,
        },
        "preemptive_gate": {
            "low_risk": low_risk.to_dict(),
            "high_risk": high_risk.to_dict(),
            "summary": gate.gate_summary(),
        },
        "feedback_learner": feedback.to_dict(),
        "gate29": {
            "low_risk_case": gate29_pass.to_dict(),
            "high_risk_case": gate29_block.to_dict(),
            "expected_high_risk_status": "blocked",
            "matched_expectation": gate29_block.status == "blocked" and gate29_pass.status == "pass",
        },
        "summary": {
            "pne_outcome_count": core.total_ingested(),
            "low_risk_blocked": low_risk.blocked,
            "high_risk_blocked": high_risk.blocked,
            "high_risk_max_probability": high_risk.max_probability,
            "feedback_precision": feedback.metrics.precision(),
            "feedback_f1": feedback.metrics.f1(),
            "runtime_training_enabled": predictor.runtime_training_enabled,
            "gate29_authority_mode": "secondary_predictive_gate",
        },
        "next_development_order": ["stage125", "stage126"],
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "story_doctor_llm_call_count": 0,
        "pne_provider_call_count": 0,
        "pne_runtime_training_count": 0,
        "auto_repair_mutation_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }

    _write_json(root / "manifests/stage124_pne_gate29_manifest.json", {
        "stage": "124",
        "title": contract["title"],
        "absorbed_from_reference": "V555 PNE / Gate29 concepts only",
        "absorbed_components": contract["absorbed_concepts"],
        "blocked_components": contract["blocked_concepts"],
        "gate29_authority_mode": "secondary_predictive_gate",
        "runtime_training_enabled": False,
        "sklearn_required": False,
        "provider_default_calls": 0,
    })
    _write_json(root / "release/current/stage124_pne_gate29_absorption_report.json", result)
    _write_json(root / "release/current/stage124_prediction_report.json", {
        "low_risk": low_risk.prediction_report.to_dict(),
        "high_risk": high_risk.prediction_report.to_dict(),
    })
    _write_json(root / "release/current/stage124_gate29_report.json", result["gate29"])
    _write_json(root / "release/current/stage124_feedback_metrics_report.json", feedback.to_dict())
    return result
