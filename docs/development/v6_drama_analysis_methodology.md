# V6 Drama Analysis Methodology

Date: 2026-07-06
Status: handoff standard
Scope: Korean drama source archive analysis into Claude-compatible base outputs plus V1700 extended evidence layers.

## 1. Objective

The V6 method produces a developer-ready analysis package from a drama source archive.

Required result:

```text
close-reading analysis
+ Claude-compatible base structure
+ V1700 extended layers
+ strict validation report
```

The method was created after failures in earlier versions:

```text
v0: structure only
v1: multi-agent form but shallow grounding
v2: content-grounded candidate
v3: extension layers but template-like wording failures
v4: close-reading repair but extension priority was weakened
v5: extension restored but Dokkaebi comparison exposed calibration defects
v6: calibrated close-reading plus V1700 extension
```

## 2. Required base structure

The package must preserve the Claude-style base directories:

```text
authored/
authored_seq/
authored_arc/
```

Required base artifacts:

```text
SceneCard
SequenceBlueprint
EpisodeArc
SeriesArc
```

SceneCard required fields:

```text
work_id
scene_no
heading
title
intent_gist
core
core2
skin
by
```

SequenceBlueprint required fields:

```text
seq_id
work_id
episode_no
seq_index
member_scene_nos
scene_span
scene_budget
sequence_intent
goal
obstacle
value_shift
turn_type
turn_class
core_mix
pov_char
place_cluster
runtime_share
by
```

EpisodeArc required fields:

```text
work_id
episode_no
sequence_count
scene_count
turning_point
act_structure
by
entry_state
exit_state
central_conflict_axis
episode_function
dramatic_question
core_dist
```

## 3. Required V1700 extension layers

The final package must also include:

```text
agent_votes/
agent_votes_v1700/
arbiter/
boundary_decisions/
sequence_boundary_decisions/
eat8d/
evaluation_packets/
graph_advisory/
ledgers/
renderer_packet_bindings/
validation/
quality/
original_extracted/
```

Mandatory ledgers:

```text
plant_payoff_ledger.json
character_arc_ledger.json
relationship_arc_ledger.json
causal_spine_ledger.json
hook_chain_ledger.json
genre_rhythm_ledger.json
```

## 4. Episode extraction rule

Episode authority must be resolved in this order:

```text
1. file name marker
2. archive path marker
3. document heading marker
4. body marker
5. sequential fallback with warning
```

The Dokkaebi v5 failure showed that body-internal numbers can be mistaken for episode numbers. V6 therefore uses file name and path markers before body markers.

## 5. Scene boundary rule

Scenes must be separated by story function, not by fixed length.

Boundary signals:

```text
place change
time change
character group change
conversation objective change
action objective change
information reveal
misbelief creation or correction
relationship shift
emotional polarity shift
fantasy-rule activation
threat or dilemma escalation
sequence-turn event
```

If source scene markers exist, retain them as evidence. Long source scenes may still be split into internal beats when the dramatic function changes.

## 6. Core classification rule

Do not classify by keyword alone. Classify by dominant dramatic function.

Core vocabulary:

```text
ESTABLISH
INTRO
DESIRE
BOND
CONFLICT
REVELATION
ORACLE
PERIL
LOSS
RELIEF
REVERSAL
RESCUE
REUNION
PUNISH
HOOK
ROMANCE
```

Dokkaebi v5 failed because fantasy-rule keywords were overclassified as ORACLE. V6 repairs this:

```text
ORACLE is only used when the scene mainly explains or enforces a rule, prophecy, contract, or metaphysical condition.
If the fantasy element is used for romance, loss, desire, bond, peril, or revelation, classify by that dramatic function instead.
```

## 7. Sequence rule

A sequence is not a fixed number of scenes. It is a goal-obstacle-turn unit.

A valid sequence must have:

```text
goal
obstacle
value_shift
turn_type
turn_class
core_mix
pov_char
place_cluster
```

Reject if sequence goals, obstacles, POV, or place clusters collapse into generic repeated values.

## 8. EAT8D advisory tensor

EAT8D dimensions:

```text
SP: Suspense Pressure
RU: Reveal Urgency
ET: Emotional Turbulence
RD: Relational Disequilibrium
AG: Agency Gradient
DL: Dilemma Load
PD: Plot Density
AT: Arc Trajectory Alignment
```

Each scene receives 0.0 to 1.0 values. These are advisory diagnostics, not hard pass/fail scores. Genre affects normal ranges.

## 9. GraphAdvisory rule

GraphAdvisory must distinguish:

```text
real contradiction
intended mystery
character misbelief
audience information advantage
reveal deferral
continuity dependency
```

Do not treat intended mystery or delayed reveal as a plot hole.

## 10. Calibration workflow

When the same drama has a Claude reference package:

```text
1. analyze the original source with V6
2. compare with Claude reference
3. identify systematic defects
4. repair classification and boundary policy
5. re-run analysis
6. transfer repaired policy to another work
```

Dokkaebi is the calibration work. My Girlfriend Is a Gumiho is the transfer work.

## 11. Quality gate

A developer-ready package should pass:

```text
JSON parse errors: 0
JSONL parse errors: 0
base directories present
extension directories present
known repeated template phrase count: 0
known grammar error count: 0
generic heading count: 0 or explained
unique title ratio high
unique intent ratio high
max intent repetition low
sequence goal diversity pass
sequence obstacle diversity pass
place cluster diversity pass
ORACLE overclassification check pass
raw source export disabled
provider call count honestly recorded
training update claim false
adapter promotion claim false
P9 promotion claim false
```

## 12. Package naming

Use:

```text
{work_id}_seqcard_analysis_v6_calibrated_close_reading_v1700_extended_{YYYYMMDD}.zip
```

## 13. Final invariant

A final package must satisfy all four conditions:

```text
Claude base structure preserved
close-reading content quality repaired
V1700 extension layers included
strict validation report included
```

If one condition is missing, label the result as candidate, not final.
