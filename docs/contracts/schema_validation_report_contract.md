# Schema Validation Report Contract

Status: contract draft
Created: 2026-06-10
Scope: future corpus fixture schema validation report
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This contract defines the structure of a future schema validation report for V1700 metadata-only corpus fixtures.

The report verifies that fixture records conform to `narrative_corpus_schema_v0_1.md`.

## 2. Required report record

```text
SchemaValidationReport
```

## 3. Required fields

```text
report_id
fixture_path
schema_ref
validation_status
record_count_total
record_count_by_type
missing_required_fields
invalid_record_refs
warning_count
blocking_failure_count
created_at
review_status
```

## 4. Validation statuses

```text
NOT_RUN
PASS
PASS_WITH_WARNINGS
FAIL
BLOCKED
```

## 5. Required checks

The validator must check:

- record_id exists
- record_type exists
- source_class exists
- rights_status exists
- provenance_ref exists
- required fields by record type exist
- FormulaSignalRecord links to valid source records
- CausalityMatrixRecord includes trigger / resolution / residue summary fields
- SceneBlueprintRecord includes conflict and emotional transition fields

## 6. Required output sections

```text
1. Fixture summary
2. Schema reference
3. Record count by type
4. Required field validation
5. Cross-record link validation
6. Source and rights field validation
7. Warnings
8. Blocking failures
9. Final validation status
```

## 7. Blocking failures

- any record missing record_id
- any record missing record_type
- any record missing source_class
- any record missing rights_status
- any record missing provenance_ref
- FormulaSignalRecord source_record_id missing or invalid
- restricted full text field detected
- schema_ref missing

## 8. Review statuses

```text
DRAFT
VALIDATED
VALIDATED_WITH_WARNINGS
REJECTED
SUPERSEDED
```

## 9. Final decision

Schema validation is required before a narrative corpus fixture can be used by Value Proof, LearnableCritic audit, or Writer IDE prototypes.
