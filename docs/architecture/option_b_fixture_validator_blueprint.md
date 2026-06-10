# Option B Fixture Validator Blueprint

Status: blueprint draft
Created: 2026-06-10
Scope: validator design for Page18 Option B fixtures, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint defines the future validator for the Page18 Option B fixture bundle.

It does not implement the validator. It specifies modules, input files, output records, and fail-closed behavior required before any implementation scaffold is created.

## 2. Target fixture bundle

```text
fixtures/corpus_adapter_mapping/mapping_table.json
fixtures/narrative_corpus_minimum/fixture.json
fixtures/formula_catalog_minimum/fixture.json
fixtures/formula_signal_minimum/fixture.json
fixtures/corpus_adapter_rejected_records/rejected_records.json
```

## 3. Validation reports

The validator should update or emit:

```text
fixtures/option_b_validation/source_review_report.md
fixtures/option_b_validation/schema_validation_report.md
fixtures/option_b_validation/corpus_adapter_mapping_report.md
fixtures/option_b_validation/formula_signal_validation_report.md
fixtures/option_b_validation/rejected_records_report.md
```

## 4. Validator modules

### 4.1 JSON Parse Validator

Responsibilities:

- parse every fixture JSON file
- detect invalid JSON
- detect missing top-level fields
- record parse errors without continuing into unsafe downstream validation

### 4.2 Source Policy Validator

Responsibilities:

- validate `source_class`
- validate `rights_status`
- validate `provenance_ref`
- ensure restricted and unknown records remain quarantined
- reject unlicensed full-text payloads

### 4.3 Schema Validator

Responsibilities:

- validate base fixture record fields
- validate record type-specific fields
- validate cross-record references
- validate scene and causality metadata minimums

### 4.4 Mapping Table Validator

Responsibilities:

- validate mapping table fields
- ensure source fields map to declared target record and field
- ensure target record type is schema-supported
- ensure transformation rule is present

### 4.5 Formula Catalog Validator

Responsibilities:

- validate formula ids
- validate formula groups
- validate lineage refs
- validate input and output schema refs
- validate boundary rules

### 4.6 Formula Signal Validator

Responsibilities:

- validate signal ids
- validate formula references
- validate corpus source references
- validate input field names
- preserve fixture/placeholder status
- prevent proof overclaiming

### 4.7 Rejected Records Validator

Responsibilities:

- validate rejected record fields
- validate rejection reason and severity
- ensure quarantine-required cases are quarantined
- ensure rejected records are not used downstream

### 4.8 Acceptance Decision Builder

Responsibilities:

- aggregate validation results
- produce an acceptance status
- preserve warnings
- fail closed on blocking failures

## 5. Execution order

```text
1. JSON Parse Validator
2. Mapping Table Validator
3. Source Policy Validator
4. Schema Validator
5. Formula Catalog Validator
6. Formula Signal Validator
7. Rejected Records Validator
8. Acceptance Decision Builder
```

## 6. Fail-closed rule

If any blocking failure occurs, downstream readiness must be:

```text
NOT_READY
```

The validator must not silently promote a fixture bundle.

## 7. Required result output

The validator should produce:

```text
OptionBFixtureValidatorResult
```

defined in:

```text
docs/contracts/option_b_fixture_validator_result_contract.md
```

## 8. Non-goals

The validator must not:

- open Page18 implementation
- create Stage243+
- perform LLM generation
- mutate canonical story state
- perform coefficient learning
- ingest unreviewed external content

## 9. Final decision

The Option B validator must be deterministic, evidence-producing, warning-preserving, and fail-closed.
