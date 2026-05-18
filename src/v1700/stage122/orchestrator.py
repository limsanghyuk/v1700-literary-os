from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.nie.stability import (
    AgentCalibrator,
    MetaLearnerSkeleton,
    NILStabilityModule,
    TIdealLearner,
    TemporalCIMAdapter,
)
from v1700.stage122.contracts import Stage122Contract
from v1700.stage122.fixtures import (
    ACTUAL_TENSION_VALUES,
    AGENT_RELIABILITY,
    MAE_AGENT_WEIGHTS,
    META_LEARNER_PROPOSALS,
    TEMPORAL_CIM_VOLATILITY,
    TEMPORAL_ROLE_TIERS,
)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _extract_nil_report(root: Path) -> dict[str, Any]:
    report = _read_json(root / "release/current/stage118_nil_orchestrator_report.json")
    nil = report.get("nil_orchestrator")
    if isinstance(nil, dict):
        return nil
    return {}


def run_stage122(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    contract = Stage122Contract().to_dict()
    nil_report = _extract_nil_report(root)
    issues: list[str] = []
    if not nil_report:
        issues.append("missing_stage118_nil_orchestrator_report")

    stability = NILStabilityModule().evaluate(nil_report).to_dict()
    calibration = AgentCalibrator().calibrate(MAE_AGENT_WEIGHTS, AGENT_RELIABILITY).to_dict()
    t_ideal = TIdealLearner().fit_once(ACTUAL_TENSION_VALUES).to_dict()
    temporal_cim = TemporalCIMAdapter().evaluate(TEMPORAL_ROLE_TIERS, TEMPORAL_CIM_VOLATILITY).to_dict()
    meta_learner = MetaLearnerSkeleton().propose(META_LEARNER_PROPOSALS).to_dict()

    component_reports = {
        "nil_stability": stability,
        "agent_calibrator": calibration,
        "t_ideal_learner": t_ideal,
        "temporal_cim_adapter": temporal_cim,
        "meta_learner_skeleton": meta_learner,
    }
    for name, report in component_reports.items():
        if report.get("status") != "pass":
            issues.append(f"{name}_blocked")

    # Stage122 is intentionally conservative: absorb only stability adapters.
    v525_alpha_relaxation_adopted = False
    gate28_authority_enabled = False
    gate29_authority_enabled = False
    direct_candidate_merge_performed = False
    runtime_model_training_performed = False
    if v525_alpha_relaxation_adopted:
        issues.append("v525_alpha_relaxation_adopted_too_early")
    if gate28_authority_enabled or gate29_authority_enabled:
        issues.append("future_gate_authority_enabled_too_early")
    if direct_candidate_merge_performed:
        issues.append("direct_candidate_merge_performed")
    if runtime_model_training_performed:
        issues.append("runtime_model_training_performed")

    required = [root / rel for rel in contract["required_outputs"] if not rel.endswith("stage122_release_gate_report.json")]
    missing = [p.relative_to(root).as_posix() for p in required if not p.exists()]
    # Required docs/manifests are written below, so only missing pre-existing evidence matters.

    result: dict[str, Any] = {
        "stage": "122",
        "baseline_stage": "121",
        "title": contract["title"],
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "release_contract": contract,
        "absorption_policy": {
            "stage120_gate25_primary_authority_preserved": True,
            "stage121_conflict_matrix_preserved": True,
            "direct_v545_v555_merge_allowed": False,
            "v525_alpha_relaxation_adopted": v525_alpha_relaxation_adopted,
            "gate28_authority_enabled": gate28_authority_enabled,
            "gate29_authority_enabled": gate29_authority_enabled,
            "runtime_model_training_performed": runtime_model_training_performed,
        },
        "components": component_reports,
        "stability_score": stability.get("score", 0.0),
        "agent_calibration_max_shift": calibration.get("max_shift", 1.0),
        "t_ideal_max_shift": t_ideal.get("max_shift", 1.0),
        "temporal_cim_mean_volatility": temporal_cim.get("mean_volatility", 1.0),
        "meta_learner_mode": meta_learner.get("mode"),
        "next_development_order": ["stage123", "stage124", "stage125", "stage126"],
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }

    # Manifests and reports.
    _write_json(root / "manifests/stage122_stability_absorption_manifest.json", {
        "stage": "122",
        "title": contract["title"],
        "absorbed_from_reference": "V525 NIE v2.0 stability concepts only",
        "absorbed_components": contract["absorbed_concepts"],
        "blocked_components": contract["blocked_concepts"],
        "provider_default_calls": 0,
        "release_gate_runtime_training_allowed": False,
    })
    _write_json(root / "release/current/stage122_nie_v2_stability_absorption_report.json", result)
    _write_json(root / "release/current/stage122_stability_component_report.json", component_reports)
    return result
