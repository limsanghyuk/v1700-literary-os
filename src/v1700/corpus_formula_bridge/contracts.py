from __future__ import annotations

from dataclasses import asdict, dataclass, field

from v1700.narrative_state_tensor.contracts import NarrativeStateTensor


@dataclass(frozen=True)
class FormulaSignalRecord:
    formula_signal_id: str
    formula_id: str
    formula_group: str
    source_record_ids: tuple[str, ...]
    source_record_types: tuple[str, ...]
    input_field_names: tuple[str, ...]
    source_class_summary: str
    rights_status_summary: str
    output_signal_type: str
    output_signal_value_or_label: str
    confidence: float
    explanation_summary: str
    signal_type_label: str
    critic_mapping_ref: str
    value_proof_mapping_ref: str
    writer_ide_panel_ref: str
    created_at: str
    review_status: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CorpusFormulaBridgeReport:
    corpus_id: str
    status: str
    formula_signals: tuple[FormulaSignalRecord, ...]
    narrative_state_tensors: tuple[NarrativeStateTensor, ...]
    issues: tuple[str, ...] = ()
    counters: dict[str, int] = field(default_factory=dict)
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["formula_signals"] = [record.to_dict() for record in self.formula_signals]
        payload["narrative_state_tensors"] = [record.to_dict() for record in self.narrative_state_tensors]
        return payload
