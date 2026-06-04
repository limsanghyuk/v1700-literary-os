# Narrative Corpus Database Blueprint

Status: blueprint draft
Created: 2026-06-04
Scope: Page18+ planning, no implementation

## 1. Purpose

This blueprint defines a future narrative corpus database for V1700.

It is a metadata and analysis database, not a raw copyrighted text ingestion plan.

## 2. Core principle

The database must store structured analytical records, not uncontrolled full-text copies.

The goal is to support:

- genre pattern comparison
- scene function analysis
- character arc modeling
- relationship transition analysis
- tension curve analysis
- dialogue function tagging
- trope detection and variation
- reader and viewer response mapping
- value proof experiments
- LearnableCritic calibration

## 3. Candidate corpus domains

Initial domains:

- Korean dramas
- global prestige dramas
- platform series
- Japanese animation
- genre fiction
- literary fiction
- web novels
- screenplays where legally available

## 4. Record model

### 4.1 WorkRecord

Fields:

- work_id
- title
- country_or_language
- medium
- genre_tags
- release_period
- source_rights_status
- analysis_permission_status
- provenance_ref

### 4.2 EpisodeOrChapterRecord

Fields:

- segment_id
- work_id
- sequence_index
- synopsis
- major_turning_points
- primary_conflict
- ending_hook
- provenance_ref

### 4.3 SceneRecord

Fields:

- scene_id
- segment_id
- scene_order
- scene_function
- location_type
- active_characters
- conflict_type
- emotional_start
- emotional_end
- tension_delta
- information_delta
- reader_viewer_position
- closing_image_type

### 4.4 CharacterArcRecord

Fields:

- character_id
- work_id
- desire
- wound
- false_belief
- pressure_source
- arc_phase
- decision_points
- behavior_shift
- relationship_links

### 4.5 DialogueFunctionRecord

Fields:

- dialogue_unit_id
- scene_id
- speaker_role
- overt_function
- subtext_function
- conflict_pressure
- exposition_load
- rhythm_note

### 4.6 AudienceSignalRecord

Fields:

- signal_id
- work_id
- segment_id
- source_type
- rating_signal
- review_theme
- dropoff_or_retention_note
- emotional_reaction_tags
- cultural_context_note

## 5. Legal and ethical boundary

Required rules:

- no uncontrolled full-text scraping
- no copyrighted bulk replication without permission
- store analysis metadata when possible
- store provenance and rights status
- separate public-domain, licensed, user-owned, and analysis-only sources
- allow removal and correction records

## 6. Database architecture candidates

Recommended hybrid model:

- relational DB for authority records and provenance
- graph DB for character, relation, trope, and scene links
- vector index for metadata and synopsis search
- file/object store only for permitted assets

## 7. Integration with V1700

The corpus database should connect to:

- Value Proof Gate
- LearnableCritic Bridge
- NarrativeStateTensor advisory layer
- Formula Ledger v2
- Writer Collaborative Narrative IDE
- Multi-agent critic roles

## 8. Acceptance criteria before implementation

- rights policy defined
- schema v0.1 approved
- source categories defined
- ingestion protocol approved
- deletion/correction policy approved
- GitNexus evidence path planned
- no Page18 implementation opened yet

## 9. Open questions

- Which domain starts first: Korean drama, Japanese animation, or web novel?
- Is the first database hand-curated or semi-automated?
- What is the minimum dataset for value proof?
- Who approves rights classification?
- Should audience signal ingestion begin with public reviews or manually curated summaries?

## 10. Recommended first step

Create a corpus source policy and a minimal schema fixture before building the database.
