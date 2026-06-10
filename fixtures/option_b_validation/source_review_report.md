# Option B Source Review Report

Status: NOT_RUN
Created: 2026-06-10
Scope: preliminary source review skeleton for Option B fixtures
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This report skeleton records the source and rights review required before Option B fixture bundle acceptance.

It does not yet claim PASS because automated or manual validation has not been executed.

## 2. Target fixture bundle

```text
fixtures/corpus_adapter_mapping/mapping_table.json
fixtures/narrative_corpus_minimum/fixture.json
fixtures/formula_catalog_minimum/fixture.json
fixtures/formula_signal_minimum/fixture.json
fixtures/corpus_adapter_rejected_records/rejected_records.json
```

## 3. Source policy reference

```text
docs/policies/narrative_corpus_source_policy.md
```

## 4. Preliminary source class inventory

Expected allowed classes in positive fixtures:

```text
METADATA_ONLY_ANALYSIS_RECORD
```

Expected rejected/quarantined classes in negative-path fixture:

```text
MISSING
UNKNOWN_OR_UNRESOLVED_SOURCE
RESTRICTED_COPYRIGHTED_FULL_TEXT
```

## 5. Required review checks

```text
[ ] every positive fixture record has source_class
[ ] every positive fixture record has rights_status
[ ] every positive fixture record has provenance_ref
[ ] restricted full-text records appear only in rejected/quarantined fixture
[ ] unknown source records appear only in rejected/quarantined fixture
[ ] mapping table preserves source policy requirement
```

## 6. Current decision

```text
SOURCE_REVIEW_NOT_RUN
```

## 7. Blocking failures to check later

- missing source_class in positive fixture
- missing rights_status in positive fixture
- missing provenance_ref in positive fixture
- restricted full text outside rejected records fixture
- unknown source outside quarantine

## 8. Final note

This file is a validation report skeleton. It must be updated after actual validation is performed.
