# Option B Rejected Records Report

Status: NOT_RUN
Created: 2026-06-10
Scope: preliminary rejected records report skeleton for Option B fixtures
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This report skeleton records review requirements for rejected or quarantined corpus adapter records.

It does not claim PASS because rejected records validation has not been executed.

## 2. Target fixture

```text
fixtures/corpus_adapter_rejected_records/rejected_records.json
```

## 3. Contract reference

```text
docs/contracts/corpus_adapter_rejected_record_contract.md
```

## 4. Required validation checks

```text
[ ] rejected_records fixture parses
[ ] rejected_records array exists
[ ] every rejected record has rejected_record_id
[ ] every rejected record has rejection_reason
[ ] every rejected record has rejection_severity
[ ] every rejected record has source_class
[ ] every rejected record has rights_status
[ ] every rejected record has provenance_ref
[ ] quarantine-required categories are quarantined
[ ] restricted full text category is quarantined
[ ] unknown source category is quarantined
[ ] rejected records are not used by formula_signal_minimum fixture
```

## 5. Current decision

```text
REJECTED_RECORDS_VALIDATION_NOT_RUN
```

## 6. Required rejection categories expected

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

## 7. Blocking failures to check later

- rejected record lacks rejection_reason
- rejected record lacks rejection_severity
- restricted full text not quarantined
- unknown source not quarantined
- rejected record used downstream
- rejected record disappears without remediation/supersession

## 8. Final note

This file is a validation report skeleton. It must be updated after actual rejected records validation is performed.
