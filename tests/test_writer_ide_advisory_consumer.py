from __future__ import annotations

from pathlib import Path

from v1700.formula_signal_store import run_formula_signal_store
from v1700.learnable_critic_audit import run_learnable_critic_audit_fixture
from v1700.writer_ide_advisory_consumer import WRITER_IDE_ADVISORY_CONSUMER_MODE, run_writer_ide_advisory_consumer


def _sample_bridge_report() -> dict:
    return {
        "status": "pass",
        "parts": {
            "formula_signal_registry": [
                {
                    "formula_signal_id": "formula-signal:tensor:sample_work",
                    "formula_id": "formula:narrative_state_tensor",
                    "formula_group": "Narrative State Tensor",
                    "source_record_ids": ["canonical_work:sample_work", "learning_signal:sample_work"],
                    "source_record_types": ["CanonicalWorkRecord", "LearningSignalRecord"],
                    "input_field_names": ["mean_conflict_intensity", "mean_scene_energy_ratio"],
                    "source_class_summary": "metadata_only_corpus_records",
                    "rights_status_summary": "user_provided_structured_analysis_db",
                    "output_signal_type": "NARRATIVE_STATE_TENSOR_SIGNAL",
                    "output_signal_value_or_label": "PASS",
                    "confidence": 0.81,
                    "explanation_summary": "Advisory tensor signal for sample_work.",
                    "signal_type_label": "CALCULATED_SIGNAL",
                    "critic_mapping_ref": "critic:narrative_state_tensor",
                    "value_proof_mapping_ref": "value_proof:arm_b_formula_guidance",
                    "writer_ide_panel_ref": "writer_ide:right_panel:narrative_state_tensor",
                    "created_at": "2026-06-16T00:00:00+00:00",
                    "review_status": "VALID_FOR_VALUE_PROOF_PREREGISTRATION",
                },
                {
                    "formula_signal_id": "formula-signal:emotion:sample_work",
                    "formula_id": "formula:emotional_momentum",
                    "formula_group": "Emotional Momentum",
                    "source_record_ids": ["learning_signal:sample_work"],
                    "source_record_types": ["LearningSignalRecord"],
                    "input_field_names": ["mean_conflict_intensity", "mean_dialogue_ratio"],
                    "source_class_summary": "metadata_only_corpus_records",
                    "rights_status_summary": "user_provided_structured_analysis_db",
                    "output_signal_type": "EMOTIONAL_MOMENTUM_SIGNAL",
                    "output_signal_value_or_label": "intensity=0.7000",
                    "confidence": 0.76,
                    "explanation_summary": "Advisory emotional signal for sample_work.",
                    "signal_type_label": "CALCULATED_SIGNAL",
                    "critic_mapping_ref": "critic:emotion",
                    "value_proof_mapping_ref": "value_proof:arm_b_formula_guidance",
                    "writer_ide_panel_ref": "writer_ide:right_panel:emotional_momentum",
                    "created_at": "2026-06-16T00:00:00+00:00",
                    "review_status": "VALID_FOR_UI_WIRING",
                },
                {
                    "formula_signal_id": "formula-signal:rag:sample_work",
                    "formula_id": "formula:retrieval_grounding",
                    "formula_group": "RAG/BM25/RRF retrieval fusion",
                    "source_record_ids": ["rag_index:sample_work"],
                    "source_record_types": ["RagIndexRecord"],
                    "input_field_names": ["scene_count", "chunk_count"],
                    "source_class_summary": "metadata_only_index_records",
                    "rights_status_summary": "user_provided_structured_analysis_db",
                    "output_signal_type": "NARRATIVE_FITNESS_COMPANION_SIGNAL",
                    "output_signal_value_or_label": "RAG_READY",
                    "confidence": 1.0,
                    "explanation_summary": "Advisory retrieval signal for sample_work.",
                    "signal_type_label": "CALCULATED_SIGNAL",
                    "critic_mapping_ref": "critic:retrieval_grounding",
                    "value_proof_mapping_ref": "value_proof:retrieval_context_panel",
                    "writer_ide_panel_ref": "writer_ide:left_panel:corpus_reference",
                    "created_at": "2026-06-16T00:00:00+00:00",
                    "review_status": "VALID_FOR_UI_WIRING",
                },
            ]
        },
    }


def test_writer_ide_advisory_consumer_builds_review_locked_surface(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir(parents=True, exist_ok=True)
    formula_signal_store_report = run_formula_signal_store(repo_root=repo_root, bridge_report=_sample_bridge_report())
    learnable_critic_audit_report = run_learnable_critic_audit_fixture(
        repo_root=repo_root,
        formula_signal_store_report=formula_signal_store_report,
    )

    result = run_writer_ide_advisory_consumer(
        repo_root=repo_root,
        formula_signal_store_report=formula_signal_store_report,
        learnable_critic_audit_report=learnable_critic_audit_report,
    )

    assert result["status"] == "pass"
    assert result["mode"] == WRITER_IDE_ADVISORY_CONSUMER_MODE
    assert result["advisory_only"] is True
    assert result["canonical_mutation_allowed"] is False
    assert result["counters"]["focus_work_id"] == "sample_work"
    assert result["parts"]["writer_session_record"]["session_scope"] == "LEARNABLE_CRITIC_REVIEW"
    assert result["parts"]["writer_session_record"]["session_status"] == "LOCKED_FOR_REVIEW"
    assert result["parts"]["approval_boundary_warning"]["approval_status"] == "PENDING_REVIEW"
    assert result["parts"]["writer_ide_surface_cards"]["card_count"] == 4
    assert result["parts"]["writer_ide_advisory_validation_report"]["status"] == "pass"

