# Formula Signal Validation Report Contract

Status: contract draft
Created: 2026-06-10
Scope: future validation report for FormulaSignalRecord mappings
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This contract defines the validation report required before formula signals can be used by Value Proof, LearnableCritic, Writer IDE, or multi-agent supervision.

Formula signals are advisory and traceable. They are not canonical truth by default.

## 2. Required report record

```text
FormulaSignalValidationReport
```

## 3. Required fields

```text
report_id
mapping_report_ref
formula_catalog_ref
corpus_fixture_ref
schema_validation_report_ref
source_review_report_ref
validation_status
formula_signal_count
placeholder_signal_count
calculated_signal_count
invalid_signal_refs
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

Each FormulaSignalRecord must include:

```text
formula_signal_id
formula_id
formula_group
source_record_ids
source_record_types
input_field_names
output_signal_type
output_signal_value_or_label
explanation_summary
review_status
```

Each signal must verify:

- formula_id exists in formula catalog
- source records exist in corpus fixture
- input fields exist in schema
- source review permits referenced records
- placeholder status is clearly labeled
- signal is not treated as proof unless calculated and reviewed

## 6. Signal type labels

```text
PLACEHOLDER_SIGNAL
MANUAL_REVIEW_SIGNAL
FIXTURE_SIGNAL
CALCULATED_SIGNAL
```

## 7. Allowed use status

```text
VALID_FOR_SCHEMA_WIRING
VALID_FOR_UI_WIRING
VALID_FOR_VALUE_PROOF_PREREGISTRATION
VALID_FOR_LEARNABLE_CRITIC_AUDIT
NOT_VALID_FOR_USE
```

## 8. Required output sections

```text
1. Formula catalog reference
2. Corpus fixture reference
3. Schema validation reference
4. Source review reference
5. Formula signal inventory
6. Signal type distribution
7. Invalid signals
8. Placeholder warning
9. Allowed use decision
10. Blocking failures
```

## 9. Blocking failures

- formula_id missing
- source_record_ids missing
- input fields missing or invalid
- source review report missing
- schema validation report missing
- placeholder signal treated as calculated proof
- formula signal used for coefficient update without audit record
- formula signal used in Value Proof without preregistration

## 10. Final decision

Formula signal validation is required before any FormulaSignalRecord output can be consumed by downstream V1700 systems.
