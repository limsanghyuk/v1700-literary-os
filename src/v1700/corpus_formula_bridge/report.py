from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from v1700.corpus_absorption import run_local_corpus_absorption
from v1700.literary_formulas.emotional_momentum import EmotionalMomentumVector
from v1700.narrative_state_tensor.contracts import NarrativeStateTensor

from .contracts import CorpusFormulaBridgeReport, FormulaSignalRecord

FORMULA_BRIDGE_MODE = "LOCAL_METADATA_ONLY_CORPUS_FORMULA_BRIDGE"


def run_local_corpus_formula_bridge(
    repo_root: Path | None = None,
    absorption_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    repo_root = repo_root or Path(__file__).resolve().parents[3]
    absorption_report = absorption_report or run_local_corpus_absorption(repo_root=repo_root)
    output_dir = repo_root / "release/current/corpus_formula_bridge_pack"
    output_dir.mkdir(parents=True, exist_ok=True)

    issues: list[str] = []
    if absorption_report.get("status") != "pass":
        issues.append("absorption_report_not_pass")

    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    formula_signals: list[FormulaSignalRecord] = []
    tensors: list[NarrativeStateTensor] = []

    learning_registry = absorption_report.get("parts", {}).get("learning_signal_registry", [])
    rag_registry_by_work = {
        record["work_id"]: record
        for record in absorption_report.get("parts", {}).get("rag_index_registry", [])
        if isinstance(record, dict)
    }

    for record in learning_registry:
        if not isinstance(record, dict):
            continue
        work_id = str(record.get("work_id", ""))
        if not work_id:
            continue
        feature_scene_count = int(record.get("feature_scene_count") or 0)
        rag_record = rag_registry_by_work.get(work_id, {})

        tensor = _build_narrative_state_tensor(record, rag_record)
        tensors.append(tensor)

        formula_signals.extend(
            [
                _build_tensor_signal(work_id, tensor, feature_scene_count, created_at),
                _build_emotional_signal(work_id, record, feature_scene_count, created_at),
                _build_rag_signal(work_id, rag_record, created_at),
            ]
        )

    if not tensors:
        issues.append("no_tensors_emitted")
    if not formula_signals:
        issues.append("no_formula_signals_emitted")

    notes = (
        "metadata_only_formula_bridge",
        "signals_are_advisory",
        "writer_authority_unchanged",
        "corpus_absorption_is_formula_input_surface",
    )
    counters = {
        "formula_signal_count": len(formula_signals),
        "tensor_count": len(tensors),
        "pass_tensor_count": sum(1 for tensor in tensors if tensor.status == "PASS"),
        "watch_tensor_count": sum(1 for tensor in tensors if tensor.status == "WATCH"),
        "review_tensor_count": sum(1 for tensor in tensors if tensor.status == "REVIEW_REQUIRED"),
    }
    report = CorpusFormulaBridgeReport(
        corpus_id=str(absorption_report.get("corpus_id", "corpus_ko")),
        status="pass" if not issues else "blocked",
        formula_signals=tuple(formula_signals),
        narrative_state_tensors=tuple(tensors),
        issues=tuple(issues),
        counters=counters,
        notes=notes,
    )
    payload = _build_result_payload(report, absorption_report, repo_root)
    _write_outputs(output_dir, payload)
    return payload


def _build_result_payload(
    report: CorpusFormulaBridgeReport,
    absorption_report: dict[str, Any],
    repo_root: Path,
) -> dict[str, Any]:
    data = report.to_dict()
    tensor_dimensions = {}
    if data["narrative_state_tensors"]:
        dims = list(data["narrative_state_tensors"][0]["dimensions"].keys())
        for dim in dims:
            values = [tensor["dimensions"][dim] for tensor in data["narrative_state_tensors"]]
            tensor_dimensions[dim] = round(sum(values) / len(values), 6)
    return {
        "corpus_id": report.corpus_id,
        "title": "Local Corpus Formula Bridge",
        "status": report.status,
        "mode": FORMULA_BRIDGE_MODE,
        "issues": list(report.issues),
        "notes": list(report.notes),
        "counters": report.counters,
        "provider_default_calls": 0,
        "runtime_training_enabled": False,
        "node2_raw_reveal_access": 0,
        "verbatim_text_exported": False,
        "raw_vectors_exported": False,
        "paths": {
            "repo_root": str(repo_root),
            "source_absorption_report": str(repo_root / "release/current/corpus_ko_absorption_pack/corpus_absorption_report.json"),
        },
        "parts": {
            "formula_signal_registry": data["formula_signals"],
            "narrative_state_tensor_registry": data["narrative_state_tensors"],
            "bridge_summary": {
                "average_tensor_dimensions": tensor_dimensions,
                "signal_groups": sorted({signal["formula_group"] for signal in data["formula_signals"]}),
                "advisory_only": True,
                "value_proof_ready_count": sum(
                    1 for signal in data["formula_signals"] if signal["review_status"] == "VALID_FOR_VALUE_PROOF_PREREGISTRATION"
                ),
                "writer_panel_refs": sorted({signal["writer_ide_panel_ref"] for signal in data["formula_signals"]}),
                "source_work_count": absorption_report.get("counters", {}).get("work_count", 0),
                "rag_ready_count": absorption_report.get("counters", {}).get("rag_ready_count", 0),
                "learning_ready_count": absorption_report.get("counters", {}).get("learning_ready_count", 0),
            },
        },
    }


def _build_narrative_state_tensor(record: dict[str, Any], rag_record: dict[str, Any]) -> NarrativeStateTensor:
    conflict = _clamp(float(record.get("mean_conflict_intensity") or 0.0))
    energy = _normalize_energy(float(record.get("mean_scene_energy_ratio") or 0.0))
    residue = _clamp(float(record.get("mean_motif_residue_score") or 0.0))
    curiosity = _clamp(float(record.get("mean_curiosity_gradient") or 0.0))
    dialogue = _clamp(float(record.get("mean_dialogue_ratio") or 0.0))
    retrieval = 1.0 if rag_record.get("scene_index_ready") and rag_record.get("chunk_index_ready") else 0.4
    dimensions = {
        "dramatic_pressure": round((conflict + energy) / 2.0, 6),
        "motif_continuity": residue,
        "reader_curiosity": curiosity,
        "dialogue_density": dialogue,
        "retrieval_grounding": retrieval,
    }
    lowest_dimension, lowest_score = min(dimensions.items(), key=lambda item: item[1])
    if lowest_score >= 0.55:
        status = "PASS"
    elif lowest_score >= 0.35:
        status = "WATCH"
    else:
        status = "REVIEW_REQUIRED"
    return NarrativeStateTensor(
        case_id=str(record["work_id"]),
        classification="metadata_only_corpus_tensor",
        dimensions=dimensions,
        status=status,
        lowest_dimension=lowest_dimension,
        lowest_score=round(lowest_score, 6),
        writer_review_required=status != "PASS",
        mutation_allowed=False,
        provider_call_required=False,
    )


def _build_tensor_signal(work_id: str, tensor: NarrativeStateTensor, feature_scene_count: int, created_at: str) -> FormulaSignalRecord:
    return FormulaSignalRecord(
        formula_signal_id=f"formula-signal:tensor:{work_id}",
        formula_id="formula:narrative_state_tensor",
        formula_group="Narrative State Tensor",
        source_record_ids=(f"canonical_work:{work_id}", f"learning_signal:{work_id}"),
        source_record_types=("CanonicalWorkRecord", "LearningSignalRecord"),
        input_field_names=("mean_conflict_intensity", "mean_scene_energy_ratio", "mean_motif_residue_score", "mean_curiosity_gradient", "mean_dialogue_ratio"),
        source_class_summary="metadata_only_corpus_records",
        rights_status_summary="user_provided_structured_analysis_db",
        output_signal_type="NARRATIVE_STATE_TENSOR_SIGNAL",
        output_signal_value_or_label=tensor.status,
        confidence=_confidence_from_count(feature_scene_count),
        explanation_summary=f"Derived from metadata-only aggregate features for {work_id}.",
        signal_type_label="CALCULATED_SIGNAL",
        critic_mapping_ref="critic:narrative_state_tensor",
        value_proof_mapping_ref="value_proof:arm_b_formula_guidance",
        writer_ide_panel_ref="writer_ide:right_panel:narrative_state_tensor",
        created_at=created_at,
        review_status="VALID_FOR_VALUE_PROOF_PREREGISTRATION",
    )


def _build_emotional_signal(work_id: str, record: dict[str, Any], feature_scene_count: int, created_at: str) -> FormulaSignalRecord:
    vector = EmotionalMomentumVector(
        tension=_clamp(float(record.get("mean_conflict_intensity") or 0.0)),
        sympathy=_clamp(float(record.get("mean_dialogue_ratio") or 0.0)),
        dread=_clamp(float(record.get("mean_curiosity_gradient") or 0.0)),
        catharsis=_clamp(float(record.get("mean_motif_residue_score") or 0.0)),
    ).clamp()
    label = f"intensity={vector.intensity():.4f}"
    return FormulaSignalRecord(
        formula_signal_id=f"formula-signal:emotion:{work_id}",
        formula_id="formula:emotional_momentum",
        formula_group="Emotional Momentum",
        source_record_ids=(f"learning_signal:{work_id}",),
        source_record_types=("LearningSignalRecord",),
        input_field_names=("mean_conflict_intensity", "mean_dialogue_ratio", "mean_curiosity_gradient", "mean_motif_residue_score"),
        source_class_summary="metadata_only_corpus_records",
        rights_status_summary="user_provided_structured_analysis_db",
        output_signal_type="EMOTIONAL_MOMENTUM_SIGNAL",
        output_signal_value_or_label=label,
        confidence=_confidence_from_count(feature_scene_count),
        explanation_summary=f"Emotion vector computed from aggregated conflict/dialogue/curiosity/residue features for {work_id}.",
        signal_type_label="CALCULATED_SIGNAL",
        critic_mapping_ref="critic:emotion",
        value_proof_mapping_ref="value_proof:arm_b_formula_guidance",
        writer_ide_panel_ref="writer_ide:right_panel:emotional_momentum",
        created_at=created_at,
        review_status="VALID_FOR_UI_WIRING",
    )


def _build_rag_signal(work_id: str, rag_record: dict[str, Any], created_at: str) -> FormulaSignalRecord:
    ready = bool(rag_record.get("scene_index_ready")) and bool(rag_record.get("chunk_index_ready"))
    return FormulaSignalRecord(
        formula_signal_id=f"formula-signal:rag:{work_id}",
        formula_id="formula:retrieval_grounding",
        formula_group="RAG/BM25/RRF retrieval fusion",
        source_record_ids=(f"rag_index:{work_id}",),
        source_record_types=("RagIndexRecord",),
        input_field_names=("scene_count", "chunk_count", "scene_index_ready", "chunk_index_ready"),
        source_class_summary="metadata_only_index_records",
        rights_status_summary="user_provided_structured_analysis_db",
        output_signal_type="AUTHORITY_WARNING_SIGNAL" if not ready else "NARRATIVE_FITNESS_COMPANION_SIGNAL",
        output_signal_value_or_label="RAG_READY" if ready else "RAG_PARTIAL",
        confidence=1.0 if ready else 0.5,
        explanation_summary=f"Retrieval readiness derived from canonical RAG registry for {work_id}.",
        signal_type_label="CALCULATED_SIGNAL",
        critic_mapping_ref="critic:retrieval_grounding",
        value_proof_mapping_ref="value_proof:retrieval_context_panel",
        writer_ide_panel_ref="writer_ide:left_panel:corpus_reference",
        created_at=created_at,
        review_status="VALID_FOR_UI_WIRING",
    )


def _confidence_from_count(feature_scene_count: int) -> float:
    if feature_scene_count >= 50:
        return 0.92
    if feature_scene_count >= 20:
        return 0.78
    if feature_scene_count >= 5:
        return 0.64
    if feature_scene_count >= 1:
        return 0.51
    return 0.25


def _normalize_energy(value: float) -> float:
    return _clamp(value / 4.0)


def _clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 6)


def _write_outputs(output_dir: Path, payload: dict[str, Any]) -> None:
    parts = payload["parts"]
    _write_json(output_dir / "formula_signal_registry.json", {"formula_signal_registry": parts["formula_signal_registry"]})
    _write_json(
        output_dir / "narrative_state_tensor_registry.json",
        {"narrative_state_tensor_registry": parts["narrative_state_tensor_registry"]},
    )
    _write_json(output_dir / "bridge_summary.json", parts["bridge_summary"])
    _write_json(output_dir / "corpus_formula_bridge_report.json", payload)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
