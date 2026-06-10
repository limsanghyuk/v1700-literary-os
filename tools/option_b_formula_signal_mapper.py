#!/usr/bin/env python3
"""Option B formula signal mapper scaffold.

This tool consumes the accepted Option B fixture bundle and emits a formula-signal
mapping result. It is intentionally narrow in scope:

- no Page18 implementation;
- no Stage243+ creation;
- no formula runtime calculation;
- no Value Proof claim;
- no LearnableCritic coefficient mutation;
- no canonical story mutation.

The mapper links FormulaSignalRecord entries to their FormulaCatalogRecord and
CorpusFixtureRecord sources, preserving advisory-only semantics.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence

MAPPER_VERSION = "0.1.0"

DEFAULT_PATHS: Mapping[str, str] = {
    "validator_result": "fixtures/option_b_validation/validator_result.json",
    "corpus": "fixtures/narrative_corpus_minimum/fixture.json",
    "formula_catalog": "fixtures/formula_catalog_minimum/fixture.json",
    "formula_signal": "fixtures/formula_signal_minimum/fixture.json",
}

ALLOWED_ACCEPTANCE_STATUS = {
    "ACCEPTED_FOR_FORMULA_SIGNAL_MAPPING",
    "ACCEPTED_WITH_WARNINGS",
}

ALLOWED_DOWNSTREAM_READINESS = {
    "READY_FOR_FORMULA_SIGNAL_MAPPING",
}

ADVISORY_SIGNAL_LABELS = {
    "PLACEHOLDER_SIGNAL",
    "MANUAL_REVIEW_SIGNAL",
    "FIXTURE_SIGNAL",
}


@dataclass
class MappingFinding:
    severity: str
    path: str
    message: str

    def to_dict(self) -> Dict[str, str]:
        return {"severity": self.severity, "path": self.path, "message": self.message}


@dataclass
class FormulaSignalMapping:
    formula_signal_id: str
    formula_id: str
    formula_group: str
    formula_name: str
    output_signal_type: str
    output_signal_value_or_label: str
    signal_type_label: str
    source_record_ids: List[str]
    source_record_types: List[str]
    source_record_summaries: List[Dict[str, Any]]
    advisory_only: bool
    value_proof_status: str
    learnable_critic_status: str
    writer_ide_status: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "formula_signal_id": self.formula_signal_id,
            "formula_id": self.formula_id,
            "formula_group": self.formula_group,
            "formula_name": self.formula_name,
            "output_signal_type": self.output_signal_type,
            "output_signal_value_or_label": self.output_signal_value_or_label,
            "signal_type_label": self.signal_type_label,
            "source_record_ids": self.source_record_ids,
            "source_record_types": self.source_record_types,
            "source_record_summaries": self.source_record_summaries,
            "advisory_only": self.advisory_only,
            "value_proof_status": self.value_proof_status,
            "learnable_critic_status": self.learnable_critic_status,
            "writer_ide_status": self.writer_ide_status,
        }


@dataclass
class MappingContext:
    validator_result: Mapping[str, Any]
    corpus: Mapping[str, Any]
    formula_catalog: Mapping[str, Any]
    formula_signal: Mapping[str, Any]
    corpus_by_id: Dict[str, Mapping[str, Any]] = field(default_factory=dict)
    formulas_by_id: Dict[str, Mapping[str, Any]] = field(default_factory=dict)


class OptionBFormulaSignalMapper:
    """Scaffold mapper for accepted Option B FormulaSignalRecord fixtures."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.findings: List[MappingFinding] = []

    def map_signals(self) -> Dict[str, Any]:
        started_at = _utc_now()
        self.findings = []
        context = self._load_context()
        if self.findings:
            return self._build_result(started_at, [], context)

        self._validate_validator_gate(context.validator_result)
        self._index_context(context)
        mappings = self._build_mappings(context) if not self.findings else []
        return self._build_result(started_at, mappings, context)

    def _load_context(self) -> MappingContext:
        payloads: MutableMapping[str, Mapping[str, Any]] = {}
        for key, relative_path in DEFAULT_PATHS.items():
            path = self.repo_root / relative_path
            if not path.exists():
                self.findings.append(MappingFinding("BLOCKING", relative_path, "required input file is missing"))
                payloads[key] = {}
                continue
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
                if not isinstance(raw, Mapping):
                    self.findings.append(MappingFinding("BLOCKING", relative_path, "expected JSON object"))
                    payloads[key] = {}
                else:
                    payloads[key] = raw
            except json.JSONDecodeError as exc:
                self.findings.append(MappingFinding("BLOCKING", relative_path, f"invalid JSON: {exc}"))
                payloads[key] = {}

        return MappingContext(
            validator_result=payloads.get("validator_result", {}),
            corpus=payloads.get("corpus", {}),
            formula_catalog=payloads.get("formula_catalog", {}),
            formula_signal=payloads.get("formula_signal", {}),
        )

    def _validate_validator_gate(self, validator_result: Mapping[str, Any]) -> None:
        status = validator_result.get("overall_status")
        acceptance = validator_result.get("acceptance_status")
        readiness = validator_result.get("downstream_readiness")
        blocking_count = validator_result.get("blocking_failure_count")

        if status not in {"PASS", "PASS_WITH_WARNINGS"}:
            self.findings.append(MappingFinding("BLOCKING", DEFAULT_PATHS["validator_result"], f"validator status not accepted: {status}"))
        if acceptance not in ALLOWED_ACCEPTANCE_STATUS:
            self.findings.append(MappingFinding("BLOCKING", DEFAULT_PATHS["validator_result"], f"acceptance status not mapping-ready: {acceptance}"))
        if readiness not in ALLOWED_DOWNSTREAM_READINESS:
            self.findings.append(MappingFinding("BLOCKING", DEFAULT_PATHS["validator_result"], f"downstream readiness not mapping-ready: {readiness}"))
        if blocking_count != 0:
            self.findings.append(MappingFinding("BLOCKING", DEFAULT_PATHS["validator_result"], "validator_result has blocking failures"))

    def _index_context(self, context: MappingContext) -> None:
        records = _as_list(context.corpus.get("records"))
        context.corpus_by_id = {
            str(record.get("record_id")): record
            for record in records
            if isinstance(record, Mapping) and record.get("record_id")
        }
        formulas = _as_list(context.formula_catalog.get("formula_catalog_records"))
        context.formulas_by_id = {
            str(record.get("formula_id")): record
            for record in formulas
            if isinstance(record, Mapping) and record.get("formula_id")
        }

    def _build_mappings(self, context: MappingContext) -> List[FormulaSignalMapping]:
        mappings: List[FormulaSignalMapping] = []
        signals = _as_list(context.formula_signal.get("formula_signal_records"))
        if not signals:
            self.findings.append(MappingFinding("BLOCKING", DEFAULT_PATHS["formula_signal"], "formula_signal_records is empty or missing"))
            return []

        for index, signal in enumerate(signals):
            signal_path = f"{DEFAULT_PATHS['formula_signal']}#formula_signal_records[{index}]"
            if not isinstance(signal, Mapping):
                self.findings.append(MappingFinding("BLOCKING", signal_path, "signal entry is not an object"))
                continue

            formula_id = str(signal.get("formula_id", ""))
            formula = context.formulas_by_id.get(formula_id)
            if formula is None:
                self.findings.append(MappingFinding("BLOCKING", signal_path, f"missing formula reference: {formula_id}"))
                continue

            source_ids = [str(value) for value in _as_list(signal.get("source_record_ids"))]
            source_records: List[Mapping[str, Any]] = []
            for source_id in source_ids:
                source = context.corpus_by_id.get(source_id)
                if source is None:
                    self.findings.append(MappingFinding("BLOCKING", signal_path, f"missing source record reference: {source_id}"))
                else:
                    source_records.append(source)

            signal_type_label = str(signal.get("signal_type_label", ""))
            if signal_type_label not in ADVISORY_SIGNAL_LABELS:
                self.findings.append(MappingFinding("BLOCKING", signal_path, f"non-advisory signal label is not allowed in scaffold: {signal_type_label}"))
                continue

            if len(source_records) != len(source_ids):
                continue

            mappings.append(
                FormulaSignalMapping(
                    formula_signal_id=str(signal.get("formula_signal_id", "")),
                    formula_id=formula_id,
                    formula_group=str(signal.get("formula_group", "")),
                    formula_name=str(formula.get("formula_name", "")),
                    output_signal_type=str(signal.get("output_signal_type", "")),
                    output_signal_value_or_label=str(signal.get("output_signal_value_or_label", "")),
                    signal_type_label=signal_type_label,
                    source_record_ids=source_ids,
                    source_record_types=[str(source.get("record_type", "")) for source in source_records],
                    source_record_summaries=[_summarize_source_record(source) for source in source_records],
                    advisory_only=True,
                    value_proof_status="PREREGISTRATION_REQUIRED_NOT_PROOF",
                    learnable_critic_status="AUDIT_REQUIRED_NO_COEFFICIENT_UPDATE",
                    writer_ide_status="ADVISORY_PANEL_ONLY",
                )
            )
        return mappings

    def _build_result(
        self,
        started_at: str,
        mappings: List[FormulaSignalMapping],
        context: MappingContext,
    ) -> Dict[str, Any]:
        completed_at = _utc_now()
        blocking = [finding for finding in self.findings if finding.severity == "BLOCKING"]
        warnings = [finding for finding in self.findings if finding.severity == "WARNING"]
        if blocking:
            overall_status = "BLOCKED"
            downstream_status = "NOT_READY"
            acceptance_status = "BLOCKED"
        elif warnings:
            overall_status = "PASS_WITH_WARNINGS"
            downstream_status = "READY_FOR_WRITER_IDE_STATIC_FLOW"
            acceptance_status = "ACCEPTED_WITH_WARNINGS"
        else:
            overall_status = "PASS"
            downstream_status = "READY_FOR_WRITER_IDE_STATIC_FLOW"
            acceptance_status = "ACCEPTED_FOR_WRITER_IDE_STATIC_FLOW"

        return {
            "result_id": f"option_b_formula_signal_mapping_result_{completed_at}",
            "mapper_version": MAPPER_VERSION,
            "validator_result_ref": DEFAULT_PATHS["validator_result"],
            "validator_acceptance_status": context.validator_result.get("acceptance_status"),
            "input_refs": dict(DEFAULT_PATHS),
            "overall_status": overall_status,
            "acceptance_status": acceptance_status,
            "downstream_status": downstream_status,
            "mapping_count": len(mappings),
            "warning_count": len(warnings),
            "blocking_failure_count": len(blocking),
            "warnings": [finding.to_dict() for finding in warnings],
            "blocking_failures": [finding.to_dict() for finding in blocking],
            "formula_signal_mappings": [mapping.to_dict() for mapping in mappings],
            "value_proof_status": "NOT_PROOF_PREREGISTRATION_REQUIRED",
            "learnable_critic_status": "NO_COEFFICIENT_UPDATE_AUDIT_REQUIRED",
            "canonical_mutation_status": "NO_CANONICAL_MUTATION",
            "page18_status": "NOT_OPENED",
            "stage243_status": "NOT_CREATED",
            "validation_started_at": started_at,
            "validation_completed_at": completed_at,
            "created_at": completed_at,
            "review_status": "GENERATED_BY_SCAFFOLD",
        }


def _summarize_source_record(source: Mapping[str, Any]) -> Dict[str, Any]:
    summary_keys = [
        "record_id",
        "record_type",
        "scene_function",
        "conflict_type",
        "tension_delta_label",
        "emotional_start_tag",
        "emotional_end_tag",
        "relationship_type",
        "pressure_level",
        "trust_level",
        "conflict_level",
        "trigger_summary",
        "resolution_summary",
        "residue_summary",
        "minimum_causality_clarity",
        "minimum_emotional_legibility",
    ]
    return {key: source.get(key) for key in summary_keys if key in source}


def _as_list(value: Any) -> List[Any]:
    if isinstance(value, list):
        return value
    return []


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Map Option B formula signals to corpus and formula records.")
    parser.add_argument("--repo-root", default=".", help="Repository root containing fixtures/ and docs/.")
    parser.add_argument("--output", default="", help="Optional JSON mapping result output path.")
    args = parser.parse_args(argv)

    mapper = OptionBFormulaSignalMapper(Path(args.repo_root).resolve())
    result = mapper.map_signals()
    output_text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output_text + "\n", encoding="utf-8")
    else:
        print(output_text)
    return 0 if result["overall_status"] in {"PASS", "PASS_WITH_WARNINGS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
