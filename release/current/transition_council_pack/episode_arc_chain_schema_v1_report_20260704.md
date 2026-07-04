# EpisodeArcChain Schema v1 Report

Date: 2026-07-04  
Status: Stage243 P2 schema completed  
Scope: EpisodeArcChain / SeasonPlan decomposition / Full-Series Creative OS roadmap

## 0. Executive Summary

This work completes the second schema step in the updated Full-Series Creative OS roadmap.

Created artifact:

```text
release/current/season_wiring_pack/episode_arc_chain_schema_v1.json
```

This schema defines how a `SeasonPlan` is decomposed into episode-to-episode state transitions before `SequenceBlueprint`, `SceneBlueprint`, `LLMRendererPromptPacket`, and later controlled prose generation.

## 1. Roadmap Position

This task corresponds to:

```text
P2. EpisodeArcChain schema
```

It follows:

```text
P1. FullSeriesArcSpec / SeasonPlan schema
```

It precedes:

```text
P3. SequenceBlueprint schema
P4. SceneBlueprint schema
P5. LLMRendererPromptPacket schema
P6. FullSeasonCandidatePackage schema
```

## 2. Work Method

### ChatGPT-direct work

Performed directly:

```text
schema architecture
field contract design
episode-to-episode dependency modeling
season-turn index design
plant/payoff reference design
character and relationship delta indexing
hook-chain contract design
Stage243 safety boundary encoding
remote GitHub hub loading
```

### Codex-local work

Not required for this step.

Reason:

```text
This was schema design work. It did not require local filesystem inspection, local DB parsing, archive scan, raw corpus scan, or local git status.
```

Codex-local work may be required later when actual local fixture instances are generated and need JSON schema validation, parsing, and leakage scanning.

## 3. EpisodeArcChain Schema Purpose

The schema defines the bridge between:

```text
SeasonPlan
→ EpisodeArcChain
→ SequenceBlueprint
```

Its purpose is to ensure that episodes are not isolated summaries.

Each episode must function as:

```text
a state transition inside the full season arc
a causal link in the season spine
a holder of plant/payoff operations
a carrier of character and relationship deltas
a hook source for the next episode
a decomposition source for sequence planning
```

## 4. Required Top-Level Sections

The schema requires:

```text
schema_version
authority
source_refs
chain_identity
episode_count
episode_nodes
inter_episode_dependencies
season_turn_index
plant_payoff_index
character_delta_index
relationship_delta_index
hook_chain
hard_rule_preflight
scorecard_preflight_targets
decomposition_targets
safety_boundary
promotion_interpretation
```

## 5. Episode Node Contract

Each episode node must define:

```text
episode
episode_title
episode_function
entry_state
exit_state
central_question
main_turn
irreversible_change
conflict_step
plant_operations
payoff_operations
character_deltas
relationship_deltas
genre_mode
ending_hook
sequence_targets
hard_rule_risks
```

This ensures each episode is not merely a plot summary but a structured transformation unit.

## 6. Dependency Link Contract

The schema defines inter-episode dependency links across:

```text
causal
information
emotional
relationship
plant_payoff
conflict
hook
```

This is required to prevent impossible episode order, payoff without plant, relationship shifts without event, and disconnected episode summaries.

## 7. Hard-Rule and Scorecard Alignment

The schema directly supports hard-rule preflight for:

```text
impossible_episode_order
causality_contradiction
orphan_plant_without_payoff
payoff_without_plant
character_arc_discontinuity
relationship_arc_discontinuity
episode_hook_absent_over_threshold
genre_rhythm_flatline
promotion_claim_detected
raw_text_leakage
```

It also aligns with scorecard dimensions:

```text
episode_arc_coherence
causal_spine_integrity
plant_payoff_integrity
character_arc_continuity
relationship_arc_continuity
conflict_escalation
hook_sequence_quality
genre_rhythm_balance
```

## 8. Boundary Encoding

The schema encodes the Stage243 boundary:

```text
fixture_only: true
metadata_only: true
provider_call_count: 0
runtime_generation: false
raw_text_exported: false
promotion_claim: false
actual_prose_allowed: false
provider_generation_allowed: false
raw_source_allowed: false
canonical_mutation_allowed: false
```

Therefore this schema does not open Page18 runtime and does not authorize prose generation.

## 9. Promotion Interpretation

This schema is not promotion evidence by itself.

```text
Macro Planner Promotion = BLOCKED
Full Author Promotion = BLOCKED
Live Generation Readiness = BLOCKED
```

It is a foundation contract for future full-season candidate packages.

## 10. Development Impact

The system now has the following schema chain foundation:

```text
FullSeriesArcSpec
→ SeasonPlan
→ EpisodeArcChain
```

This makes the full-series hierarchy operational before sequence and scene blueprinting.

## 11. Next Required Step

The next roadmap step is:

```text
P3. SequenceBlueprint schema
```

Recommended next artifact:

```text
release/current/season_wiring_pack/sequence_blueprint_schema_v1.json
```

It should define sequence-level dramatic purpose, entry/exit states, scene count target, character/relationship delta, conflict escalation step, plant/payoff operations, tone/genre mode, directorial intention, renderer handoff summary, and hard-rule risks.

## 12. Final Decision

Stage243 P2 is completed at the schema-design level.

The next direct ChatGPT task should create `sequence_blueprint_schema_v1.json` unless local fixture validation is requested first.
