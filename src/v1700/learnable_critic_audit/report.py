from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from v1700.formula_signal_store import run_formula_signal_store
from v1700.formula_signal_store.loader import work_id_from_signal
from v1700.narrative_optimization.coefficients import NarrativePhysicsCoefficientSet

from .contracts import (
    AdvisoryOutputRecord,
    AlignmentResultRecord,
    CalibrationRunRecord,
    CoefficientDiffRecord,
    CoefficientStateRecord,
    CriticInputSourceRecord,
    DeterministicSeedRecord,
    HumanApprovalRecord,
    LearnableCriticConfig,
    RollbackRecord,
)
from .loader import validate_audit_fixture

LEARNABLE_CRITIC_AUDIT_MODE = "AUDIT_FIRST_LEARNABLE_CRITIC_FIXTURE"


def run_learnable_critic_audit_fixture(
    repo_root: Path | None = None,
    formula_signal_store_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    repo_root = repo_root or Path(__file__).resolve().parents[3]
    formula_signal_store_report = formula_signal_store_report or run_formula_signal_store(repo_root=repo_root)
    output_dir = repo_root / "release/current/learnable_critic_audit_pack"
    output_dir.mkdir(parents=True, exist_ok=True)

    signals = formula_signal_store_report.get("parts", {}).get("formula_signal_query_surface", {}).get("example_queries", {}).get("high_confidence", [])
    if not signals:
        signals = formula_signal_store_report.get("parts", {}).get("formula_signal_query_surface", {}).get("example_queries", {}).get("by_work", [])
    if not signals:
        signals = formula_signal_store_report.get("parts", {}).get("formula_signal_index", {}).get("entries", [])

    selected_signal = _select_signal(signals)
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    config = LearnableCriticConfig(
        critic_id="critic:emotion_calibration_audit",
        critic_name="Emotion Calibration Audit Critic",
        critic_axis="EMOTIONAL_MOMENTUM",
        allowed_input_types=("FormulaSignalRecord",),
        allowed_output_types=("LearnableCriticAdvisoryOutputRecord",),
        coefficient_schema_ref="NarrativePhysicsCoefficientSet.emotional_momentum_weight",
        source_policy_ref="docs/policies/narrative_corpus_source_policy.md",
        approval_policy_ref="docs/contracts/approval_decision_record_contract.md",
        status="ADVISORY_ONLY",
    )

    input_source = CriticInputSourceRecord(
        input_source_id="critic-input:sample-emotion-audit",
        critic_id=config.critic_id,
        source_record_id=str(selected_signal["formula_signal_id"]),
        source_record_type="FormulaSignalRecord",
        source_class="USER_PROVIDED_STRUCTURED_ANALYSIS_DB",
        rights_status="user_provided_structured_analysis_db",
        formula_signal_ref=str(selected_signal["formula_signal_id"]),
        corpus_signal_ref=f"formula_signal_store:{_signal_work_id(selected_signal)}",
        value_proof_ref="value_proof:pending_preregistration",
        provenance_ref="release/current/formula_signal_store_pack/formula_signal_store_report.json",
    )

    baseline = NarrativePhysicsCoefficientSet()
    before_value = baseline.emotional_momentum_weight
    after_value = round(before_value + 0.05, 6)

    before_state = CoefficientStateRecord(
        coefficient_state_id="coefficient-state:emotion:before",
        critic_id=config.critic_id,
        formula_id="formula:emotional_momentum",
        coefficient_name="emotional_momentum_weight",
        coefficient_value=before_value,
        coefficient_version="v0",
        created_at=created_at,
        source_basis="baseline_narrative_physics_coefficients",
        review_status="BASELINE_LOCKED",
    )
    after_state = CoefficientStateRecord(
        coefficient_state_id="coefficient-state:emotion:after",
        critic_id=config.critic_id,
        formula_id="formula:emotional_momentum",
        coefficient_name="emotional_momentum_weight",
        coefficient_value=after_value,
        coefficient_version="v0_candidate_1",
        created_at=created_at,
        source_basis="formula_signal_store_audit_fixture",
        review_status="CANDIDATE_REVIEW_REQUIRED",
    )

    seed = DeterministicSeedRecord(
        seed_id="seed:learnable-critic-audit",
        seed_value=17000616,
        run_id="calibration-run:emotion-audit",
        randomization_scope="audit_fixture_only",
        reproducibility_note="Static audit fixture, no hidden learning loop.",
    )

    calibration = CalibrationRunRecord(
        calibration_run_id="calibration-run:emotion-audit",
        critic_id=config.critic_id,
        input_source_refs=(input_source.input_source_id,),
        formula_signal_refs=(selected_signal["formula_signal_id"],),
        value_proof_refs=("value_proof:pending_preregistration",),
        learning_rate=0.0,
        iteration_count=0,
        loss_or_error_metric="fixture_only_no_runtime_optimization",
        seed_ref=seed.seed_id,
        created_at=created_at,
    )

    diff = CoefficientDiffRecord(
        coefficient_diff_id="coefficient-diff:emotion-audit",
        before_state_id=before_state.coefficient_state_id,
        after_state_id=after_state.coefficient_state_id,
        changed_fields=("coefficient_value", "coefficient_version"),
        old_values={"coefficient_value": before_value},
        new_values={"coefficient_value": after_value},
        change_reason="Audit-first candidate adjustment derived from a high-confidence emotional momentum signal.",
        source_signal_refs=(selected_signal["formula_signal_id"],),
        calibration_run_ref=calibration.calibration_run_id,
    )

    alignment = AlignmentResultRecord(
        alignment_result_id="alignment-result:emotion-audit",
        calibration_run_id=calibration.calibration_run_id,
        before_alignment=0.62,
        after_alignment=0.67,
        improvement_delta=0.05,
        failure_notes=(),
        overfit_warning=False,
        human_review_required=True,
    )

    rollback = RollbackRecord(
        rollback_id="rollback:emotion-audit",
        coefficient_diff_id=diff.coefficient_diff_id,
        rollback_target_state_id=before_state.coefficient_state_id,
        rollback_reason="Candidate coefficient remains advisory until human approval.",
        rollback_status="READY",
        performed_at=created_at,
    )

    approval = HumanApprovalRecord(
        approval_id="approval:emotion-audit",
        coefficient_diff_id=diff.coefficient_diff_id,
        reviewer_role="PRINCIPAL_AUTHORITY_REVIEWER",
        approval_status="PENDING_REVIEW",
        approval_note="Audit fixture prepared; no promotion until explicit human decision.",
        approved_at=created_at,
    )

    advisory_output = AdvisoryOutputRecord(
        advisory_output_id="advisory-output:emotion-audit",
        critic_id=config.critic_id,
        input_source_refs=(input_source.input_source_id,),
        output_type="LearnableCriticAdvisoryOutputRecord",
        score_or_label="ADJUST_EMOTIONAL_MOMENTUM_WEIGHT:+0.05",
        explanation="Audit fixture proposes a bounded, review-only emotional momentum coefficient adjustment.",
        confidence=round(float(selected_signal.get("confidence") or 0.0), 6),
        suggested_action="REVIEW_ONLY",
        canonical_mutation_allowed=False,
        review_status="APPROVAL_REQUIRED",
    )

    bundle = {
        "learnable_critic_config": config.to_dict(),
        "critic_input_source_record": input_source.to_dict(),
        "coefficient_state_before": before_state.to_dict(),
        "coefficient_state_after": after_state.to_dict(),
        "deterministic_seed_record": seed.to_dict(),
        "calibration_run_record": calibration.to_dict(),
        "coefficient_diff_record": diff.to_dict(),
        "alignment_result_record": alignment.to_dict(),
        "rollback_record": rollback.to_dict(),
        "human_approval_record": approval.to_dict(),
        "advisory_output_record": advisory_output.to_dict(),
        "selected_formula_signal": selected_signal,
    }
    validation = validate_audit_fixture(bundle)

    result = {
        "title": "Learnable Critic Audit Fixture",
        "status": "pass" if validation["status"] == "pass" else "blocked",
        "mode": LEARNABLE_CRITIC_AUDIT_MODE,
        "issues": list(validation["issues"]),
        "provider_default_calls": 0,
        "runtime_training_enabled": False,
        "actual_coefficient_optimization_enabled": False,
        "canonical_mutation_allowed": False,
        "approval_required": True,
        "paths": {
            "repo_root": str(repo_root),
            "source_formula_signal_store": str(repo_root / "release/current/formula_signal_store_pack/formula_signal_store_report.json"),
        },
        "counters": {
            "selected_signal_confidence": round(float(selected_signal.get("confidence") or 0.0), 6),
            "alignment_improvement_delta": alignment.improvement_delta,
            "input_source_count": 1,
            "coefficient_change_count": 1,
        },
        "parts": {
            **bundle,
            "audit_validation_report": validation,
        },
    }
    _write_outputs(output_dir, result)
    return result


def _select_signal(signals: list[dict[str, Any]]) -> dict[str, Any]:
    preferred = [signal for signal in signals if str(signal.get("formula_group", "")) == "Emotional Momentum"]
    candidates = preferred or signals
    return sorted(candidates, key=lambda item: float(item.get("confidence") or 0.0), reverse=True)[0]


def _signal_work_id(signal: dict[str, Any]) -> str:
    explicit = str(signal.get("work_id", "")).strip()
    if explicit:
        return explicit
    derived = work_id_from_signal(signal)
    if derived:
        return derived
    signal_id = str(signal.get("formula_signal_id", ""))
    return signal_id.rsplit(":", 1)[-1] if ":" in signal_id else "unknown_work"


def _write_outputs(output_dir: Path, payload: dict[str, Any]) -> None:
    parts = payload["parts"]
    _write_json(output_dir / "learnable_critic_config.json", parts["learnable_critic_config"])
    _write_json(output_dir / "critic_input_source_record.json", parts["critic_input_source_record"])
    _write_json(output_dir / "coefficient_state_before.json", parts["coefficient_state_before"])
    _write_json(output_dir / "coefficient_state_after.json", parts["coefficient_state_after"])
    _write_json(output_dir / "deterministic_seed_record.json", parts["deterministic_seed_record"])
    _write_json(output_dir / "calibration_run_record.json", parts["calibration_run_record"])
    _write_json(output_dir / "coefficient_diff_record.json", parts["coefficient_diff_record"])
    _write_json(output_dir / "alignment_result_record.json", parts["alignment_result_record"])
    _write_json(output_dir / "rollback_record.json", parts["rollback_record"])
    _write_json(output_dir / "human_approval_record.json", parts["human_approval_record"])
    _write_json(output_dir / "advisory_output_record.json", parts["advisory_output_record"])
    _write_json(output_dir / "audit_validation_report.json", parts["audit_validation_report"])
    _write_json(output_dir / "learnable_critic_audit_report.json", payload)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
