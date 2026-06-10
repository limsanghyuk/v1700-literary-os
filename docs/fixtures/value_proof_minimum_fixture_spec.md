# Value Proof Minimum Fixture Spec

Status: fixture spec draft
Created: 2026-06-07
Scope: post-roadmap value proof planning
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This spec defines the smallest controlled fixture for an early Value Proof experiment.

It is not a full proof of literary superiority. It is a minimum fixture to detect obvious design flaws before larger experiments.

## 2. Fixture goal

Test whether the V1700 structured pipeline produces a detectable preference signal over a pure LLM baseline under controlled conditions.

## 3. Minimum scale

```text
scenes: 10~15
evaluators: 2~3
arms: A and B required, C optional
timebox: limited MVE window
```

## 4. Inputs

Each scene prompt should include:

- genre
- situation
- character desire
- obstacle
- emotional target
- target length
- language

The prompt must not reveal the arm label.

## 5. Arm configuration

### Arm A

Pure LLM baseline.

Allowed:

- prompt only
- no formula hints
- no V1700 story state
- no corpus reference

### Arm B

V1700 structured pipeline.

Allowed:

- declared formula guidance
- declared critic guidance
- declared story state fields
- declared corpus metadata if source policy allows

Not allowed:

- hidden extra context
- longer token budget
- post-generation manual improvement not also applied to Arm A
- using copyrighted full text without permission

## 6. Length control

Both arms must use the same target length.

Recommended:

```text
350 +/- 30 Korean characters for very small scene unit
or
800 +/- 80 Korean characters for short scene unit
```

Length deviations must be recorded.

## 7. Blind packet construction

For each scene:

```text
scene_id
output_1
output_2
randomized_order
hidden_arm_labels
length_count
provider_metadata_hidden_from_evaluator
```

Evaluators receive only output text and evaluation form.

## 8. Evaluation form

Each evaluator selects:

- preferred output
- confidence: low / medium / high
- story coherence score
- tension score
- character believability score
- dialogue/subtext score
- emotional movement score
- originality score
- brief reason

## 9. Aggregation

Minimum metrics:

- Arm B preference rate
- per-dimension average score
- confidence-weighted preference
- length deviation analysis
- disagreement notes

Optional:

- simple binomial test if sample size permits
- effect size estimate

## 10. Pass / fail interpretation

MVE pass does not prove final superiority.

MVE pass only means:

```text
Proceed to larger preregistered experiment is reasonable.
```

MVE fail means:

```text
Do not open execution-engine expansion. Redesign prompt, critic, corpus, or formula guidance first.
```

## 11. Required records

```text
ValueProofFixtureRecord
ScenePromptRecord
ArmConfigRecord
BlindPacketRecord
EvaluatorResponseRecord
AggregationReport
LengthControlReport
FailureDecisionRecord
```

## 12. Evidence paths

```text
experiments/value_proof/mve_fixture/
experiments/value_proof/mve_fixture/prompts/
experiments/value_proof/mve_fixture/outputs/
experiments/value_proof/mve_fixture/blind_packets/
experiments/value_proof/mve_fixture/results/
experiments/value_proof/mve_fixture/aggregate_report.md
```

## 13. Final rule

A value proof fixture must remain controlled, blind, and comparable.

If any arm receives hidden advantages, the result cannot be used for roadmap promotion.
