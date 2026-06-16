from __future__ import annotations

from pathlib import Path

from v1700.learnable_critic_audit import LEARNABLE_CRITIC_AUDIT_MODE, run_learnable_critic_audit_fixture, validate_audit_fixture


def _sample_formula_signal_store_report() -> dict:
    return {
        "status": "pass",
        "parts": {
            "formula_signal_query_surface": {
                "example_queries": {
                    "high_confidence": [
                        {
                            "formula_signal_id": "formula-signal:emotion:sample_work",
                            "work_id": "sample_work",
                            "formula_group": "Emotional Momentum",
                            "formula_id": "formula:emotional_momentum",
                            "confidence": 0.92,
                            "writer_ide_panel_ref": "writer_ide:right_panel:emotional_momentum",
                            "review_status": "VALID_FOR_UI_WIRING",
                        }
                    ]
                }
            }
        },
    }


def test_learnable_critic_audit_fixture_is_advisory_and_passes(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir(parents=True, exist_ok=True)
    result = run_learnable_critic_audit_fixture(
        repo_root=repo_root,
        formula_signal_store_report=_sample_formula_signal_store_report(),
    )

    assert result["status"] == "pass"
    assert result["mode"] == LEARNABLE_CRITIC_AUDIT_MODE
    assert result["runtime_training_enabled"] is False
    assert result["actual_coefficient_optimization_enabled"] is False
    assert result["canonical_mutation_allowed"] is False
    assert result["approval_required"] is True
    assert result["parts"]["human_approval_record"]["approval_status"] == "PENDING_REVIEW"


def test_learnable_critic_validation_blocks_canonical_mutation() -> None:
    bundle = {
        "critic_input_source_record": {
            "formula_signal_ref": "formula-signal:emotion:sample_work",
            "source_class": "USER_PROVIDED_STRUCTURED_ANALYSIS_DB",
            "rights_status": "user_provided_structured_analysis_db",
        },
        "coefficient_state_before": {"coefficient_state_id": "before", "coefficient_value": 1.0},
        "coefficient_state_after": {"coefficient_state_id": "after", "coefficient_value": 1.1},
        "coefficient_diff_record": {"before_state_id": "before", "after_state_id": "after", "coefficient_diff_id": "diff", "calibration_run_ref": "run"},
        "deterministic_seed_record": {"seed_id": "seed"},
        "calibration_run_record": {"seed_ref": "seed", "calibration_run_id": "run"},
        "alignment_result_record": {"before_alignment": 0.6, "after_alignment": 0.7, "improvement_delta": 0.1, "human_review_required": True},
        "rollback_record": {"rollback_target_state_id": "before", "rollback_status": "READY"},
        "human_approval_record": {"coefficient_diff_id": "diff", "approval_status": "PENDING_REVIEW"},
        "advisory_output_record": {"canonical_mutation_allowed": True},
    }
    validation = validate_audit_fixture(bundle)
    assert validation["status"] == "blocked"
    assert "canonical_mutation_allowed" in validation["issues"]
