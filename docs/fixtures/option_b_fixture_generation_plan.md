# Option B Fixture Generation Plan

Status: planning draft
Created: 2026-06-10
Scope: Page18 Option B fixture generation planning, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This plan defines how future Page18 Option B fixtures should be generated after entry criteria are satisfied.

It does not create the JSON fixtures and does not open Page18.

## 2. Option B scope

Option B is:

```text
Corpus and Formula Mapping Infrastructure
```

The target is metadata-only corpus and formula signal mapping support.

## 3. Planned fixture outputs

Future outputs:

```text
fixtures/narrative_corpus_minimum/fixture.json
fixtures/formula_catalog_minimum/fixture.json
fixtures/formula_signal_minimum/fixture.json
fixtures/corpus_adapter_mapping/mapping_table.json
fixtures/corpus_adapter_rejected_records/rejected_records.json
```

## 4. Required preconditions

Before fixture generation, the following must exist:

```text
docs/policies/narrative_corpus_source_policy.md
docs/architecture/narrative_corpus_schema_v0_1.md
docs/contracts/corpus_fixture_record_contract.md
docs/contracts/formula_catalog_record_contract.md
docs/contracts/formula_signal_record_contract.md
docs/contracts/corpus_adapter_mapping_report_contract.md
docs/contracts/corpus_adapter_rejected_record_contract.md
docs/fixtures/narrative_corpus_minimum_fixture_json_blueprint.md
docs/fixtures/formula_catalog_minimum_fixture_json_blueprint.md
docs/fixtures/formula_signal_minimum_fixture_json_blueprint.md
docs/fixtures/corpus_adapter_mapping_table_blueprint.md
docs/fixtures/corpus_adapter_rejected_records_fixture_blueprint.md
```

## 5. Generation order

Recommended generation order:

```text
1. corpus_adapter_mapping/mapping_table.json
2. narrative_corpus_minimum/fixture.json
3. formula_catalog_minimum/fixture.json
4. formula_signal_minimum/fixture.json
5. corpus_adapter_rejected_records/rejected_records.json
```

Reason:

Mapping table clarifies how source fields become corpus fields. Corpus and formula catalog must exist before formula signals. Rejected records can then document negative-path behavior.

## 6. Source policy rule

Every generated fixture must include references to:

```text
source_policy_ref
schema_ref
contract_ref
review_status
```

No fixture may include unlicensed full text, subtitles, raw transcripts, or unknown-source expressive payloads.

## 7. Required review outputs

Future fixture generation should also produce or prepare:

```text
source_review_report.md
schema_validation_report.md
formula_signal_validation_report.md
corpus_adapter_mapping_report.md
rejected_records_report.md
```

## 8. Fixture generation modes

Allowed modes:

```text
MANUAL_BLUEPRINT_DERIVED
HAND_CURATED_METADATA_ONLY
SYNTHETIC_METADATA_ONLY
USER_PROVIDED_STRUCTURED_ANALYSIS_DB
```

Disallowed by default:

```text
UNREVIEWED_FULL_TEXT_EXTRACTION
UNKNOWN_SOURCE_IMPORT
PROVIDER_GENERATED_CANONICAL_DATA
```

## 9. Blocking failures

- fixture generated before source policy references exist
- fixture generated without schema reference
- formula signal fixture generated before corpus and catalog fixtures
- rejected records not represented
- restricted full text included
- provenance missing
- review status missing

## 10. Final decision

Option B fixture generation should proceed only after this plan, validation sequence, and acceptance criteria are all present.
