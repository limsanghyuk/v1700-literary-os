# Narrative Corpus Minimum Fixture JSON Blueprint

Status: blueprint draft
Created: 2026-06-10
Scope: future metadata-only narrative corpus fixture JSON, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint defines the structure of a future minimum narrative corpus fixture JSON file.

It is not the fixture itself. It is a schema-level example for later implementation.

## 2. Future path

```text
fixtures/narrative_corpus_minimum/fixture.json
```

## 3. Top-level JSON shape

```json
{
  "fixture_id": "narrative_corpus_minimum_v0_1",
  "fixture_version": "0.1",
  "schema_ref": "docs/architecture/narrative_corpus_schema_v0_1.md",
  "source_policy_ref": "docs/policies/narrative_corpus_source_policy.md",
  "review_status": "DRAFT",
  "records": []
}
```

## 4. Required top-level fields

```text
fixture_id
fixture_version
schema_ref
source_policy_ref
review_status
records
```

## 5. Base record shape

Every record in `records` must include:

```json
{
  "record_id": "rec_example_001",
  "record_type": "SceneBlueprintRecord",
  "source_class": "METADATA_ONLY_ANALYSIS_RECORD",
  "rights_status": "METADATA_ONLY",
  "provenance_ref": "source_review:example",
  "review_status": "DRAFT",
  "created_at": "2026-06-10T00:00:00Z",
  "updated_at": "2026-06-10T00:00:00Z"
}
```

## 6. Minimum record inventory

The future fixture should include at least:

```text
1 WorkRecord
1 DramaEntryRecord
1 CorePhilosophyRecord
2 CharacterRecord
1 RelationshipGraphRecord
2 SceneBlueprintRecord
2 CausalityMatrixRecord
1 DialogueFunctionRecord
1 CriticThresholdRecord
```

FormulaSignalRecord may be held in a separate fixture until validation is complete.

## 7. Example SceneBlueprintRecord shape

```json
{
  "record_id": "scene_001",
  "record_type": "SceneBlueprintRecord",
  "source_class": "METADATA_ONLY_ANALYSIS_RECORD",
  "rights_status": "METADATA_ONLY",
  "provenance_ref": "source_review:scene_001",
  "review_status": "DRAFT",
  "scene_blueprint_id": "scene_001",
  "segment_id": "segment_001",
  "scene_order": 1,
  "scene_function": "inciting_pressure",
  "active_character_roles": ["protagonist", "opponent"],
  "conflict_type": "value_conflict",
  "emotional_start_tag": "controlled",
  "emotional_end_tag": "destabilized",
  "tension_delta_label": "increase",
  "information_delta_label": "new_risk_revealed"
}
```

## 8. Example CausalityMatrixRecord shape

```json
{
  "record_id": "causality_001",
  "record_type": "CausalityMatrixRecord",
  "source_class": "METADATA_ONLY_ANALYSIS_RECORD",
  "rights_status": "METADATA_ONLY",
  "provenance_ref": "source_review:causality_001",
  "review_status": "DRAFT",
  "causality_matrix_id": "causality_001",
  "work_id": "work_001",
  "trigger_summary": "a prior choice creates social pressure",
  "resolution_summary": "the character avoids immediate collapse",
  "residue_summary": "unresolved emotional debt remains",
  "logic_consistency_note": "cause and consequence are explicit",
  "unresolved_debt": true
}
```

## 9. Forbidden payloads

The future JSON must not include:

- unlicensed full script text
- unlicensed book chapters
- subtitles
- raw transcripts
- hidden training payloads
- source material without provenance

## 10. Validation requirements

Before use, the fixture requires:

```text
SourceReviewReport
SchemaValidationReport
CorpusAdapterMappingReport
```

## 11. Final decision

The future JSON fixture must remain metadata-only, source-reviewed, schema-validated, and reversible.
