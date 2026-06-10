# Corpus Adapter Rejected Record Contract

Status: contract draft
Created: 2026-06-10
Scope: rejected or quarantined records from future corpus ingestion adapter
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This contract defines how a future metadata-only corpus adapter must record rejected or quarantined source records.

Rejection must be explicit. The adapter must not silently drop unsafe, invalid, or unmappable records.

## 2. Required record

```text
CorpusAdapterRejectedRecord
```

## 3. Required fields

```text
rejected_record_id
source_bundle_ref
source_record_ref
source_record_type_guess
rejection_reason
rejection_severity
source_class
rights_status
provenance_ref
quarantine_required
suggested_remediation
created_at
review_status
```

## 4. Rejection reasons

```text
MISSING_SOURCE_CLASS
MISSING_RIGHTS_STATUS
MISSING_PROVENANCE_REF
UNKNOWN_SOURCE_CLASS
RESTRICTED_FULL_TEXT_DETECTED
SCHEMA_TARGET_NOT_FOUND
REQUIRED_FIELD_MISSING
FORMULA_SIGNAL_SOURCE_MISSING
UNMAPPABLE_FIELD_STRUCTURE
DUPLICATE_RECORD_CONFLICT
PAYLOAD_TYPE_CONTRADICTION
```

## 5. Rejection severity

```text
INFO
WARNING
ERROR
BLOCKING
```

## 6. Quarantine rule

The following must set:

```text
quarantine_required: true
```

- UNKNOWN_SOURCE_CLASS
- RESTRICTED_FULL_TEXT_DETECTED
- PAYLOAD_TYPE_CONTRADICTION
- MISSING_PROVENANCE_REF

## 7. Review statuses

```text
REJECTED
QUARANTINED
REMEDIATION_REQUIRED
REMEDIATED
SUPERSEDED
```

## 8. Required reports

Rejected records must be summarized in:

```text
ingestion_rejected_records.md
source_review_report.md
schema_validation_report.md
```

## 9. Blocking failures

- unsafe record silently dropped
- rejected record lacks reason
- restricted full-text record not quarantined
- unknown source not quarantined
- provenance removed
- rejected record later used without remediation record

## 10. Final decision

Every rejected or quarantined adapter input must be traceable, reviewable, and excluded from downstream formula mapping until remediated.
