from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

REQUIRED_SIGNAL_FIELDS = (
    "formula_signal_id",
    "formula_id",
    "formula_group",
    "source_record_ids",
    "source_record_types",
    "input_field_names",
    "source_class_summary",
    "rights_status_summary",
    "output_signal_type",
    "output_signal_value_or_label",
    "confidence",
    "explanation_summary",
    "signal_type_label",
    "critic_mapping_ref",
    "value_proof_mapping_ref",
    "writer_ide_panel_ref",
    "created_at",
    "review_status",
)

ALLOWED_SIGNAL_TYPE_LABELS = {
    "PLACEHOLDER_SIGNAL",
    "MANUAL_REVIEW_SIGNAL",
    "FIXTURE_SIGNAL",
    "CALCULATED_SIGNAL",
}


def load_formula_signal_registry(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload.get("formula_signal_registry", payload)
    if not isinstance(records, list):
        return []
    return [record for record in records if isinstance(record, dict)]


def stable_signal_checksum(record: dict[str, Any]) -> str:
    payload = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def work_id_from_signal(record: dict[str, Any]) -> str:
    for source_id in record.get("source_record_ids", []):
        if not isinstance(source_id, str):
            continue
        if ":" not in source_id:
            continue
        return source_id.rsplit(":", 1)[-1]
    return ""


def validate_formula_signal_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    ids = [str(record.get("formula_signal_id", "")) for record in records]
    missing_required = [record.get("formula_signal_id", "<unknown>") for record in records if any(field not in record for field in REQUIRED_SIGNAL_FIELDS)]
    duplicate_ids = sorted({record_id for record_id in ids if record_id and ids.count(record_id) > 1})
    invalid_confidence = [
        record.get("formula_signal_id", "<unknown>")
        for record in records
        if not isinstance(record.get("confidence"), (int, float)) or not 0.0 <= float(record["confidence"]) <= 1.0
    ]
    invalid_signal_type_labels = [
        record.get("formula_signal_id", "<unknown>")
        for record in records
        if str(record.get("signal_type_label", "")) not in ALLOWED_SIGNAL_TYPE_LABELS
    ]
    missing_writer_panels = [
        record.get("formula_signal_id", "<unknown>")
        for record in records
        if not str(record.get("writer_ide_panel_ref", "")).strip()
    ]
    canonical_mutation_leaks = [
        record.get("formula_signal_id", "<unknown>")
        for record in records
        if bool(record.get("canonical_mutation_allowed"))
    ]

    issues: list[str] = []
    for name, values in {
        "missing_required_fields": missing_required,
        "duplicate_ids": duplicate_ids,
        "invalid_confidence": invalid_confidence,
        "invalid_signal_type_labels": invalid_signal_type_labels,
        "missing_writer_panels": missing_writer_panels,
        "canonical_mutation_leaks": canonical_mutation_leaks,
    }.items():
        if values:
            issues.append(f"{name}:{','.join(map(str, values))}")

    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "record_count": len(records),
        "required_fields": list(REQUIRED_SIGNAL_FIELDS),
        "duplicate_ids": duplicate_ids,
        "invalid_confidence": invalid_confidence,
        "invalid_signal_type_labels": invalid_signal_type_labels,
        "missing_writer_panels": missing_writer_panels,
        "canonical_mutation_leaks": canonical_mutation_leaks,
    }


def query_formula_signals(
    records: list[dict[str, Any]],
    *,
    work_id: str | None = None,
    formula_group: str | None = None,
    review_status: str | None = None,
    writer_ide_panel_ref: str | None = None,
    min_confidence: float | None = None,
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for record in records:
        if work_id and work_id_from_signal(record) != work_id:
            continue
        if formula_group and str(record.get("formula_group")) != formula_group:
            continue
        if review_status and str(record.get("review_status")) != review_status:
            continue
        if writer_ide_panel_ref and str(record.get("writer_ide_panel_ref")) != writer_ide_panel_ref:
            continue
        if min_confidence is not None and float(record.get("confidence") or 0.0) < min_confidence:
            continue
        result.append(record)
    return result
