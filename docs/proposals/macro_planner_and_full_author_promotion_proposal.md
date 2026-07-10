# Macro Planner & Full Author Promotion Proposal

Date: 2026-07-02  
Status: Stage243 proposal / promotion framework  
Scope: metadata-only planning, gate definition, and roadmap alignment

## 0. Executive Summary

This proposal records the Stage243 discussion about two future promotion claims for GPT V1700 Literary OS:

```text
1. Macro Planner Promotion
2. Full Author Promotion
```

The current conclusion is explicit:

```text
Macro Planner Promotion = BLOCKED until structural generation and blind evaluation evidence exists.
Full Author Promotion = BLOCKED until generation, gate, panel, revision, and full-season value proof exist.
```

Stage243 is not a live generation stage. Stage243 remains:

```text
Data Bridge + Learning Bridge + Season Wiring Preflight
```

The purpose of this document is not to declare promotion. The purpose is to define what evidence must exist before promotion can be claimed.

## 1. Current Evidence Baseline

### 1.1 Confirmed Assets

| Asset | Role | Current Status |
|---|---|---|
| `corpus_ko` | Local Korean drama/film structural corpus | Page27 Data Bridge substrate |
| `seqcard_ko` | Scene function / intent metadata | Scene Function layer; snapshot refresh needed |
| Claude 16 taxonomy | Scene function core labels | Keep as core taxonomy |
| `4070_oneclick` | SP-E.10 Path B v3 learning evidence | craft-axis evidence only |
| Pass1-Pass3 | Premise, causality, scene brief contracts | prototype ready |
| Pass4-Pass7 | Retrieval, draft, gate, panel/reward contracts | required for Stage243 preflight |

### 1.2 Confirmed Boundaries

The 4070 evidence supports:

```text
LLM-1 craft critic / show-vs-flat-tell axis
```

It does not support:

```text
16/24-episode macro planner promotion
full author promotion
live generation readiness
```

The Page18 boundary hardening rule remains active:

```text
No raw scripts.
No full JSONL text rows.
No source archives.
No embedding arrays.
No token files or API keys.
No adapter weights.
No model checkpoints.
No live provider call.
No runtime training.
No canonical mutation.
```

## 2. Promotion Terms

### 2.1 Macro Planner

A Macro Planner is the system component capable of designing long-form narrative structure before prose execution.

It must produce and validate:

```text
season arc
series premise
episode arc map
scene grid
conflict escalation curve
plant/payoff chain
reveal timing
character arc trajectory
relationship arc trajectory
episode-ending hook sequence
midpoint / crisis / climax placement
```

A macro planner is not required to produce final prose. It must prove structural planning ability.

### 2.2 Full Author

A Full Author is the system capable of executing the whole authoring loop:

```text
design
→ scene brief
→ retrieval
→ draft
→ structural gate
→ critic/panel reward
→ revision instruction
→ revised draft
→ accepted/rejected signal
→ measured learning signal
```

A full author must prove not only structure, but also scene-level craft, dialogue, style, evaluation, revision, and long-range consistency.

## 3. Agent Council Findings

### 3.1 Chief Principal Architect

Macro Planner and Full Author are separate promotion levels. They must not be merged.

Recommended ladder:

```text
Level 0: Scene Function Classifier
Level 1: Scene Brief Planner
Level 2: Episode Planner
Level 3: Season Macro Planner
Level 4: Draft Author
Level 5: Revision Author
Level 6: Full Author
```

Current Stage243 work prepares Level 3 evidence and the contracts for Level 4-6.

### 3.2 Chief Principal Compiler

Literary concepts must be compiled into strict schemas and pass contracts. Current Pass1-Pass3 are insufficient for full author claims.

Current:

```text
Pass1 premise -> WorkSpec
Pass2 causality -> Beat[]
Pass3 scene brief -> SceneBrief[]
```

Required:

```text
Pass4 RetrievalPacket
Pass5 DraftPacket
Pass6 GateResult
Pass7 PanelResult
```

### 3.3 Main Writer

Claude's 16 scene functions are valuable but incomplete for season authorship. They answer:

```text
What does this scene do?
```

A writer also needs:

```text
Why is this scene necessary now?
What does it change?
What does it plant?
What does it pay off?
Whose belief changes?
What later event depends on it?
Can this scene be removed or merged?
```

### 3.4 Sub Writer

Full Author Promotion requires actual generation and revision traces, not only analysis. The minimum loop is:

```text
scene_brief -> draft -> gate -> panel -> revision_instruction -> revised_draft -> accepted_or_rejected
```

### 3.5 Literary Critic

Evaluation must separate structural quality from prose/craft quality.

Required evaluation modes:

```text
Macro Blind Evaluation: evaluates only the design packet.
Scenario Blind Evaluation: evaluates generated scenes and prose/craft.
Revision Evaluation: evaluates whether revision improves the work.
```

### 3.6 Director / Drama Director

Drama authorship needs staging and episode propulsion, not only plot labels.

Required additions:

```text
visual objective
location function
entrance / exit logic
cut point
episode ending image
reveal staging
emotional close-up point
action geography
episode-to-episode propulsion
subplot braid density
```

### 3.7 Principal Systems Engineer

All evidence must be machine-readable, safe, parseable, and promotion-bounded.

Every evidence artifact must state:

```text
raw_text_exported
raw_vectors_exported
token_exported
adapter_weight_exported
provider_called
runtime_training_started
canonical_mutation_started
```

### 3.8 Data Steward

The next data bridge artifacts are mandatory:

```text
manifest_v2.json
schema_registry.json
seqcard_corpus_linkage_v2.json
scene_function_taxonomy_16.json
macro_analysis_layer_schema.json
```

### 3.9 Evaluation Scientist

Promotion requires three evidence classes:

```text
1. Structural Evidence
2. Generative Evidence
3. Revision Evidence
```

Macro Planner Promotion needs structural evidence. Full Author Promotion needs all three.

## 4. Claude 16 Scene Function Core Taxonomy

The Claude taxonomy is kept as the core scene-function vocabulary:

```text
ESTABLISH
ORACLE
INTRO
BOND
CONFLICT
REVERSAL
LOSS
PUNISH
REVELATION
REUNION
RELIEF
ROMANCE
PERIL
RESCUE
DESIRE
HOOK
```

Operational meanings:

| Code | Function | Core Question |
|---|---|---|
| `ESTABLISH` | establish setting/status/rules | What is the current order? |
| `ORACLE` | omen/forecast/foreshadow | What future shadow is planted? |
| `INTRO` | introduce new element | What new person/place/problem enters? |
| `BOND` | build relationship | Who becomes connected? |
| `CONFLICT` | create opposition | Who or what collides? |
| `REVERSAL` | reverse state/knowledge/power | What turns upside down? |
| `LOSS` | cause loss | What is lost? |
| `PUNISH` | impose consequence | What price is paid? |
| `REVELATION` | reveal hidden information | What truth emerges? |
| `REUNION` | reconnect separated lines | Who/what meets again? |
| `RELIEF` | release pressure | Where does tension ease? |
| `ROMANCE` | move romantic line | How does attraction/jealousy/love move? |
| `PERIL` | create danger | What is at risk now? |
| `RESCUE` | save or escape | Who/what is rescued? |
| `DESIRE` | expose want/goal | What does the character want? |
| `HOOK` | pull next scene/episode | What unresolved question remains? |

## 5. GPT V1700 Macro Analysis Layers

The 16 functions are not enough for macro promotion. GPT V1700 adds the following layers:

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

### 5.1 Layer Purpose Matrix

| Layer | Purpose | Promotion Role |
|---|---|---|
| Identity | locate work/episode/scene | required for linkage |
| Scene Function | define scene function | core taxonomy |
| Episode/Season Position | locate structural position | macro planner |
| Causality | link cause/effect | macro planner |
| Plant/Payoff | track foreshadow/reveal/payoff | macro planner |
| Character Arc | track belief/want/status change | macro planner/full author |
| Relationship Arc | track trust/power/intimacy shifts | macro planner/full author |
| Conflict System | track conflict type/intensity/escalation | macro planner |
| Tension/Genre Rhythm | regulate pacing and genre pressure | macro planner/full author |
| Scene Necessity | detect redundancy/cut risk | editor function |
| Dialogue/Style Craft | evaluate prose and dialogue | full author |
| Retrieval Linkage | retrieve metadata-only references | Pass4 |
| Gate/Panel/Revision | evaluate and improve draft | Pass6/Pass7/full author |

## 6. Promotion Gates

### Gate A — Macro Planner Candidate

Minimum evidence:

```text
50 works or equivalent structural diversity
1,000 episodes or equivalent episode-level metadata
70,000 scene function records
seqcard_corpus_linkage_v2
schema_registry
season arc + episode arc + scene grid generation packets
```

Gate A does not promote the model. It creates a candidate.

### Gate B — Macro Planner Promotion

Minimum evidence:

```text
30 new seeds
15 generated 16-episode design packets
15 generated 24-episode design packets
blind structural evaluation pass
reveal/payoff consistency pass
character arc continuity pass
baseline planner comparison pass
failure case review complete
```

### Gate C — Full Author Candidate

Minimum evidence:

```text
Pass4-Pass7 implemented
10,000 scene_brief -> draft records
10,000 gate results
10,000 panel results
5,000 revision traces
accepted/rejected registry
craft-axis evidence separated from macro evidence
```

### Gate D — Full Author Promotion

Minimum evidence:

```text
10 full 16-episode simulations
5 full 24-episode simulations
long-range causality audit pass
character arc continuity audit pass
prose/dialogue blind evaluation pass
revision loop improvement shown
human/mixed critic panel pass
value proof packet complete
```

## 7. Roadmap Impact

### Stage243-A — Data Bridge Finalization

```text
manifest_v2.json
schema_registry.json
seqcard_corpus_linkage_v2.json
scene_function_taxonomy_16.json
macro_analysis_layer_schema.json
```

### Stage243-B — Promotion Evidence Framework

```text
promotion_gate_definition.json
promotion_evidence_registry.json
macro_full_author_blocker_report.md
```

### Stage243-C — Season Wiring Contract

```text
RetrievalPacket
DraftPacket
GateResult
PanelResult
```

### Stage244 — Macro Planner Candidate

```text
season arc generator
episode arc generator
scene grid generator
plant/payoff chain generator
character arc trajectory generator
```

### Stage245 — Macro Planner Evaluation

```text
blind structural evaluation
baseline comparison
failure case review
promotion decision
```

### Stage246 — Full Author Candidate

```text
draft generation
gate
panel
revision loop
accepted/rejected registry
```

### Stage247 — Full Author Value Proof

```text
full season simulation
human/mixed panel
long continuity audit
style/dialogue evaluation
promotion decision
```

## 8. Final Decision

The council decision is:

```text
1. Keep Claude 16 taxonomy as the Scene Function Core.
2. Add GPT V1700 macro analysis layers above it.
3. Treat macro planner and full author as separate promotions.
4. Do not promote now.
5. Build the evidence gates first.
6. Stage243 remains metadata-only bridge/preflight.
```

The strategic conclusion:

```text
Stage243 is not a promotion stage.
Stage243 is the stage that builds the evidence machinery that makes future promotion legitimate.
```
