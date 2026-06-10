# Corpus Ingestion Adapter Blueprint

Status: blueprint draft
Created: 2026-06-10
Scope: metadata-only corpus adapter planning, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint defines a future metadata-only ingestion adapter for the V1700 narrative corpus.

It is not a full-text ingestion system. It converts approved structured analysis records into V1700 corpus schema records.

## 2. Source boundary

Allowed source classes:

- USER_PROVIDED_STRUCTURED_ANALYSIS_DB
- USER_OWNED_SOURCE
- PUBLIC_DOMAIN_SOURCE
- LICENSED_SOURCE
- METADATA_ONLY_ANALYSIS_RECORD

Default blocked source class:

- RESTRICTED_COPYRIGHTED_FULL_TEXT
- UNKNOWN_OR_UNRESOLVED_SOURCE

## 3. Adapter goals

- validate source class
- validate rights status
- normalize uploaded DB field names
- emit schema v0.1 records
- preserve provenance
- reject raw full-text payloads
- produce an ingestion review report

## 4. Input format candidates

Future adapter may accept:

```text
structured JSON
structured YAML
CSV exported from user-owned analysis DB
manual fixture record
DOCX-derived metadata summary only after review
```

The adapter must not ingest unreviewed expressive text.

## 5. Output records

The adapter may emit:

- WorkRecord
- DramaEntryRecord
- CorePhilosophyRecord
- LorebookRecord
- CharacterRecord
- KeyObjectRecord
- CausalityMatrixRecord
- EpisodeOrChapterRecord
- SceneBlueprintRecord
- DialogueFunctionRecord
- StyleModuleRecord
- CriticThresholdRecord
- RelationshipGraphRecord
- FormulaSignalRecord placeholder

## 6. Mapping seed from uploaded DB

Example source fields:

```text
Drama_Entry
Section_00_Core_Philosophy
Master_Theme
Conflict_Axis
Character
Key_Object
Causality_Matrix
Trigger
Resolution
Residue
Dialogue_Tone
Style_Module
Critic_Thresholds
Scene_Blueprint
Tragic_Engine
```

Example target records:

```text
Drama_Entry -> DramaEntryRecord
Master_Theme -> CorePhilosophyRecord.master_theme
Conflict_Axis -> CorePhilosophyRecord.conflict_axis
Character -> CharacterRecord
Key_Object -> KeyObjectRecord
Causality_Matrix -> CausalityMatrixRecord
Dialogue_Tone -> DialogueFunctionRecord.dialogue_tone
Critic_Thresholds -> CriticThresholdRecord
Scene_Blueprint -> SceneBlueprintRecord
Tragic_Engine -> GenreEngineRecord
```

## 7. Validation pipeline

```text
load source bundle
identify source class
verify rights status
scan for disallowed full-text fields
normalize field names
map to schema v0.1 records
validate required fields
emit fixture candidate
emit source review report
emit rejected records report
```

## 8. Required reports

Future adapter should produce:

```text
ingestion_source_review.md
ingestion_mapping_report.md
ingestion_rejected_records.md
ingestion_schema_validation_report.md
```

## 9. Blocking failures

- missing source class
- missing rights status
- unknown source used outside quarantine
- restricted full text detected
- provenance removed
- record mapped without schema target
- formula signal created without source record link

## 10. Page18 suitability

This adapter is suitable as a Page18 Option B candidate because it is:

- metadata-only
- deterministic
- reversible
- source-policy governed
- useful for Value Proof, LearnableCritic, Writer IDE, and multi-agent planning

## 11. Final decision

The first corpus adapter must ingest only approved structured metadata and analysis records.

No raw copyrighted text ingestion is permitted by default.
