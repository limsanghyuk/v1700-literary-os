# Option B Rejected Records Report

Status: PASS
Created: 2026-06-10
Updated: 2026-06-10
Scope: rejected records validation for Option B fixtures
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This report records review results for rejected or quarantined corpus adapter records under the Option B validator scaffold.

## 2. Target fixture

```text
fixtures/corpus_adapter_rejected_records/rejected_records.json
```

## 3. Contract reference

```text
docs/contracts/corpus_adapter_rejected_record_contract.md
```

## 4. Validator artifact

```text
fixtures/option_b_validation/validator_result.json
```

## 5. Validation checks

```text
[x] rejected_records fixture parses
[x] rejected_records array exists
[x] every rejected record has rejected_record_id
[x] every rejected record has rejection_reason
[x] every rejected record has rejection_severity
[x] every rejected record has source_class
[x] every rejected record has rights_status
[x] every rejected record has provenance_ref
[x] quarantine-required categories are quarantined
[x] restricted full text category is quarantined
[x] unknown source category is quarantined
[x] rejected records are not used by formula_signal_minimum fixture
```

## 6. Current decision

```text
REJECTED_RECORDS_VALIDATION_PASS
```

## 7. Required rejection categories confirmed

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

## 8. Warning count

```text
0
```

## 9. Blocking failure count

```text
0
```

## 10. Final note

Rejected and quarantined records are represented as negative-path fixtures and are not accepted for downstream formula signal use.
