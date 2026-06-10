# Formula Signal Minimum Fixture JSON Blueprint

Status: blueprint draft
Created: 2026-06-10
Scope: future FormulaSignalRecord fixture JSON, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint defines the structure of a future minimum FormulaSignalRecord fixture JSON file.

It connects formula catalog records to metadata-only corpus records through traceable advisory signals.

## 2. Future path

```text
fixtures/formula_signal_minimum/fixture.json
```

## 3. Top-level JSON shape

```json
{
  "fixture_id": "formula_signal_minimum_v0_1",
  "fixture_version": "0.1",
  "formula_signal_contract_ref": "docs/contracts/formula_signal_record_contract.md",
  "formula_catalog_fixture_ref": "fixtures/formula_catalog_minimum/fixture.json",
  "corpus_fixture_ref": "fixtures/narrative_corpus_minimum/fixture.json",
  "review_status": "DRAFT",
  "formula_signal_records": []
}
```

## 4. Required FormulaSignalRecord shape

```json
{
  "formula_signal_id": "signal_emotional_momentum_scene_001",
  "formula_id": "formula_emotional_momentum_v0_1",
  "formula_group": "EMOTIONAL_MOMENTUM",
  "source_record_ids": ["scene_001"],
  "source_record_types": ["SceneBlueprintRecord"],
  "input_field_names": ["emotional_start_tag", "emotional_end_tag", "tension_delta_label"],
  "source_class_summary": "METADATA_ONLY_ANALYSIS_RECORD",
  "rights_status_summary": "METADATA_ONLY",
  "output_signal_type": "EMOTIONAL_MOMENTUM_SIGNAL",
  "output_signal_value_or_label": "increase_destabilizing",
  "confidence": 0.5,
  "explanation_summary": "Fixture-level advisory signal derived from emotional transition metadata.",
  "signal_type_label": "FIXTURE_SIGNAL",
  "critic_mapping_ref": "CriticInputSourceRecord:future",
  "value_proof_mapping_ref": "ValueProof:preregistration_required",
  "writer_ide_panel_ref": "WriterIDE:advisory_panel_future",
  "created_at": "2026-06-10T00:00:00Z",
  "review_status": "DRAFT"
}
```

## 5. Minimum signal inventory

Future fixture should include at least:

```text
1 NARRATIVE_STATE_TENSOR_SIGNAL
1 EMOTIONAL_MOMENTUM_SIGNAL
1 CHARACTER_INTERACTION_SIGNAL
1 CAUSALITY_TRANSITION_SIGNAL
1 NARRATIVE_FITNESS_COMPANION_SIGNAL
```

## 6. Signal type limits

The first fixture may use:

```text
PLACEHOLDER_SIGNAL
FIXTURE_SIGNAL
MANUAL_REVIEW_SIGNAL
```

It should not claim:

```text
CALCULATED_SIGNAL
```

unless an actual validated formula runtime exists.

## 7. Required validation reports

Before use, future fixture requires:

```text
FormulaSignalValidationReport
SchemaValidationReport
SourceReviewReport
Formula signal mapping minimal report
```

## 8. Blocking failures

- missing formula_signal_id
- missing formula_id
- missing source_record_ids
- source record missing from corpus fixture
- formula missing from catalog fixture
- input field missing from schema
- placeholder signal treated as proof
- signal used in Value Proof without preregistration
- signal used in LearnableCritic without audit trail

## 9. Final decision

Formula signal fixture must remain advisory, traceable, and validation-gated before downstream use.
