# Macro Planner / Full Author Promotion Discussion Summary

Date: 2026-07-02  
Status: loaded to Stage243 transition council pack  
Purpose: summarize the ChatGPT discussion and preserve it as hub context

## 0. One-Line Summary

```text
Claude's SeqCard data is a scene-function map; GPT V1700 must turn it into a season-scale planning and authoring evidence system.
```

## 1. What Was Discussed

The discussion focused on whether the current drama analysis method can produce evidence for:

```text
1. Macro Planner Promotion
2. Full Author Promotion
```

The conclusion is that these two claims are different and must be evaluated separately.

```text
Macro Planner Promotion = structural design capability.
Full Author Promotion = complete design, generation, evaluation, revision, and learning loop.
```

## 2. Meaning of Claude Data

Claude's data is not treated as text to imitate. It is treated as a structural map of scene function and intent.

It helps answer:

```text
What does this scene do inside the story?
```

It should not be used to copy source text. It should be used to learn function, position, rhythm, and structural necessity.

## 3. Claude 16 Scene Functions

The 16 core categories are retained:

```text
ESTABLISH, ORACLE, INTRO, BOND, CONFLICT, REVERSAL,
LOSS, PUNISH, REVELATION, REUNION, RELIEF, ROMANCE,
PERIL, RESCUE, DESIRE, HOOK
```

These are useful as the core scene-function taxonomy.

They are not enough for macro planning alone because they do not fully encode:

```text
season position
causality
plant/payoff
character change
relationship change
conflict escalation
tension rhythm
scene necessity
draft quality
revision outcome
```

## 4. GPT V1700 Required Expansion

The required GPT V1700 analysis layers are:

```text
Layer 0. Identity
Layer 1. Scene Function Core 16
Layer 2. Episode / Season Position
Layer 3. Causality
Layer 4. Plant / Payoff
Layer 5. Character Arc
Layer 6. Relationship Arc
Layer 7. Conflict System
Layer 8. Tension / Genre Rhythm
Layer 9. Scene Necessity
Layer 10. Dialogue / Style Craft
Layer 11. Retrieval Linkage
Layer 12. Gate / Panel / Revision
```

The key conceptual distinction is:

```text
Claude 16 = what the scene does.
GPT V1700 layers = why it is needed, where it belongs, what it changes, and whether the generated result succeeds.
```

## 5. Macro Planner Promotion Discussion

Macro planner capability can begin from drama analysis. The following evidence is relevant:

```text
scene function distribution
episode arc map
conflict escalation curve
reveal/payoff chain
character arc trajectory
relationship arc trajectory
episode ending hook pattern
midpoint/crisis/climax placement
```

However, analysis alone is not promotion evidence.

Macro Planner Promotion requires the system to generate new 16/24-episode design packets from unseen seeds and pass blind structural evaluation.

## 6. Full Author Promotion Discussion

Full Author Promotion cannot be obtained from analysis alone.

It requires a closed loop:

```text
design
→ scene brief
→ retrieval
→ draft
→ structural gate
→ critic/panel reward
→ revision instruction
→ revised draft
→ accepted/rejected
→ measured learning signal
```

This means Pass4-Pass7 are mandatory before full author evidence can exist.

## 7. Required Data Scale Estimates

The discussion proposed practical target ranges:

### Macro Planner Candidate

```text
15-30 works minimum for prototype
300-700 episodes
20,000-50,000 scene function records
4-6 genres
```

### Macro Planner Promotion Candidate

```text
50-100 works
1,000-2,000 episodes
70,000-150,000 scene function records
8-12 genres
arc/reveal/payoff/character trajectory annotations
```

### Full Author Candidate

```text
100-300 works
2,000-5,000 episodes
150,000-400,000 scene function records
10,000-50,000 scene brief -> draft pairs
5,000-30,000 preference/revision records
```

The central point is that full author requires revision/evaluation data, not just more source analysis.

## 8. Agent Council Consensus

The simulated council consensus was:

```text
1. Keep Claude 16 taxonomy.
2. Add GPT V1700 macro analysis layers.
3. Separate macro planner promotion from full author promotion.
4. Do not promote now.
5. Build evidence gates first.
6. Keep Stage243 metadata-only.
7. Use SeqCard and corpus data through safe linkage, not raw text.
```

## 9. Required Hub Artifacts

The discussion produced these required artifacts:

```text
docs/proposals/macro_planner_and_full_author_promotion_proposal.md
release/current/transition_council_pack/promotion_gate_definition.json
release/current/transition_council_pack/macro_full_author_blocker_report.md
release/current/data_foundry_pack/macro_analysis_layer_schema_plan.json
```

Recommended next additions:

```text
schema_registry.json
scene_function_taxonomy_16.json
seqcard_corpus_linkage_v2.json
promotion_evidence_registry.json
macro_planner_candidate_report.json
```

## 10. Final Decision

```text
Stage243 is not a promotion stage.
Stage243 is the stage that builds the machinery required to make future promotion legitimate.
```

Current official state:

```text
Macro Planner Promotion = BLOCKED
Full Author Promotion = BLOCKED
```

Required next state:

```text
Build the data bridge, schema registry, promotion gate registry, and Pass4-Pass7 preflight contracts.
```
