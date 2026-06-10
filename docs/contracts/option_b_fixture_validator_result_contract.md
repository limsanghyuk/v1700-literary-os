# Option B Fixture Validator Result Contract

Status: contract draft
Created: 2026-06-10
Scope: result record for future Option B fixture validator
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This contract defines the result object emitted by a future Option B fixture validator.

The result must be explicit, warning-preserving, and fail-closed.

## 2. Required result record

```text
OptionBFixtureValidatorResult
```

## 3. Required fields

```text
result_id
validator_version
fixture_bundle_refs
source_review_report_ref
schema_validation_report_ref
mapping_report_ref
formula_signal_validation_report_ref
rejected_records_report_ref
validation_started_at
validation_completed_at
overall_status
module_results
warning_count
blocking_failure_count
downstream_readiness
acceptance_status
created_at
review_status
```

## 4. Module result fields

Each module result must include:

```text
module_name
module_status
checked_file_refs
warning_refs
blocking_failure_refs
summary
```

## 5. Overall statuses

```text
NOT_RUN
PASS
PASS_WITH_WARNINGS
FAIL
BLOCKED
```

## 6. Module statuses

```text
NOT_RUN
PASS
PASS_WITH_WARNINGS
FAIL
BLOCKED
SKIPPED_DUE_TO_PRIOR_FAILURE
```

## 7. Downstream readiness values

```text
NOT_READY
READY_FOR_SCHEMA_WIRING
READY_FOR_FORMULA_SIGNAL_MAPPING
READY_FOR_VALUE_PROOF_PREREGISTRATION
READY_FOR_LEARNABLE_CRITIC_AUDIT
READY_FOR_WRITER_IDE_STATIC_FLOW
```

## 8. Acceptance status values

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

## 9. Warning preservation rule

If warning_count > 0, the result cannot hide warnings behind PASS.

Allowed statuses:

```text
PASS_WITH_WARNINGS
ACCEPTED_WITH_WARNINGS
```

## 10. Blocking failure rule

If blocking_failure_count > 0:

```text
overall_status: BLOCKED
acceptance_status: BLOCKED
downstream_readiness: NOT_READY
```

## 11. Required file refs

The result must reference:

```text
fixtures/corpus_adapter_mapping/mapping_table.json
fixtures/narrative_corpus_minimum/fixture.json
fixtures/formula_catalog_minimum/fixture.json
fixtures/formula_signal_minimum/fixture.json
fixtures/corpus_adapter_rejected_records/rejected_records.json
```

## 12. Final decision

No Option B fixture bundle should be treated as accepted unless an OptionBFixtureValidatorResult exists and declares a valid acceptance status.
