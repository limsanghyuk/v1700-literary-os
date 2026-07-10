from __future__ import annotations

from typing import Any


def validate_audit_fixture(bundle: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []

    input_source = bundle.get("critic_input_source_record", {})
    before_state = bundle.get("coefficient_state_before", {})
    after_state = bundle.get("coefficient_state_after", {})
    diff = bundle.get("coefficient_diff_record", {})
    seed = bundle.get("deterministic_seed_record", {})
    calibration = bundle.get("calibration_run_record", {})
    alignment = bundle.get("alignment_result_record", {})
    rollback = bundle.get("rollback_record", {})
    approval = bundle.get("human_approval_record", {})
    advisory = bundle.get("advisory_output_record", {})

    if not input_source.get("formula_signal_ref"):
        issues.append("missing_formula_signal_ref")
    if not input_source.get("source_class"):
        issues.append("missing_source_class")
    if not input_source.get("rights_status"):
        issues.append("missing_rights_status")

    if before_state.get("coefficient_state_id") != diff.get("before_state_id"):
        issues.append("before_state_diff_mismatch")
    if after_state.get("coefficient_state_id") != diff.get("after_state_id"):
        issues.append("after_state_diff_mismatch")
    if calibration.get("seed_ref") != seed.get("seed_id"):
        issues.append("seed_link_mismatch")
    if diff.get("calibration_run_ref") != calibration.get("calibration_run_id"):
        issues.append("calibration_diff_link_mismatch")
    if rollback.get("rollback_target_state_id") != before_state.get("coefficient_state_id"):
        issues.append("rollback_target_mismatch")
    if approval.get("coefficient_diff_id") != diff.get("coefficient_diff_id"):
        issues.append("approval_diff_mismatch")
    if advisory.get("canonical_mutation_allowed") is not False:
        issues.append("canonical_mutation_allowed")

    before_value = float(before_state.get("coefficient_value") or 0.0)
    after_value = float(after_state.get("coefficient_value") or 0.0)
    improvement = round(float(alignment.get("after_alignment") or 0.0) - float(alignment.get("before_alignment") or 0.0), 6)
    if round(after_value - before_value, 6) == 0.0:
        issues.append("coefficient_unchanged")
    if round(float(alignment.get("improvement_delta") or 0.0), 6) != improvement:
        issues.append("alignment_delta_mismatch")
    if approval.get("approval_status") not in {"PENDING_REVIEW", "APPROVED", "REJECTED"}:
        issues.append("invalid_approval_status")

    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "source_linked": bool(input_source.get("formula_signal_ref")),
        "seed_present": bool(seed.get("seed_id")),
        "rollback_ready": rollback.get("rollback_status") == "READY",
        "human_review_required": bool(alignment.get("human_review_required")),
        "canonical_mutation_allowed": bool(advisory.get("canonical_mutation_allowed")),
    }
