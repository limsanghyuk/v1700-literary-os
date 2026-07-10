# Sequence / Scene Blueprint Purpose Alignment Report

Date: 2026-07-03  
Status: purpose alignment and roadmap correction  
Scope: GPT V1700 Macro Planner / Sequence Blueprint / Scene Blueprint / LLM Renderer Handoff

## 0. Executive Decision

GPT V1700 should not be optimized primarily as a freeform prose generator.

The current strategic purpose is:

```text
Build a long-form creative planning model that decides the sequence and scene design, writes the theme/purpose/content explanation for those sequences and scenes, divides them into concrete scene units, and produces renderer-ready prompt packets for a latest large language model to generate detailed prose later.
```

Therefore, the model's central product is not final prose but:

```text
SequenceBlueprint
SceneBlueprint
LLMRendererPromptPacket
RevisionInstructionPlan
```

## 1. Reasoning

Modern large language models are already strong at detailed prose expansion when they receive rich, specific, well-structured scene instructions.

Therefore, GPT V1700 should focus on what generic LLM prompting alone does not reliably solve:

```text
long-range structure
season-level goal
multi-episode causality
sequence purpose
scene necessity
plant/payoff management
character and relationship arc continuity
conflict escalation
hook scheduling
genre rhythm control
self-check and revision planning
```

The detailed prose renderer can be a later Page18-controlled LLM generation layer.

## 2. Correct Role Split

### GPT V1700 Macro Planner

Responsible for:

```text
what should happen
why it should happen
where it belongs in the long-form structure
what each sequence must accomplish
how many scenes are needed
what each scene must change
what information is revealed or withheld
what plant/payoff operation is active
what emotional and relationship movement occurs
what instructions the renderer must follow
```

### Latest LLM Renderer

Responsible later for:

```text
turning the blueprint into detailed prose
rendering atmosphere, dialogue, action, rhythm, and scene texture
following the constraints supplied by GPT V1700
```

The renderer must not be asked to invent the long-range structure from scratch.

## 3. Design Consequence

The previous composition pipeline remains valid, but a new handoff layer must be inserted before any actual prose generation:

```text
Macro Planner Candidate Package
→ SequenceBlueprint
→ SceneBlueprint
→ LLMRendererPromptPacket
→ Page18 Controlled Generation Boundary
→ Latest LLM Renderer Detailed Prose
```

During Stage243, only the blueprint and prompt packet may be created.

Actual prose generation remains blocked.

## 4. New Required Contract

Created artifact:

```text
release/current/season_wiring_pack/sequence_scene_blueprint_generator_contract_v1.json
```

This contract defines GPT V1700 as:

```text
long_form_macro_planner
sequence_architect
scene_blueprint_author
director_brief_generator
llm_renderer_prompt_packager
hard_rule_self_checker
revision_instruction_planner
```

It explicitly rejects defining GPT V1700 as:

```text
freeform_prose_generator
verbatim_drama_writer
raw_corpus_reproducer
unbounded_scene_drafter
```

## 5. Blueprint Hierarchy

The new hierarchy is:

```text
SeasonPlan
EpisodePlan
SequenceBlueprint
SceneBlueprint
LLMRendererPromptPacket
```

This allows the system to plan at long range and hand controlled creative instructions to a renderer model later.

## 6. Required Blueprint Fields

SequenceBlueprint must define:

```text
sequence_id
episode_id
sequence_title
sequence_purpose
sequence_theme_focus
sequence_dramatic_question
entry_state
exit_state
conflict_escalation_step
character_arc_delta
relationship_arc_delta
plant_payoff_operations
tone_and_genre_mode
directorial_intention
scene_count_target
scene_blueprint_refs
hard_rule_risks
renderer_handoff_summary
```

SceneBlueprint must define:

```text
scene_id
sequence_id
episode_id
scene_order
scene_function_core
scene_function_core2
scene_purpose
scene_objective
dramatic_conflict
character_entry_state
character_exit_state
relationship_delta
causal_input
causal_output
plant_operations
payoff_operations
information_reveal
emotional_turn
visual_or_directorial_notes
dialogue_intention
subtext_target
ending_hook_or_transition
renderer_prompt_constraints
hard_rule_self_check
```

LLMRendererPromptPacket must define:

```text
packet_id
renderer_model_family
generation_scope
do_not_use_raw_corpus
sequence_context_summary
scene_blueprints
style_directive
tone_directive
pov_or_camera_directive
dialogue_directive
subtext_directive
continuity_constraints
must_include_payloads
must_avoid_payloads
hard_rule_constraints
output_format_request
revision_hooks
```

## 7. Roadmap Correction

The latest priority order must be adjusted again:

```text
1. Composition Output Schemas v1
2. SequenceBlueprint / SceneBlueprint / RendererPromptPacket Schemas v1
3. Composition Self-Check Fixture v1
4. Sequence/Scene Blueprint Fixture v1
5. Macro Planner Candidate Package Schema v1
6. Fixture-only Candidate Package generation
7. Gate A Review Packet
8. Heldout / Negative-Control Evaluation Loop
9. Only later: Page18 controlled generation preparation
```

## 8. Boundary State

The following remain blocked:

```text
actual_scene_prose
provider_generated_scene
verbatim_source_text
raw_drama_script
canonical_memory_mutation
runtime_training_update
promotion_claim
```

The following remain false:

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

## 9. Promotion Interpretation

No promotion is created by this alignment report.

```text
Macro Planner Promotion = BLOCKED
Full Author Promotion = BLOCKED
Live Generation Readiness = BLOCKED
```

The system is now better aligned with the final goal:

```text
not merely evaluating stories,
not merely generating prose,
but planning long-form dramatic architecture and producing renderer-ready scene blueprints.
```

## 10. Final Decision

GPT V1700's Stage243 purpose is now clarified as:

```text
A long-form macro creative planner and sequence/scene blueprint generator that prepares structured prompt packets for future controlled LLM rendering.
```

The next direct ChatGPT work should create:

```text
sequence_blueprint_schema_v1.json
scene_blueprint_schema_v1.json
llm_renderer_prompt_packet_schema_v1.json
sequence_scene_blueprint_fixture_v1.json
```
