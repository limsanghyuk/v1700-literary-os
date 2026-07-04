# LLMRendererPromptPacket Schema v1 Report

Date: 2026-07-04  
Status: Stage243 P5 schema completed  
Scope: LLMRendererPromptPacket / SceneBlueprint handoff / Full-Series Creative OS roadmap

## 0. Executive Summary

This work completes the fifth schema step in the updated Full-Series Creative OS roadmap.

Created artifact:

```text
release/current/season_wiring_pack/llm_renderer_prompt_packet_schema_v1.json
```

This schema defines how `SceneBlueprint` payloads are packaged into controlled prompt packets for a future LLM renderer.

The packet is not live generation. It is a controlled handoff contract.

## 1. Roadmap Position

This task corresponds to:

```text
P5. LLMRendererPromptPacket schema
```

It follows:

```text
P1. FullSeriesArcSpec / SeasonPlan schema
P2. EpisodeArcChain schema
P3. SequenceBlueprint schema
P4. SceneBlueprint schema
```

It precedes:

```text
P6. FullSeasonCandidatePackage schema
```

## 2. Work Method

ChatGPT directly performed:

```text
schema architecture
field contract design
SceneBlueprint-to-renderer handoff modeling
renderer role boundary design
context stack design
prompt directive design
continuity and hard-rule constraint design
revision hook design
Stage243 safety boundary encoding
remote GitHub hub loading
```

Codex-local work was not required for this schema-design step.

## 3. Prompt Packet Purpose

The schema defines the bridge:

```text
SceneBlueprint
→ LLMRendererPromptPacket
→ future controlled prose rendering
```

The renderer packet must tell the renderer:

```text
what to write
why the scene exists
what must change
what must be preserved
what must be avoided
what context must be respected
what output format is expected
what revision hooks should be retained
```

The renderer must not invent the long-range structure from scratch.

## 4. Required Top-Level Sections

The schema requires:

```text
schema_version
authority
source_refs
packet_identity
renderer_role_contract
generation_scope
context_stack
scene_blueprint_payloads
prompt_directives
continuity_constraints
must_include_payloads
must_avoid_payloads
hard_rule_constraints
output_format_request
revision_hooks
safety_boundary
promotion_interpretation
```

## 5. Renderer Role Contract

The schema requires an explicit split between:

```text
planner_responsibility
renderer_responsibility
```

It also requires:

```text
long_range_structure_locked: true
raw_corpus_use_allowed: false
```

This prevents the renderer from replacing the full-series structure with improvised structure.

## 6. Context Stack

The packet must include:

```text
series_context_summary
season_context_summary
episode_context_summary
sequence_context_summary
prior_continuity_summary
next_continuity_requirement
```

This ensures the renderer receives enough context to render a scene without inventing the macro plan.

## 7. Scene Payloads

Each payload includes scene-level fields such as:

```text
scene_id
scene_order
scene_function_core
scene_function_core2
scene_purpose
scene_objective
dramatic_conflict
entry_state
exit_state
required_state_change
causal_input
causal_output
information_reveal
emotional_turn
dialogue_intention
subtext_target
visual_or_directorial_notes
ending_hook_or_transition
renderer_prompt_constraints
scene_necessity_claim
```

## 8. Control Constraints

The schema separates constraints into:

```text
continuity_constraints
must_include_payloads
must_avoid_payloads
hard_rule_constraints
```

This allows the renderer prompt to be strict enough for continuity, while still leaving room for prose rendering later.

## 9. Output Format and Revision Hooks

The schema includes:

```text
output_format_request
revision_hooks
```

This means the future renderer output can be reviewed, compared, revised, or regenerated using the same evaluation-aligned loop.

## 10. Boundary Encoding

The schema encodes the Stage243 boundary:

```text
fixture_only: true
metadata_only: true
provider_call_count: 0
runtime_generation: false
draft_text_exported: false
actual_provider_call_allowed: false
actual_prose_generation_allowed: false
raw_source_allowed: false
canonical_mutation_allowed: false
training_update_allowed: false
promotion_claim: false
```

Therefore this schema does not open Page18 runtime and does not authorize prose generation.

## 11. Promotion Interpretation

This schema is not promotion evidence by itself.

```text
Macro Planner Promotion = BLOCKED
Full Author Promotion = BLOCKED
Live Generation Readiness = BLOCKED
```

It is a foundation contract for future renderer handoff and full-season candidate packages.

## 12. Development Impact

The system now has the following schema chain foundation:

```text
FullSeriesArcSpec
→ SeasonPlan
→ EpisodeArcChain
→ SequenceBlueprint
→ SceneBlueprint
→ LLMRendererPromptPacket
```

This completes the planning-to-renderer-packet foundation before full-season candidate packaging.

## 13. Hub Loading and Push State

This work was loaded to the remote GitHub branch:

```text
repository: limsanghyuk/v1700-literary-os
branch: corpus-absorption-formula-bridge-handoff
```

The work is considered pushed to the remote hub once the GitHub contents API commit is created and remote fetch verification succeeds.

## 14. Next Required Step

The next roadmap step is:

```text
P6. FullSeasonCandidatePackage schema
```

Recommended next artifact:

```text
release/current/season_wiring_pack/full_season_candidate_package_schema_v1.json
```

It should package FullSeriesArcSpec, SeasonPlan, EpisodeArcChain, SequenceBlueprint, SceneBlueprint, LLMRendererPromptPacket, hard-rule checks, scorecard preflight, and revision plan into one reviewable candidate structure.

## 15. Final Decision

Stage243 P5 is completed at the schema-design level.

The next direct ChatGPT task should create `full_season_candidate_package_schema_v1.json` unless local fixture validation is requested first.
