# Formula to Corpus Mapping Blueprint

Status: blueprint draft
Created: 2026-06-07
Scope: connect normalized formulas to narrative corpus schema
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint maps V1700 formula groups to corpus schema fields so that formulas, corpus metadata, LearnableCritic records, and Value Proof metrics can operate on the same structured substrate.

It does not implement calculations. It defines the mapping layer required before implementation.

## 2. Inputs

Source planning documents:

- docs/reviews/formula_catalog_normalization_report.md
- docs/architecture/narrative_corpus_schema_v0_1.md
- docs/policies/narrative_corpus_source_policy.md
- docs/architecture/learnable_critic_bridge_blueprint.md
- docs/architecture/post_roadmap_value_proof_gate_blueprint.md

## 3. Mapping principles

- formulas must read structured fields, not uncontrolled raw text
- every formula signal must identify source records
- every formula output must be advisory until promoted by future authority
- coefficient learning requires audit and rollback
- source rights must be preserved
- Value Proof human evaluation remains external validation

## 4. Mapping table

| Formula group | Corpus input records | Corpus fields | Output signal | V1700 target |
|---|---|---|---|---|
| DRSE | SceneBlueprintRecord, CausalityMatrixRecord | scene_order, trigger, reaction, resolution, residue, emotional_start, emotional_end | state_transition_signal | NarrativeStateTensor, LearnableCritic |
| Narrative State Tensor | WorkRecord, CharacterRecord, SceneBlueprintRecord, RelationshipGraphRecord | genre_tags, desire, arc_phase, conflict_type, tension_delta, relationship edges | narrative_state_vector | Writer IDE right panel, Value Proof features |
| Narrative Fitness Score | SceneBlueprintRecord, CriticThresholdRecord, AudienceSignalRecord | tension_delta, information_delta, thresholds, rating_signal, review_theme | fitness_score | advisory metric, not final proof |
| Emotional Momentum | SceneBlueprintRecord, CharacterRecord | emotional_start, emotional_end, behavior_shift, pressure_source | emotional_momentum_delta | critic signal, scene revision hint |
| Character Interaction Matrix | CharacterRecord, RelationshipGraphRecord | node_refs, edge_refs, trust_level, conflict_level, hidden_dependency_note | interaction_pressure_matrix | continuity critic, writer IDE graph |
| Triangle Tension | CharacterRecord, CorePhilosophyRecord, RelationshipGraphRecord | desire, conflict_axis, moral_pressure, pressure_level | triadic_tension_signal | conflict critic, scene planning |
| RAG/BM25/RRF retrieval fusion | WorkRecord, SceneBlueprintRecord, CorePhilosophyRecord | title, genre_tags, master_theme, scene_function, conflict_type | retrieval_candidate_set | corpus reference panel, no rights bypass |
| Fourier tension curve | EpisodeOrChapterRecord, SceneBlueprintRecord | sequence_index, scene_order, tension_delta, turning_points | macro_tension_curve | value proof metric companion |
| Causal self-healing | CausalityMatrixRecord, KeyObjectRecord, SceneBlueprintRecord | trigger, resolution, residue, payoff_status, unresolved_debt | causality_gap_signal | advisory repair candidate |
| Governance authority formulas | release/current reports, manifest records | status, warnings, evidence refs, gate state | authority_integrity_signal | release readiness, entry criteria |

## 5. FormulaSignalRecord lifecycle

Recommended lifecycle:

```text
select source corpus records
validate source class and rights status
extract declared input fields
run formula or formula placeholder
emit FormulaSignalRecord
attach explanation
attach confidence
attach critic mapping ref
keep advisory until approval
```

## 6. Required FormulaSignalRecord fields

```text
formula_signal_id
formula_id
formula_group
source_record_ids
source_record_types
input_fields
source_class_summary
rights_status_summary
output_signal_type
output_signal_value
confidence
explanation
critic_mapping_ref
value_proof_mapping_ref
created_at
review_status
```

## 7. LearnableCritic connection

Formula outputs may feed LearnableCritic only through audited records.

Required path:

```text
FormulaSignalRecord
→ CriticInputSourceRecord
→ CoefficientStateRecord
→ CoefficientDiffRecord
→ DeterministicSeedRecord
→ AlignmentResultRecord
→ RollbackRecord
```

## 8. Value Proof connection

Formula outputs may be used in Arm B guidance only if preregistered.

Required preregistration fields:

```text
allowed_formula_groups
allowed_corpus_records
allowed_guidance_fields
hidden_context_policy
length_control_policy
```

Formula outputs must not leak arm labels to evaluators.

## 9. Writer IDE connection

Formula-to-corpus signals can appear in:

- story memory panel
- critic panel
- tension curve panel
- character graph panel
- rewrite candidate comparison panel

Rules:

- show source and explanation
- distinguish signal from canonical state
- require writer approval before canonical mutation

## 10. Multi-agent connection

Agents may reference formula signals only if they have capability scope.

Example mapping:

- Formula Critic -> all FormulaSignalRecord types
- Continuity Critic -> DRSE, causal self-healing, CIM
- Dialogue Critic -> DialogueFunctionRecord and style modules
- Emotion Critic -> Emotional Momentum and tension signals
- Rights Reviewer -> source_class and rights_status fields

## 11. Blocking failures

- formula reads unrestricted raw full text without approval
- source_class missing
- rights_status missing
- FormulaSignalRecord has no source record
- coefficient update happens without audit
- formula output becomes canonical story state without approval
- Value Proof arm receives unregistered formula guidance

## 12. Priority mappings for first fixture

First fixture should map only:

1. Narrative State Tensor
2. Emotional Momentum
3. Character Interaction Matrix
4. Causality Matrix / DRSE
5. Narrative Fitness companion metric

Reason:

These map directly to uploaded Master DB schema fields and can support early Value Proof experiments without needing a full runtime engine.

## 13. Final decision

Formula and corpus layers must be connected before V1700 opens execution-engine implementation.

The first implementation candidate should be a small metadata fixture, not a full writing engine.
