# Narrative Corpus Minimum Fixture Spec

Status: fixture spec draft
Created: 2026-06-09
Scope: narrative corpus planning fixture
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This fixture spec defines the smallest rights-aware structured metadata bundle needed before V1700 can test formula-to-corpus mapping, Value Proof preparation, or LearnableCritic audit planning.

This fixture is metadata-only. It must not contain full copyrighted scripts, episodes, books, subtitles, or other protected expressive text unless a separate explicit license decision exists.

## 2. Minimum fixture size

```text
works: 3
segments: 3 to 6
scenes: 6 to 12
characters: 6 to 12
causality records: 6 to 12
formula signals: 6 to 12
```

## 3. Allowed source classes

Each record must use one of:

```text
USER_PROVIDED_STRUCTURED_ANALYSIS_DB
USER_OWNED_SOURCE
PUBLIC_DOMAIN_SOURCE
LICENSED_SOURCE
METADATA_ONLY_ANALYSIS_RECORD
```

Unknown source class must remain quarantined.

## 4. Required records

Minimum record set:

```text
WorkRecord
DramaEntryRecord
CorePhilosophyRecord
CharacterRecord
KeyObjectRecord
CausalityMatrixRecord
EpisodeOrChapterRecord
SceneBlueprintRecord
DialogueFunctionRecord
CriticThresholdRecord
FormulaSignalRecord
RelationshipGraphRecord
```

Optional record set:

```text
AudienceSignalRecord
GenreEngineRecord
StyleModuleRecord
```

## 5. Required metadata fields

Each fixture record must include:

```text
record_id
record_type
source_class
rights_status
provenance_ref
review_status
```

Scene metadata must include:

```text
scene_function
active_character_roles
conflict_type
emotional_start_tag
emotional_end_tag
tension_delta_label
information_delta_label
```

Causality metadata must include:

```text
trigger_summary
resolution_summary
residue_summary
logic_consistency_note
```

Formula signal metadata must include:

```text
formula_id
source_record_ids
input_field_names
output_signal_type
explanation_summary
```

## 6. Fixture pass criteria

The fixture is valid if:

- every record has source classification
- every record has rights status
- no restricted full text is stored
- formula signals link to source records
- scene records can support controlled prompt construction
- LearnableCritic input records can reference formula signals
- corpus records can support one writer IDE scene review

## 7. Blocking failures

- source_class missing
- rights_status missing
- restricted full text included
- formula signal has no source record
- scene metadata lacks conflict or emotional transition tags
- causality metadata lacks trigger, resolution, or residue summary
- unknown source used outside quarantine

## 8. Output path proposal

Future fixture may live at:

```text
fixtures/narrative_corpus_minimum/fixture.json
fixtures/narrative_corpus_minimum/README.md
fixtures/narrative_corpus_minimum/source_review.md
```

## 9. Final rule

No corpus-backed Value Proof or LearnableCritic implementation should proceed until a minimum metadata-only corpus fixture is approved.
