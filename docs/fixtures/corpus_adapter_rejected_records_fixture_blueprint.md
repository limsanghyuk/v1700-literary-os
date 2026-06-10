# Corpus Adapter Rejected Records Fixture Blueprint

Status: blueprint draft
Created: 2026-06-10
Scope: future rejected records fixture, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint defines the structure of a future rejected records fixture for the corpus adapter.

Rejected records must be explicit, traceable, and excluded from downstream corpus, formula, Value Proof, LearnableCritic, Writer IDE, and multi-agent use until remediated.

## 2. Future path

```text
fixtures/corpus_adapter_rejected_records/rejected_records.json
fixtures/corpus_adapter_rejected_records/rejected_records.md
```

## 3. Top-level JSON shape

```json
{
  "fixture_id": "corpus_adapter_rejected_records_v0_1",
  "fixture_version": "0.1",
  "contract_ref": "docs/contracts/corpus_adapter_rejected_record_contract.md",
  "source_policy_ref": "docs/policies/narrative_corpus_source_policy.md",
  "review_status": "DRAFT",
  "rejected_records": []
}
```

## 4. Rejected record example

```json
{
  "rejected_record_id": "rejected_001",
  "source_bundle_ref": "source_bundle:future",
  "source_record_ref": "source_record:unknown_001",
  "source_record_type_guess": "UnknownRecord",
  "rejection_reason": "UNKNOWN_SOURCE_CLASS",
  "rejection_severity": "BLOCKING",
  "source_class": "UNKNOWN_OR_UNRESOLVED_SOURCE",
  "rights_status": "UNKNOWN",
  "provenance_ref": "missing",
  "quarantine_required": true,
  "suggested_remediation": "provide source_class, rights_status, and provenance_ref before remapping",
  "created_at": "2026-06-10T00:00:00Z",
  "review_status": "QUARANTINED"
}
```

## 5. Required rejected record fields

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

## 6. Required sample rejection categories

The future fixture should include at least one example for:

```text
MISSING_SOURCE_CLASS
MISSING_RIGHTS_STATUS
MISSING_PROVENANCE_REF
UNKNOWN_SOURCE_CLASS
RESTRICTED_FULL_TEXT_DETECTED
SCHEMA_TARGET_NOT_FOUND
REQUIRED_FIELD_MISSING
UNMAPPABLE_FIELD_STRUCTURE
```

## 7. Quarantine rule

The future fixture must demonstrate quarantine for:

```text
UNKNOWN_SOURCE_CLASS
RESTRICTED_FULL_TEXT_DETECTED
PAYLOAD_TYPE_CONTRADICTION
MISSING_PROVENANCE_REF
```

## 8. Blocking failures

- rejected record lacks reason
- restricted full text not quarantined
- unknown source not quarantined
- rejected record has no remediation note
- rejected record is later used in formula signal mapping
- rejected record disappears from reports without superseding remediation

## 9. Final decision

Rejected records fixture is required before corpus adapter implementation because unsafe or invalid records must be visible and auditable.
