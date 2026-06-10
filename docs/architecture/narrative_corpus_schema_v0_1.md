# Narrative Corpus Schema v0.1

Status: schema draft
Created: 2026-06-07
Scope: narrative corpus planning, schema seed from uploaded Master DB files
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This schema defines an initial V1700 narrative corpus model.

It uses the uploaded K-Drama Master DB and Cinematic Sovereign DB row dumps as structured analysis schema seeds while preserving source and rights boundaries.

## 2. Schema principles

- store structured metadata and analysis records
- keep source class and rights status on every record
- avoid uncontrolled copyrighted full-text ingestion
- support drama, film, animation, novel, web novel, and screenplay metadata
- support formula mapping, Value Proof, LearnableCritic, Writer IDE, and multi-agent critic supervision

## 3. Base record fields

All records inherit:

```text
record_id
record_type
source_class
source_name
provenance_ref
rights_status
allowed_use_scope
review_status
created_at
updated_at
```

## 4. WorkRecord

Purpose:

Represents a work, series, film, novel, animation, or screenplay.

Fields:

```text
work_id
title
original_title
medium
country_or_language
genre_tags
release_period
creator_or_source_note
source_class
rights_status
provenance_ref
```

## 5. DramaEntryRecord

Purpose:

Adapter record for uploaded `Drama_Entry` style records.

Fields:

```text
drama_entry_id
work_id
entry_version
master_theme_ref
conflict_axis_ref
lorebook_ref
macro_architecture_ref
rendering_engine_ref
critic_threshold_ref
```

## 6. CorePhilosophyRecord

Seeded from:

- Section_00_Core_Philosophy
- Master_Theme
- Conflict_Axis
- Core_Dilemma
- Catastrophe_Source

Fields:

```text
core_philosophy_id
work_id
master_theme
conflict_axis
core_dilemma
catastrophe_source
moral_pressure
emotional_question
```

## 7. LorebookRecord

Seeded from:

- Section_01_Lorebook_Database
- Character
- Key_Object

Fields:

```text
lorebook_id
work_id
character_refs
key_object_refs
world_rule_refs
institution_refs
secret_refs
```

## 8. CharacterRecord

Purpose:

Represents character identity, desire, wound, pressure, and arc.

Fields:

```text
character_id
work_id
name_or_role
desire
wound
false_belief
pressure_source
arc_phase
behavior_shift
relationship_refs
```

## 9. KeyObjectRecord

Purpose:

Represents important symbolic, plot, or causal objects.

Fields:

```text
key_object_id
work_id
object_name
symbolic_function
causal_function
owner_or_association
appearance_refs
payoff_status
```

## 10. CausalityMatrixRecord

Seeded from:

- Causality_Matrix
- Trigger
- Resolution
- Residue
- Logic_Consistency

Fields:

```text
causality_matrix_id
work_id
source_event_ref
trigger
reaction
resolution
residue
logic_consistency_note
payoff_ref
unresolved_debt
```

## 11. EpisodeOrChapterRecord

Purpose:

Represents episode, chapter, act, or major segment.

Fields:

```text
segment_id
work_id
sequence_index
segment_type
synopsis
major_turning_points
primary_conflict
ending_hook
causality_refs
scene_refs
```

## 12. SceneBlueprintRecord

Seeded from:

- Scene_Blueprint
- Scene_Blueprint_V8

Fields:

```text
scene_blueprint_id
segment_id
scene_order
scene_function
active_characters
location_type
conflict_type
emotional_start
emotional_end
tension_delta
information_delta
closing_image_type
formula_signal_refs
```

## 13. DialogueFunctionRecord

Seeded from:

- Dialogue_Tone

Fields:

```text
dialogue_function_id
scene_blueprint_id
speaker_role
overt_function
subtext_function
dialogue_tone
conflict_pressure
exposition_load
rhythm_note
```

## 14. StyleModuleRecord

Seeded from:

- Style_Module
- Rendering_Engine

Fields:

```text
style_module_id
work_id
style_name
sentence_rhythm
visual_density
melodrama_level
comic_relief_level
genre_convention_notes
rendering_constraints
```

## 15. CriticThresholdRecord

Seeded from:

- Critic_Thresholds
- Tone_Penalty

Fields:

```text
critic_threshold_id
work_id
coherence_threshold
tension_threshold
emotion_threshold
dialogue_threshold
cliche_penalty
tone_penalty
rights_warning_threshold
formula_threshold_refs
```

## 16. AudienceSignalRecord

Purpose:

Stores audience or evaluator reaction metadata where allowed.

Fields:

```text
audience_signal_id
work_id
segment_id
source_type
rating_signal
review_theme
retention_or_dropoff_note
emotional_reaction_tags
cultural_context_note
```

## 17. GenreEngineRecord

Seeded from:

- Tragic_Engine
- genre-specific rendering modules

Fields:

```text
genre_engine_id
work_id
genre_mode
engine_name
expected_arc_shape
conflict_rules
emotional_rules
ending_rules
variation_notes
```

## 18. FormulaSignalRecord

Purpose:

Connect formulas to corpus fields.

Fields:

```text
formula_signal_id
formula_id
source_record_id
source_record_type
input_fields
output_signal
confidence
explanation
critic_mapping_ref
```

## 19. RelationshipGraphRecord

Purpose:

Supports CIM and multi-character interaction modeling.

Fields:

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

## 20. Integration targets

This schema supports:

- formula_to_corpus_mapping_blueprint
- Value Proof fixture
- LearnableCritic calibration
- Writer IDE story memory
- multi-agent critic supervision
- future execution engine entry

## 21. Open questions

- Should DramaEntryRecord be a first-class record or adapter only?
- Should SceneBlueprintRecord support raw text snippets or metadata only?
- Which source classes can feed Value Proof?
- Which records are sufficient for the first corpus fixture?
- Should film and drama use the same segment model?

## 22. Final decision

This schema v0.1 is accepted as a planning seed.

Implementation remains blocked until source policy, fixture spec, and entry criteria are approved.
