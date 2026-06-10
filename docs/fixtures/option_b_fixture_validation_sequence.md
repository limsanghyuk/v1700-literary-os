# Option B Fixture Validation Sequence

Status: validation sequence draft
Created: 2026-06-10
Scope: Page18 Option B fixture validation planning, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This document defines the validation sequence required before future Option B fixtures can be used by downstream V1700 systems.

It does not run validation and does not create fixtures.

## 2. Target fixtures

```text
fixtures/corpus_adapter_mapping/mapping_table.json
fixtures/narrative_corpus_minimum/fixture.json
fixtures/formula_catalog_minimum/fixture.json
fixtures/formula_signal_minimum/fixture.json
fixtures/corpus_adapter_rejected_records/rejected_records.json
```

## 3. Required validation reports

```text
source_review_report.md
schema_validation_report.md
corpus_adapter_mapping_report.md
formula_signal_validation_report.md
rejected_records_report.md
```

## 4. Validation sequence

### Step 1 — Mapping table structural validation

Validate:

- mapping table id
- adapter version
- source_policy_ref
- schema_ref
- every mapping row has source and target fields
- no target record type outside schema

### Step 2 — Source review

Validate:

- every corpus record has source_class
- every corpus record has rights_status
- every corpus record has provenance_ref
- restricted full text absent
- unknown sources quarantined

### Step 3 — Corpus schema validation

Validate:

- base fields exist
- record type-specific required fields exist
- cross-record links resolve
- scene metadata includes conflict and emotional transition tags
- causality metadata includes trigger, resolution, and residue summaries

### Step 4 — Formula catalog validation

Validate:

- every formula has formula_id
- every formula has formula_group
- every formula has lineage_ref
- every formula has input/output schema refs
- every formula has boundary rules

### Step 5 — Formula signal validation

Validate:

- every signal references an existing formula
- every signal references existing corpus records
- input fields exist in schema
- signal type label is clear
- placeholder signal is not treated as proof

### Step 6 — Rejected records validation

Validate:

- rejected record has reason
- rejected record has severity
- quarantine-required categories are quarantined
- rejected records are excluded from formula signal mapping
- remediation is documented

### Step 7 — Downstream readiness decision

Assign one of:

```text
NOT_READY
READY_FOR_SCHEMA_WIRING
READY_FOR_FORMULA_SIGNAL_MAPPING
READY_FOR_VALUE_PROOF_PREREGISTRATION
READY_FOR_LEARNABLE_CRITIC_AUDIT
READY_FOR_WRITER_IDE_STATIC_FLOW
```

## 5. Validation order rule

Formula signals cannot be validated before:

```text
corpus fixture validation
formula catalog validation
source review
schema validation
```

## 6. Blocking failures

- source review missing
- schema validation missing
- formula catalog validation missing
- formula signal validation run before prerequisites
- rejected records missing despite blocked input categories
- placeholder signal used as calculated proof
- restricted full text detected

## 7. Final decision

Option B fixture validation must be sequential, evidence-producing, and fail-closed.
