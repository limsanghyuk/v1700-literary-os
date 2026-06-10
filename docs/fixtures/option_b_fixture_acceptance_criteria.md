# Option B Fixture Acceptance Criteria

Status: acceptance criteria draft
Created: 2026-06-10
Scope: Page18 Option B fixture acceptance planning, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This document defines the acceptance criteria for future Page18 Option B fixtures.

It does not accept any current fixture because the fixtures have not yet been generated.

## 2. Target acceptance unit

The acceptance unit is the full Option B fixture bundle:

```text
fixtures/corpus_adapter_mapping/mapping_table.json
fixtures/narrative_corpus_minimum/fixture.json
fixtures/formula_catalog_minimum/fixture.json
fixtures/formula_signal_minimum/fixture.json
fixtures/corpus_adapter_rejected_records/rejected_records.json
```

## 3. Required acceptance reports

The bundle cannot be accepted unless these reports exist:

```text
source_review_report.md
schema_validation_report.md
corpus_adapter_mapping_report.md
formula_signal_validation_report.md
rejected_records_report.md
```

## 4. Acceptance statuses

```text
NOT_SUBMITTED
SUBMITTED_FOR_REVIEW
ACCEPTED_FOR_SCHEMA_WIRING
ACCEPTED_FOR_FORMULA_SIGNAL_MAPPING
ACCEPTED_FOR_VALUE_PROOF_PREREGISTRATION
ACCEPTED_FOR_LEARNABLE_CRITIC_AUDIT
ACCEPTED_FOR_WRITER_IDE_STATIC_FLOW
ACCEPTED_WITH_WARNINGS
REJECTED
BLOCKED
```

## 5. Minimum acceptance criteria

The bundle may be accepted for schema wiring only if:

- all JSON files parse
- required top-level fields exist
- source policy references exist
- schema references exist
- every record has source_class
- every record has rights_status
- every record has provenance_ref
- no unlicensed full text is included
- schema validation is PASS or PASS_WITH_WARNINGS
- source review is PASS or PASS_WITH_WARNINGS

## 6. Formula signal mapping acceptance

The bundle may be accepted for formula signal mapping only if:

- formula catalog fixture exists
- corpus fixture exists
- formula signal fixture exists
- every signal references existing formula_id
- every signal references existing source_record_ids
- every input field exists in schema
- placeholder signals are labeled
- formula signal validation is PASS or PASS_WITH_WARNINGS

## 7. Value Proof preregistration acceptance

The bundle may be accepted for Value Proof preregistration only if:

- formula signals are validated
- Value Proof use is explicitly declared
- placeholder signals are not treated as performance proof
- source review permits referenced records
- LLM boundary remains at or below approved level

## 8. LearnableCritic audit acceptance

The bundle may be accepted for LearnableCritic audit only if:

- formula signals are valid for audit
- source records are allowed
- audit input source refs can be generated
- coefficient updates remain prohibited until audit fixture is present

## 9. Writer IDE static flow acceptance

The bundle may be accepted for Writer IDE static flow only if:

- corpus fixture includes at least one scene
- formula signal fixture includes at least one scene-linked signal
- source and rights warnings can be displayed
- no candidate is inserted as canonical text

## 10. Automatic rejection criteria

The bundle is automatically rejected if:

- restricted full text appears
- source_class is missing
- rights_status is missing
- provenance_ref is missing
- unknown source is used outside quarantine
- formula signal references nonexistent source records
- formula signal references nonexistent formula records
- placeholder signal is labeled as proof
- rejected record is used downstream

## 11. Warning preservation

PASS_WITH_WARNINGS is allowed only if warnings are preserved in:

```text
source_review_report.md
schema_validation_report.md
corpus_adapter_mapping_report.md
formula_signal_validation_report.md
```

Warnings must not be hidden by acceptance status.

## 12. Final decision

Option B fixture bundle acceptance must be explicit, report-backed, and fail-closed.

No fixture bundle should be used by implementation unless it has a declared acceptance status and linked validation reports.
