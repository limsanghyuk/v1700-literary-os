from __future__ import annotations

from pathlib import Path

from v1700.formula_signal_store import FORMULA_SIGNAL_STORE_MODE, query_formula_signals, run_formula_signal_store, validate_formula_signal_records


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
                    "input_field_names": [
                        "mean_conflict_intensity",
                        "mean_scene_energy_ratio",
                    ],
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
                    "input_field_names": [
                        "mean_conflict_intensity",
                        "mean_dialogue_ratio",
                    ],
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
                    "input_field_names": [
                        "scene_count",
                        "chunk_count",
                    ],
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


def test_formula_signal_store_builds_queryable_advisory_pack(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir(parents=True, exist_ok=True)
    result = run_formula_signal_store(repo_root=repo_root, bridge_report=_sample_bridge_report())

    assert result["status"] == "pass"
    assert result["mode"] == FORMULA_SIGNAL_STORE_MODE
    assert result["advisory_only"] is True
    assert result["canonical_mutation_allowed"] is False
    assert result["counters"]["signal_count"] == 3
    assert result["counters"]["work_count"] == 1
    assert result["parts"]["formula_signal_index"]["entry_count"] == 3
    assert result["parts"]["writer_ide_advisory_cards"]["card_count"] == 3


def test_formula_signal_loader_validation_and_query_surface() -> None:
    records = _sample_bridge_report()["parts"]["formula_signal_registry"]
    validation = validate_formula_signal_records(records)
    assert validation["status"] == "pass"
    assert validation["duplicate_ids"] == []
    assert validation["invalid_confidence"] == []

    high_confidence = query_formula_signals(records, work_id="sample_work", min_confidence=0.8)
    assert len(high_confidence) == 2
    assert {record["formula_group"] for record in high_confidence} == {
        "Narrative State Tensor",
        "RAG/BM25/RRF retrieval fusion",
    }
