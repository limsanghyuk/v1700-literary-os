# Option B Schema Validation Report

Status: NOT_RUN
Created: 2026-06-10
Scope: preliminary schema validation skeleton for Option B fixtures
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This report skeleton records schema validation requirements for Option B fixtures.

It does not yet claim PASS because validation has not been executed.

## 2. Target fixture bundle

```text
fixtures/narrative_corpus_minimum/fixture.json
fixtures/formula_catalog_minimum/fixture.json
fixtures/formula_signal_minimum/fixture.json
fixtures/corpus_adapter_mapping/mapping_table.json
fixtures/corpus_adapter_rejected_records/rejected_records.json
```

## 3. Schema and contract references

```text
docs/architecture/narrative_corpus_schema_v0_1.md
docs/contracts/corpus_fixture_record_contract.md
docs/contracts/formula_catalog_record_contract.md
docs/contracts/formula_signal_record_contract.md
docs/contracts/corpus_adapter_mapping_report_contract.md
docs/contracts/corpus_adapter_rejected_record_contract.md
```

## 4. Required validation checks

```text
[ ] JSON files parse
[ ] required top-level fields exist
[ ] every corpus record includes record_id
[ ] every corpus record includes record_type
[ ] every corpus record includes source_class
[ ] every corpus record includes rights_status
[ ] every corpus record includes provenance_ref
[ ] scene records include conflict and emotional transition metadata
[ ] causality records include trigger / resolution / residue metadata
[ ] formula records include lineage and boundary rules
[ ] formula signals reference existing formula ids
[ ] formula signals reference existing corpus record ids
[ ] rejected records include rejection reason and severity
```

## 5. Current decision

```text
SCHEMA_VALIDATION_NOT_RUN
```

## 6. Blocking failures to check later

- JSON parse failure
- missing required top-level field
- missing base record field
- invalid cross-record reference
- formula signal referencing nonexistent source record
- formula signal referencing nonexistent formula record

## 7. Final note

This file is a validation report skeleton. It must be updated after actual validation is performed.
