#!/usr/bin/env python3
"""Option B fixture validator scaffold.

This validator is intentionally narrow in scope:
- validates the Option B fixture bundle only;
- emits an explicit fail-closed result;
- does not open Page18 implementation;
- does not create Stage243+;
- does not perform LLM generation, coefficient learning, or canonical story mutation.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence

VALIDATOR_VERSION = "0.1.0"

FIXTURE_PATHS: Mapping[str, str] = {
    "mapping_table": "fixtures/corpus_adapter_mapping/mapping_table.json",
    "corpus": "fixtures/narrative_corpus_minimum/fixture.json",
    "formula_catalog": "fixtures/formula_catalog_minimum/fixture.json",
    "formula_signal": "fixtures/formula_signal_minimum/fixture.json",
    "rejected_records": "fixtures/corpus_adapter_rejected_records/rejected_records.json",
}

REPORT_REFS: Mapping[str, str] = {
    "source_review_report_ref": "fixtures/option_b_validation/source_review_report.md",
    "schema_validation_report_ref": "fixtures/option_b_validation/schema_validation_report.md",
    "mapping_report_ref": "fixtures/option_b_validation/corpus_adapter_mapping_report.md",
    "formula_signal_validation_report_ref": "fixtures/option_b_validation/formula_signal_validation_report.md",
    "rejected_records_report_ref": "fixtures/option_b_validation/rejected_records_report.md",
}

ALLOWED_POSITIVE_SOURCE_CLASSES = {
    "METADATA_ONLY_ANALYSIS_RECORD",
    "USER_PROVIDED_STRUCTURED_ANALYSIS_DB",
    "USER_OWNED_SOURCE",
    "PUBLIC_DOMAIN_SOURCE",
    "LICENSED_SOURCE",
}

ALLOWED_POSITIVE_RIGHTS_STATUS = {
    "METADATA_ONLY",
    "USER_OWNED",
    "PUBLIC_DOMAIN",
    "LICENSED",
}

ALLOWED_RECORD_TYPES = {
    "WorkRecord",
    "DramaEntryRecord",
    "CorePhilosophyRecord",
    "LorebookRecord",
    "CharacterRecord",
    "KeyObjectRecord",
    "CausalityMatrixRecord",
    "EpisodeOrChapterRecord",
    "SceneBlueprintRecord",
    "DialogueFunctionRecord",
    "StyleModuleRecord",
    "CriticThresholdRecord",
    "AudienceSignalRecord",
    "GenreEngineRecord",
    "RelationshipGraphRecord",
    "FormulaSignalRecord",
}

REQUIRED_CORPUS_RECORD_TYPES = {
    "WorkRecord",
    "DramaEntryRecord",
    "CorePhilosophyRecord",
    "RelationshipGraphRecord",
    "DialogueFunctionRecord",
    "CriticThresholdRecord",
}

REQUIRED_FORMULA_IDS = {
    "formula_narrative_state_tensor_v0_1",
    "formula_emotional_momentum_v0_1",
    "formula_character_interaction_matrix_v0_1",
    "formula_drse_v0_1",
    "formula_narrative_fitness_score_v0_1",
}

REQUIRED_SIGNAL_TYPES = {
    "NARRATIVE_STATE_TENSOR_SIGNAL",
    "EMOTIONAL_MOMENTUM_SIGNAL",
    "CHARACTER_INTERACTION_SIGNAL",
    "CAUSALITY_TRANSITION_SIGNAL",
    "NARRATIVE_FITNESS_COMPANION_SIGNAL",
}

REQUIRED_REJECTION_REASONS = {
    "MISSING_SOURCE_CLASS",
    "MISSING_RIGHTS_STATUS",
    "MISSING_PROVENANCE_REF",
    "UNKNOWN_SOURCE_CLASS",
    "RESTRICTED_FULL_TEXT_DETECTED",
    "SCHEMA_TARGET_NOT_FOUND",
    "REQUIRED_FIELD_MISSING",
    "UNMAPPABLE_FIELD_STRUCTURE",
}

QUARANTINE_REQUIRED_REASONS = {
    "UNKNOWN_SOURCE_CLASS",
    "RESTRICTED_FULL_TEXT_DETECTED",
    "PAYLOAD_TYPE_CONTRADICTION",
    "MISSING_PROVENANCE_REF",
}

FULL_TEXT_RISK_KEYS = {
    "full_text",
    "raw_text",
    "script_text",
    "book_chapter",
    "chapter_text",
    "subtitle",
    "subtitles",
    "transcript",
    "raw_transcript",
    "dialogue_lines",
}


@dataclass
class Finding:
    module: str
    severity: str
    path: str
    message: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "module": self.module,
            "severity": self.severity,
            "path": self.path,
            "message": self.message,
        }


@dataclass
class ModuleResult:
    module_name: str
    checked_file_refs: List[str] = field(default_factory=list)
    warnings: List[Finding] = field(default_factory=list)
    blocking_failures: List[Finding] = field(default_factory=list)

    @property
    def module_status(self) -> str:
        if self.blocking_failures:
            return "BLOCKED"
        if self.warnings:
            return "PASS_WITH_WARNINGS"
        return "PASS"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module_name": self.module_name,
            "module_status": self.module_status,
            "checked_file_refs": self.checked_file_refs,
            "warning_refs": [finding.to_dict() for finding in self.warnings],
            "blocking_failure_refs": [finding.to_dict() for finding in self.blocking_failures],
            "summary": f"{self.module_name}: {self.module_status}",
        }


class OptionBFixtureValidator:
    """Deterministic fail-closed validator for the Option B fixture bundle."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.loaded: MutableMapping[str, Any] = {}
        self.module_results: List[ModuleResult] = []

    def validate(self) -> Dict[str, Any]:
        started_at = _utc_now()
        self.module_results = []
        self.loaded = {}

        self.module_results.append(self._validate_json_parse())
        if self._has_blocking_failures():
            return self._build_result(started_at)

        self.module_results.append(self._validate_mapping_table())
        self.module_results.append(self._validate_source_policy())
        self.module_results.append(self._validate_schema())
        self.module_results.append(self._validate_formula_catalog())
        self.module_results.append(self._validate_formula_signals())
        self.module_results.append(self._validate_rejected_records())
        return self._build_result(started_at)

    def _validate_json_parse(self) -> ModuleResult:
        module = ModuleResult("JSON Parse Validator", checked_file_refs=list(FIXTURE_PATHS.values()))
        for key, relative_path in FIXTURE_PATHS.items():
            path = self.repo_root / relative_path
            if not path.exists():
                module.blocking_failures.append(
                    Finding(module.module_name, "BLOCKING", relative_path, "fixture file is missing")
                )
                continue
            try:
                self.loaded[key] = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                module.blocking_failures.append(
                    Finding(module.module_name, "BLOCKING", relative_path, f"invalid JSON: {exc}")
                )
        return module

    def _validate_mapping_table(self) -> ModuleResult:
        relative_path = FIXTURE_PATHS["mapping_table"]
        module = ModuleResult("Mapping Table Validator", checked_file_refs=[relative_path])
        table = self.loaded.get("mapping_table", {})
        _require_keys(
            module,
            table,
            relative_path,
            ["mapping_table_id", "adapter_version", "source_policy_ref", "schema_ref", "mappings"],
        )
        mappings = _as_list(table.get("mappings"))
        if not mappings:
            module.blocking_failures.append(
                Finding(module.module_name, "BLOCKING", relative_path, "mappings array is empty or missing")
            )
        for index, row in enumerate(mappings):
            row_path = f"{relative_path}#mappings[{index}]"
            _require_keys(
                module,
                row,
                row_path,
                [
                    "source_field_name",
                    "target_record_type",
                    "target_field_name",
                    "transformation_rule",
                    "source_policy_requirement",
                ],
            )
            target_type = row.get("target_record_type")
            if target_type not in ALLOWED_RECORD_TYPES:
                module.blocking_failures.append(
                    Finding(module.module_name, "BLOCKING", row_path, f"unsupported target_record_type: {target_type}")
                )
            note_values = " ".join(str(v).lower() for v in row.values())
            if "restricted full text" in note_values and "no mapping row permits" not in note_values:
                # Warning only: the row can mention the phrase as a prohibition.
                module.warnings.append(
                    Finding(module.module_name, "WARNING", row_path, "mapping row mentions restricted full text; confirm it is a prohibition")
                )
        return module

    def _validate_source_policy(self) -> ModuleResult:
        module = ModuleResult(
            "Source Policy Validator",
            checked_file_refs=[FIXTURE_PATHS["corpus"], FIXTURE_PATHS["formula_signal"], FIXTURE_PATHS["rejected_records"]],
        )
        corpus = self.loaded.get("corpus", {})
        for index, record in enumerate(_as_list(corpus.get("records"))):
            record_path = f"{FIXTURE_PATHS['corpus']}#records[{index}]"
            _require_keys(module, record, record_path, ["source_class", "rights_status", "provenance_ref"])
            if record.get("source_class") not in ALLOWED_POSITIVE_SOURCE_CLASSES:
                module.blocking_failures.append(
                    Finding(module.module_name, "BLOCKING", record_path, f"invalid positive source_class: {record.get('source_class')}")
                )
            if record.get("rights_status") not in ALLOWED_POSITIVE_RIGHTS_STATUS:
                module.blocking_failures.append(
                    Finding(module.module_name, "BLOCKING", record_path, f"invalid positive rights_status: {record.get('rights_status')}")
                )
            if _contains_full_text_risk(record):
                module.blocking_failures.append(
                    Finding(module.module_name, "BLOCKING", record_path, "accepted corpus record contains full-text risk key")
                )

        signals = self.loaded.get("formula_signal", {})
        for index, signal in enumerate(_as_list(signals.get("formula_signal_records"))):
            signal_path = f"{FIXTURE_PATHS['formula_signal']}#formula_signal_records[{index}]"
            if signal.get("source_class_summary") not in ALLOWED_POSITIVE_SOURCE_CLASSES:
                module.blocking_failures.append(
                    Finding(module.module_name, "BLOCKING", signal_path, "signal has invalid source_class_summary")
                )
            if signal.get("rights_status_summary") not in ALLOWED_POSITIVE_RIGHTS_STATUS:
                module.blocking_failures.append(
                    Finding(module.module_name, "BLOCKING", signal_path, "signal has invalid rights_status_summary")
                )

        rejected = self.loaded.get("rejected_records", {})
        for index, record in enumerate(_as_list(rejected.get("rejected_records"))):
            record_path = f"{FIXTURE_PATHS['rejected_records']}#rejected_records[{index}]"
            reason = record.get("rejection_reason")
            if reason in QUARANTINE_REQUIRED_REASONS and record.get("quarantine_required") is not True:
                module.blocking_failures.append(
                    Finding(module.module_name, "BLOCKING", record_path, f"{reason} must be quarantined")
                )
        return module

    def _validate_schema(self) -> ModuleResult:
        relative_path = FIXTURE_PATHS["corpus"]
        module = ModuleResult("Schema Validator", checked_file_refs=[relative_path])
        corpus = self.loaded.get("corpus", {})
        _require_keys(module, corpus, relative_path, ["fixture_id", "schema_ref", "source_policy_ref", "records"])
        records = _as_list(corpus.get("records"))
        record_types = [record.get("record_type") for record in records]
        record_ids = {record.get("record_id") for record in records if record.get("record_id")}

        for required_type in REQUIRED_CORPUS_RECORD_TYPES:
            if required_type not in record_types:
                module.blocking_failures.append(
                    Finding(module.module_name, "BLOCKING", relative_path, f"missing required record type: {required_type}")
                )
        if record_types.count("CharacterRecord") < 2:
            module.blocking_failures.append(
                Finding(module.module_name, "BLOCKING", relative_path, "at least two CharacterRecord entries are required")
            )
        if record_types.count("SceneBlueprintRecord") < 2:
            module.blocking_failures.append(
                Finding(module.module_name, "BLOCKING", relative_path, "at least two SceneBlueprintRecord entries are required")
            )
        if record_types.count("CausalityMatrixRecord") < 2:
            module.blocking_failures.append(
                Finding(module.module_name, "BLOCKING", relative_path, "at least two CausalityMatrixRecord entries are required")
            )

        for index, record in enumerate(records):
            record_path = f"{relative_path}#records[{index}]"
            _require_keys(
                module,
                record,
                record_path,
                ["record_id", "record_type", "source_class", "rights_status", "provenance_ref", "review_status"],
            )
            if record.get("record_type") not in ALLOWED_RECORD_TYPES:
                module.blocking_failures.append(
                    Finding(module.module_name, "BLOCKING", record_path, f"unsupported record_type: {record.get('record_type')}")
                )
            if record.get("record_type") == "SceneBlueprintRecord":
                _require_keys(
                    module,
                    record,
                    record_path,
                    ["conflict_type", "emotional_start_tag", "emotional_end_tag", "tension_delta_label"],
                )
            if record.get("record_type") == "CausalityMatrixRecord":
                _require_keys(
                    module,
                    record,
                    record_path,
                    ["trigger_summary", "resolution_summary", "residue_summary"],
                )
            if record.get("record_type") == "RelationshipGraphRecord":
                for ref in _as_list(record.get("node_refs")):
                    if ref not in record_ids:
                        module.blocking_failures.append(
                            Finding(module.module_name, "BLOCKING", record_path, f"node_ref does not resolve: {ref}")
                        )
        return module

    def _validate_formula_catalog(self) -> ModuleResult:
        relative_path = FIXTURE_PATHS["formula_catalog"]
        module = ModuleResult("Formula Catalog Validator", checked_file_refs=[relative_path])
        catalog = self.loaded.get("formula_catalog", {})
        _require_keys(module, catalog, relative_path, ["fixture_id", "catalog_contract_ref", "formula_catalog_records"])
        records = _as_list(catalog.get("formula_catalog_records"))
        formula_ids = {record.get("formula_id") for record in records}
        missing = REQUIRED_FORMULA_IDS - formula_ids
        for formula_id in sorted(missing):
            module.blocking_failures.append(
                Finding(module.module_name, "BLOCKING", relative_path, f"missing required formula: {formula_id}")
            )
        for index, record in enumerate(records):
            record_path = f"{relative_path}#formula_catalog_records[{index}]"
            _require_keys(
                module,
                record,
                record_path,
                ["formula_id", "formula_group", "lineage_ref", "input_schema_refs", "output_schema_refs", "boundary_rule_refs"],
            )
            if record.get("lineage_ref") == "UNRESOLVED_LINEAGE":
                module.blocking_failures.append(
                    Finding(module.module_name, "BLOCKING", record_path, "UNRESOLVED_LINEAGE cannot be used in fixture catalog")
                )
        return module

    def _validate_formula_signals(self) -> ModuleResult:
        relative_path = FIXTURE_PATHS["formula_signal"]
        module = ModuleResult("Formula Signal Validator", checked_file_refs=[relative_path])
        signal_fixture = self.loaded.get("formula_signal", {})
        _require_keys(module, signal_fixture, relative_path, ["fixture_id", "formula_signal_records"])

        corpus_ids = {
            record.get("record_id")
            for record in _as_list(self.loaded.get("corpus", {}).get("records"))
            if record.get("record_id")
        }
        formula_ids = {
            record.get("formula_id")
            for record in _as_list(self.loaded.get("formula_catalog", {}).get("formula_catalog_records"))
            if record.get("formula_id")
        }
        signal_types = set()
        for index, signal in enumerate(_as_list(signal_fixture.get("formula_signal_records"))):
            signal_path = f"{relative_path}#formula_signal_records[{index}]"
            _require_keys(
                module,
                signal,
                signal_path,
                ["formula_signal_id", "formula_id", "formula_group", "source_record_ids", "input_field_names", "signal_type_label"],
            )
            formula_id = signal.get("formula_id")
            if formula_id not in formula_ids:
                module.blocking_failures.append(
                    Finding(module.module_name, "BLOCKING", signal_path, f"formula_id does not resolve: {formula_id}")
                )
            for source_record_id in _as_list(signal.get("source_record_ids")):
                if source_record_id not in corpus_ids:
                    module.blocking_failures.append(
                        Finding(module.module_name, "BLOCKING", signal_path, f"source_record_id does not resolve: {source_record_id}")
                    )
            output_type = signal.get("output_signal_type")
            if output_type:
                signal_types.add(output_type)
            if signal.get("signal_type_label") == "CALCULATED_SIGNAL":
                module.warnings.append(
                    Finding(module.module_name, "WARNING", signal_path, "CALCULATED_SIGNAL requires runtime proof; fixture should avoid proof overclaiming")
                )
            explanation = str(signal.get("explanation_summary", "")).lower()
            if "proof" in explanation and "not performance proof" not in explanation:
                module.warnings.append(
                    Finding(module.module_name, "WARNING", signal_path, "signal explanation mentions proof; confirm it is non-proof fixture language")
                )
        missing_signal_types = REQUIRED_SIGNAL_TYPES - signal_types
        for signal_type in sorted(missing_signal_types):
            module.blocking_failures.append(
                Finding(module.module_name, "BLOCKING", relative_path, f"missing required signal type: {signal_type}")
            )
        return module

    def _validate_rejected_records(self) -> ModuleResult:
        relative_path = FIXTURE_PATHS["rejected_records"]
        module = ModuleResult("Rejected Records Validator", checked_file_refs=[relative_path])
        rejected = self.loaded.get("rejected_records", {})
        _require_keys(module, rejected, relative_path, ["fixture_id", "contract_ref", "source_policy_ref", "rejected_records"])
        records = _as_list(rejected.get("rejected_records"))
        reasons = {record.get("rejection_reason") for record in records}
        missing = REQUIRED_REJECTION_REASONS - reasons
        for reason in sorted(missing):
            module.blocking_failures.append(
                Finding(module.module_name, "BLOCKING", relative_path, f"missing rejection example: {reason}")
            )
        signal_sources = {
            source_id
            for signal in _as_list(self.loaded.get("formula_signal", {}).get("formula_signal_records"))
            for source_id in _as_list(signal.get("source_record_ids"))
        }
        for index, record in enumerate(records):
            record_path = f"{relative_path}#rejected_records[{index}]"
            _require_keys(
                module,
                record,
                record_path,
                ["rejected_record_id", "rejection_reason", "rejection_severity", "source_class", "rights_status", "provenance_ref", "quarantine_required"],
            )
            reason = record.get("rejection_reason")
            if reason in QUARANTINE_REQUIRED_REASONS and record.get("quarantine_required") is not True:
                module.blocking_failures.append(
                    Finding(module.module_name, "BLOCKING", record_path, f"{reason} must be quarantined")
                )
            if record.get("source_record_ref") in signal_sources:
                module.blocking_failures.append(
                    Finding(module.module_name, "BLOCKING", record_path, "rejected record is used by formula signal fixture")
                )
        return module

    def _has_blocking_failures(self) -> bool:
        return any(result.blocking_failures for result in self.module_results)

    def _build_result(self, started_at: str) -> Dict[str, Any]:
        completed_at = _utc_now()
        warnings = [finding for result in self.module_results for finding in result.warnings]
        failures = [finding for result in self.module_results for finding in result.blocking_failures]
        if failures:
            overall_status = "BLOCKED"
            downstream_readiness = "NOT_READY"
            acceptance_status = "BLOCKED"
        elif warnings:
            overall_status = "PASS_WITH_WARNINGS"
            downstream_readiness = "READY_FOR_SCHEMA_WIRING"
            acceptance_status = "ACCEPTED_WITH_WARNINGS"
        else:
            overall_status = "PASS"
            downstream_readiness = "READY_FOR_FORMULA_SIGNAL_MAPPING"
            acceptance_status = "ACCEPTED_FOR_FORMULA_SIGNAL_MAPPING"

        return {
            "result_id": f"option_b_fixture_validator_result_{completed_at}",
            "validator_version": VALIDATOR_VERSION,
            "fixture_bundle_refs": dict(FIXTURE_PATHS),
            **dict(REPORT_REFS),
            "validation_started_at": started_at,
            "validation_completed_at": completed_at,
            "overall_status": overall_status,
            "module_results": [result.to_dict() for result in self.module_results],
            "warning_count": len(warnings),
            "blocking_failure_count": len(failures),
            "downstream_readiness": downstream_readiness,
            "acceptance_status": acceptance_status,
            "created_at": completed_at,
            "review_status": "GENERATED_BY_SCAFFOLD",
        }


def _require_keys(module: ModuleResult, obj: Any, path: str, keys: Iterable[str]) -> None:
    if not isinstance(obj, Mapping):
        module.blocking_failures.append(Finding(module.module_name, "BLOCKING", path, "expected object"))
        return
    for key in keys:
        if key not in obj or obj.get(key) in (None, ""):
            module.blocking_failures.append(Finding(module.module_name, "BLOCKING", path, f"missing required field: {key}"))


def _as_list(value: Any) -> List[Any]:
    if isinstance(value, list):
        return value
    return []


def _contains_full_text_risk(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).lower() in FULL_TEXT_RISK_KEYS:
                return True
            if _contains_full_text_risk(child):
                return True
    elif isinstance(value, list):
        return any(_contains_full_text_risk(child) for child in value)
    return False


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Option B fixture bundle.")
    parser.add_argument("--repo-root", default=".", help="Repository root containing fixtures/ and docs/.")
    parser.add_argument("--output", default="", help="Optional JSON result output path.")
    args = parser.parse_args(argv)

    validator = OptionBFixtureValidator(Path(args.repo_root).resolve())
    result = validator.validate()
    output_text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output_text + "\n", encoding="utf-8")
    else:
        print(output_text)
    return 0 if result["overall_status"] in {"PASS", "PASS_WITH_WARNINGS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
