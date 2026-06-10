# Corpus Fixture Record Contract

Status: contract draft
Created: 2026-06-10
Scope: future metadata-only narrative corpus fixture records
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This contract defines the minimum record-level contract for future V1700 narrative corpus fixtures.

The fixture is metadata-only and rights-aware. It must not contain unlicensed full-text scripts, books, subtitles, or other protected expressive content.

## 2. Required base record

```text
CorpusFixtureRecord
```

## 3. Required base fields

Every corpus fixture record must include:

```text
record_id
record_type
source_class
rights_status
provenance_ref
review_status
created_at
updated_at
```

## 4. Allowed record types

```text
WorkRecord
DramaEntryRecord
CorePhilosophyRecord
LorebookRecord
CharacterRecord
KeyObjectRecord
CausalityMatrixRecord
EpisodeOrChapterRecord
SceneBlueprintRecord
DialogueFunctionRecord
StyleModuleRecord
CriticThresholdRecord
AudienceSignalRecord
GenreEngineRecord
RelationshipGraphRecord
FormulaSignalRecord
```

## 5. Required source fields

```text
source_class
source_name
provenance_ref
rights_status
allowed_use_scope
restriction_notes
review_status
```

## 6. Required scene metadata fields

For `SceneBlueprintRecord`:

```text
scene_blueprint_id
segment_id
scene_order
scene_function
active_character_roles
conflict_type
emotional_start_tag
emotional_end_tag
tension_delta_label
information_delta_label
```

## 7. Required causality metadata fields

For `CausalityMatrixRecord`:

```text
causality_matrix_id
work_id
trigger_summary
resolution_summary
residue_summary
logic_consistency_note
unresolved_debt
```

## 8. Required relationship metadata fields

For `RelationshipGraphRecord`:

```text
relationship_graph_id
work_id
node_refs
edge_refs
relationship_type
pressure_level
trust_level
conflict_level
hidden_dependency_note
```

## 9. Review statuses

```text
DRAFT
SOURCE_REVIEW_READY
SCHEMA_VALIDATED
FORMULA_SIGNAL_VALIDATED
VALUE_PROOF_READY
LEARNABLE_CRITIC_READY
REJECTED
SUPERSEDED
```

## 10. Blocking failures

- missing record_id
- missing record_type
- missing source_class
- missing rights_status
- missing provenance_ref
- unknown source used outside quarantine
- restricted full text included
- FormulaSignalRecord references missing source records

## 11. Final decision

No future fixture JSON should be accepted unless all CorpusFixtureRecord requirements are met.
