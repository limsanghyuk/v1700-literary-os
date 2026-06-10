# Formula Catalog Minimum Fixture JSON Blueprint

Status: blueprint draft
Created: 2026-06-10
Scope: future formula catalog fixture JSON, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint defines the structure of a future minimum FormulaCatalogRecord fixture JSON file.

It is intended to support Page18 Option B formula-to-corpus mapping infrastructure.

## 2. Future path

```text
fixtures/formula_catalog_minimum/fixture.json
```

## 3. Top-level JSON shape

```json
{
  "fixture_id": "formula_catalog_minimum_v0_1",
  "fixture_version": "0.1",
  "catalog_contract_ref": "docs/contracts/formula_catalog_record_contract.md",
  "normalization_report_ref": "docs/reviews/formula_catalog_normalization_report.md",
  "review_status": "DRAFT",
  "formula_catalog_records": []
}
```

## 4. Required top-level fields

```text
fixture_id
fixture_version
catalog_contract_ref
normalization_report_ref
review_status
formula_catalog_records
```

## 5. Minimum formula catalog record shape

```json
{
  "formula_id": "formula_emotional_momentum_v0_1",
  "formula_name": "Emotional Momentum",
  "formula_group": "EMOTIONAL_MOMENTUM",
  "canonical_label": "EMOTIONAL_MOMENTUM_SIGNAL_SOURCE",
  "lineage_ref": "UPLOADED_USER_FORMULA_ARCHIVE",
  "alias_refs": ["emotional_momentum", "emotion_delta"],
  "purpose": "Estimate directional emotional transition in scene metadata.",
  "input_schema_refs": ["SceneBlueprintRecord.emotional_start_tag", "SceneBlueprintRecord.emotional_end_tag"],
  "output_schema_refs": ["FormulaSignalRecord.output_signal_value_or_label"],
  "allowed_consumer_refs": ["FORMULA_SIGNAL_RUNTIME_BRIDGE", "WRITER_IDE_ADVISORY_PANEL"],
  "boundary_rule_refs": ["ADVISORY_ONLY", "VALID_FOR_SCHEMA_WIRING"],
  "review_status": "DRAFT"
}
```

## 6. Minimum formula groups

The future fixture should include at least one record for:

```text
NARRATIVE_STATE_TENSOR
EMOTIONAL_MOMENTUM
CHARACTER_INTERACTION_MATRIX
DRSE
NARRATIVE_FITNESS_SCORE
```

## 7. Required lineage labels

Each formula must use one of:

```text
GPT_V1700_FORMULA
SOVEREIGN_OS_FORMULA_SPEC
CLAUDE_LITERARY_OS_FORMULA
SHARED_HISTORICAL_FORMULA
UPLOADED_USER_FORMULA_ARCHIVE
DUPLICATE_OR_OVERLAP
UNRESOLVED_LINEAGE
```

## 8. Boundary rule requirements

Every formula must declare at least one boundary rule:

```text
ADVISORY_ONLY
VALID_FOR_SCHEMA_WIRING
VALID_FOR_UI_WIRING
VALID_FOR_VALUE_PROOF_PREREGISTRATION
VALID_FOR_LEARNABLE_CRITIC_AUDIT
NOT_VALID_FOR_RUNTIME_USE
```

## 9. Blocking failures

- formula_id missing
- formula_group missing
- lineage_ref missing
- input_schema_refs missing
- output_schema_refs missing
- unresolved lineage used as authority
- formula has no boundary rule

## 10. Validation requirements

Before use, the fixture requires:

```text
FormulaSignalValidationReport
FormulaCatalogRecord contract review
Formula-to-corpus mapping report
```

## 11. Final decision

The formula catalog fixture must remain explicit, lineage-aware, and advisory until downstream gates approve use.
