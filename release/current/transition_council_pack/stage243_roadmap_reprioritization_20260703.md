# Stage243 Roadmap Reprioritization: Evaluation-Aligned Composition

Date: 2026-07-03  
Status: roadmap update  
Scope: Stage243 Macro Planner / Evaluation-Aligned Generation / Candidate Composition

## 0. Executive Decision

The roadmap must be reordered.

Previously the next step after `Macro Planner Hard-Rule Gate and Candidate Evaluation v2` was:

```text
Stage243 Macro Planner Candidate Gate A Review Packet
```

That order is incomplete.

The correct next step is now:

```text
Stage243 Macro Planner Candidate Composition Contract v1
```

Reason:

```text
An evaluation system alone is not enough.
The same criteria must be converted into construction obligations so that the system learns to build season, episode, scene, causality, payoff, character, relationship, conflict, hook, and genre rhythm structures before they are evaluated.
```

## 1. User Direction Incorporated

The user direction is accepted as an architecture principle:

```text
Evaluation design must always consider the final goal: a system that can plan, compose, create, self-check, revise, and eventually generate long-form drama.
```

Therefore, every scoring dimension must have a matching constructor.

```text
Evaluation criterion -> Composition obligation -> Self-check -> Revision plan -> Candidate package
```

## 2. Current Completed Stage243 Work

Completed or accepted as current context:

```text
1. ChatGPT/Codex work division protocol
2. SeqCard v4 metadata-only snapshot analysis
3. Local/remote SeqCard v4 reconciliation
4. Macro Planner Hard-Rule Gate v2
5. Disqualification Rules v2
6. Macro Candidate Scorecard Schema v2
7. Macro Candidate Final Verdict Fixture v2
8. Macro Planner Evaluation v2 Report
9. Macro Planner Candidate Composition Contract v1
```

## 3. Reordered Roadmap

### P0 — Authority and Safety Split

Status: completed / maintained

```text
Local Hub Authority and Remote GitHub Authority must remain separated.
Raw corpus, ZIP, vectors, tokens, adapter weights, and provider outputs must not be committed.
```

### P1 — Evaluation Gate

Status: completed

```text
Macro Planner Hard-Rule Gate and Candidate Evaluation v2
```

Outputs:

```text
macro_planner_hard_rule_gate.json
macro_planner_disqualification_rules.json
macro_candidate_scorecard_schema.json
macro_candidate_final_verdict_fixture.json
macro_planner_evaluation_v2_report.md
```

### P2 — Evaluation-Aligned Composition Contract

Status: newly created / now current priority

```text
Macro Planner Candidate Composition Contract v1
```

Purpose:

```text
Convert evaluation criteria into generation-time structure-building obligations.
```

The required constructor sequence is:

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

### P3 — Composition Output Schemas

Status: next immediate work

Create:

```text
composition_output_schema_v1.json
composition_self_check_fixture_v1.json
macro_planner_candidate_package_schema_v1.json
```

Purpose:

```text
Make every constructor output machine-readable and evaluable.
```

### P4 — Candidate Package Fixture

Status: after P3

Create a fixture-only Macro Planner Candidate Package.

It must contain:

```text
SeasonGoalSpec
CausalSpineGraph
CharacterArcTrajectory
RelationshipArcMatrix
PlantPayoffLedger
ConflictEscalationCurve
EpisodeArcChain
SceneFunctionGrid
EpisodeHookSchedule
GenreRhythmPlan
HardRuleSelfCheckReport
ScorecardPreflightReport
RevisionPlan
```

It must not contain:

```text
actual prose
raw script text
provider-generated draft
live generation output
canonical mutation
training update
promotion claim
```

### P5 — Gate A Review Packet

Status: after P4

Only after composition contract and candidate package schema exist should the system create:

```text
Stage243 Macro Planner Candidate Gate A Review Packet
```

The Gate A packet should review candidate fixtures built according to the composition contract.

### P6 — Repeated Heldout / Negative-Control Evaluation

Status: later

Use:

```text
heldout fixtures
negative controls
hard-rule gate
scorecard schema
final verdict fixture
```

to determine whether candidate structures are robust enough for Gate A review.

### P7 — Page18 Controlled Generation Boundary Preparation

Status: later / still closed

Only after structural candidate packages repeatedly pass evaluation should Page18 controlled generation preparation be considered.

```text
Page18 runtime remains closed.
provider_call_count remains 0.
actual prose generation remains blocked.
```

## 4. Evaluation-to-Composition Principle

Each evaluation criterion now has a required construction counterpart:

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

## 5. Learning Rule

If test results outperform older formulas or expected structure, the learned pattern may be promoted only as a metadata-only rule after:

```text
1. evidence packet
2. hard-rule validation
3. heldout test
4. negative-control separation
5. authority review
6. hub loading
```

The system may learn structural rules from:

```text
aggregate scene-function distribution
core/core2 pair statistics
plant/payoff success/failure
hard-rule failure patterns
scorecard dimension deltas
revision success rates
heldout pass/fail outcomes
```

The system must not learn from:

```text
raw prose memorization
verbatim script extraction
unreviewed provider output
private token/model artifact
canonical mutation without approval
```

## 6. Promotion State

No promotion is created by this roadmap update.

```text
Macro Planner Promotion = BLOCKED
Full Author Promotion = BLOCKED
Live Generation Readiness = BLOCKED
```

## 7. Final Priority Order

The correct next sequence is:

```text
1. Composition Output Schemas v1
2. Composition Self-Check Fixture v1
3. Macro Planner Candidate Package Schema v1
4. Fixture-only Candidate Package generation
5. Gate A Review Packet
6. Heldout / Negative-Control Evaluation Loop
7. Only later: Page18 controlled generation preparation
```

## 8. Final Decision

The final goal must control every intermediate design.

Therefore:

```text
Evaluation must shape composition.
Composition must produce self-checkable structures.
Self-check must produce revision plans.
Revision must produce better candidate packages.
Only repeated evidence can support promotion review.
```
