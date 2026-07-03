# GPT V1700 Full-Series Creative OS Consolidated Master Plan

Date: 2026-07-03  
Status: consolidated planning authority supplement  
Scope: Stage243 and later / Full-Series Arc / Episode Arc / Sequence Blueprint / Scene Blueprint / Controlled Prose Generation

## 0. Purpose

This document consolidates the current GPT V1700 Literary OS direction after the latest architecture corrections.

It does not replace the existing `docs/planning/gpt_v1700_integrated_master_plan.md`.

It extends that plan by clarifying the complete goal hierarchy:

```text
Full Series Arc / SeasonPlan
→ EpisodeArcChain
→ SequenceBlueprint
→ SceneBlueprint
→ LLMRendererPromptPacket
→ Detailed Scene Prose Generation
→ Episode Manuscript Assembly
→ Full Season Manuscript Assembly
→ Evaluation / Revision / Regeneration / Learning Signal
```

## 1. Existing Authority Considered

The existing integrated master plan defines the North Star:

```text
GPT V1700 is not merely a script generator.
It must embed the thinking, judgment, creation, criticism, revision, and measured learning loop of a human writer team into an autonomous literary generation operating system.
```

The existing writer-team loop remains valid:

```text
Seed / Prompt
→ Synopsis Assembler
→ WorldSpec / ThemeSpec / CharacterSpec
→ CausalSpine
→ SeasonPlan
→ EpisodePlan
→ SceneBeatGrid
→ Page18 Generation Boundary
→ Scene Output Metadata
→ Page20 Value Proof
→ Revision Proposal
→ Human Approval
→ Page28 Measured Learning
→ Next Improvement
```

The existing Stage243 boundary also remains valid:

```text
Stage243 = Season Wiring + Data/Learning Bridge Stage
```

During Stage243, actual live provider generation, output capture, canonical mutation, runtime training, adapter promotion, raw text export, and raw vector export remain blocked.

## 2. Corrected Final Goal

The correct final goal is not limited to evaluation, sequence design, scene blueprinting, or prompt packet generation.

The correct final goal is:

```text
GPT V1700 must become a full-series long-form creative operating system that can first plan and compose the entire 16-episode or 24-episode drama arc, then decompose it into episodes, sequences, scenes, and renderer-ready prompt packets, and ultimately generate, evaluate, revise, and regenerate detailed scene prose and full season manuscripts under controlled boundaries.
```

Therefore, the system has two linked goal layers.

### 2.1 First Goal Layer — Full-Series Planning and Blueprinting

GPT V1700 must be able to create:

```text
FullSeriesArcSpec
SeasonPlan
EpisodeArcChain
EpisodePlan
SequenceBlueprint
SceneBlueprint
LLMRendererPromptPacket
RevisionInstructionPlan
```

This first layer defines what must be written, why it must be written, how it is structured, and how a renderer should produce it.

### 2.2 Second Goal Layer — Detailed Prose and Manuscript Generation

The ultimate goal is to use the first layer to create:

```text
DetailedSceneDraft
RevisedSceneDraft
EpisodeManuscript
FullSeasonManuscript
EvaluationReport
RevisionPlan
RegenerationPlan
LearningSignalPacket
```

This second layer must remain controlled by Page18 boundaries and later proof gates.

## 3. Core Architecture

The architecture must support both top-down generation and bottom-up verification.

### 3.1 Top-Down Generation

```text
FullSeriesArc
→ EpisodeArc
→ Sequence
→ Scene
→ Prose
```

The system must start with the full series arc, not with isolated scene prompts.

### 3.2 Bottom-Up Verification

```text
Scene necessity
→ Sequence purpose
→ Episode coherence
→ Season arc integrity
```

The system must verify that each lower-level unit supports its parent structure.

## 4. Role Separation

### 4.1 GPT V1700 Macro Creative Planner

GPT V1700 is responsible for:

```text
full series arc planning
season premise and dramatic question
episode-by-episode escalation
sequence purpose and structure
scene function and necessity
causal spine continuity
plant/payoff management
character and relationship arc continuity
conflict escalation
hook scheduling
genre rhythm control
renderer-ready prompt packet design
hard-rule self-check
revision planning
learning signal packaging
```

### 4.2 Latest LLM Renderer

A latest LLM renderer may later be responsible for:

```text
detailed prose expansion
dialogue rendering
action description
emotional texture
scene atmosphere
rhythm and pacing
style rendering
```

However, the renderer must not be asked to invent the full series structure from scratch.

## 5. Evaluation-Aligned Composition

The evaluation system must directly shape the composition system.

```text
Evaluation criterion
→ Composition obligation
→ Self-check
→ Revision plan
→ Candidate package
```

The required mapping is:

```text
season_goal_clarity -> SeasonGoalConstructor -> SeasonGoalSpec
episode_arc_coherence -> EpisodeArcConstructor -> EpisodeArcChain
scene_grid_necessity -> SceneGridConstructor -> SceneFunctionGrid
causal_spine_integrity -> CausalSpineBuilder -> CausalSpineGraph
plant_payoff_integrity -> PlantPayoffLedger -> PlantPayoffLedger
character_arc_continuity -> CharacterArcTrajectoryBuilder -> CharacterArcTrajectory
relationship_arc_continuity -> RelationshipArcMatrix -> RelationshipArcMatrix
conflict_escalation -> ConflictEscalationScheduler -> ConflictEscalationCurve
hook_sequence_quality -> EpisodeHookScheduler -> EpisodeHookSchedule
genre_rhythm_balance -> GenreRhythmController -> GenreRhythmPlan
```

## 6. Required Constructor Pipeline

The current constructor sequence is:

```text
1. Theme / Genre / Season Goal input
2. SeasonGoalSpec
3. CausalSpineGraph
4. CharacterArcTrajectory
5. RelationshipArcMatrix
6. PlantPayoffLedger
7. ConflictEscalationCurve
8. EpisodeArcChain
9. SceneFunctionGrid
10. EpisodeHookScheduler
11. GenreRhythmController
12. Hard-Rule Self-Check
13. Scorecard Preflight
14. Revision Plan
15. Candidate Package
```

This constructor pipeline exists inside the larger full-series hierarchy.

## 7. Blueprint and Renderer Handoff Layer

After the macro candidate package is composed, the system must create:

```text
SequenceBlueprint
SceneBlueprint
LLMRendererPromptPacket
```

This handoff layer must tell the renderer:

```text
what to write
why the sequence or scene exists
what must change
what must be preserved
what must be avoided
what information is revealed or withheld
what emotional and relationship shift occurs
what output format must be produced
what revision hooks are required
```

The renderer prompt must not ask the LLM to invent long-range structure from scratch.

## 8. Current Stage243 Boundary

Stage243 is not a live-generation or full-author promotion stage.

Currently allowed:

```text
metadata-only manifests
schema contracts
fixture-only candidate packages
blueprint contracts
prompt packet schemas
self-check reports
scorecard preflight reports
revision plans
hub authority records
```

Currently blocked:

```text
actual_scene_prose
provider_generated_scene
full_episode_manuscript
full_season_manuscript
verbatim_source_text
raw_drama_script
canonical_memory_mutation
runtime_training_update
adapter promotion
promotion_claim
```

Safety invariants remain:

```text
provider_call_count: 0
runtime_generation: false
raw_text_exported: false
raw_vectors_exported: false
draft_text_exported: false
token_exported: false
adapter_weight_exported: false
promotion_claim: false
```

## 9. Current Hub Context Incorporated

The following recent hub decisions are incorporated:

```text
1. ChatGPT/Codex work division protocol
2. SeqCard v4 metadata-only snapshot analysis
3. Local/remote SeqCard v4 reconciliation
4. Macro Planner Hard-Rule Gate and Candidate Evaluation v2
5. Macro Planner Candidate Composition Contract v1
6. Sequence / Scene Blueprint Generator Contract v1
7. Full Series Arc Goal Alignment
```

## 10. Updated Roadmap

The correct development order is now:

```text
P0. Authority and safety split maintained
P1. FullSeriesArcSpec / SeasonPlan schema
P2. EpisodeArcChain schema
P3. SequenceBlueprint schema
P4. SceneBlueprint schema
P5. LLMRendererPromptPacket schema
P6. FullSeasonCandidatePackage schema
P7. Fixture-only Full Series Candidate Package
P8. Hard-Rule Self-Check across full season
P9. Scorecard Preflight
P10. Gate A Review Packet
P11. Heldout / Negative-Control Evaluation
P12. Page18 controlled prose generation preparation
P13. Controlled detailed scene prose generation
P14. Episode manuscript assembly
P15. Full season manuscript assembly
P16. Evaluation / Revision / Regeneration loop
P17. LearningSignalPacket and measured improvement registry
```

## 11. Immediate Next Work

The next direct ChatGPT work should create the schema foundation:

```text
full_series_arc_spec_schema_v1.json
season_plan_schema_v1.json
episode_arc_chain_schema_v1.json
sequence_blueprint_schema_v1.json
scene_blueprint_schema_v1.json
llm_renderer_prompt_packet_schema_v1.json
full_season_candidate_package_schema_v1.json
```

Codex-local work is not required for these schema designs unless local fixture files must be parsed, scanned, or validated.

## 12. Promotion Interpretation

This document does not create promotion.

```text
Macro Planner Promotion = BLOCKED
Full Author Promotion = BLOCKED
Live Generation Readiness = BLOCKED
```

Promotion must ultimately be measured by the ability to repeatedly produce:

```text
coherent full season arcs
coherent episode chains
coherent sequence and scene blueprints
renderer-ready prompt packets
controlled detailed prose generation
revision improvement
heldout/negative-control separation
measured learning gains
```

## 13. Final Decision

The current unified direction is:

```text
GPT V1700 is a full-series long-form creative operating system.
It first plans the complete 16-episode or 24-episode dramatic arc.
It then decomposes the arc into episodes, sequences, scenes, and renderer-ready prompt packets.
It ultimately generates, evaluates, revises, and improves detailed scene prose and full season manuscripts under controlled boundaries.
```
