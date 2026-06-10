# Value Proof Experiment Engine Blueprint

Status: blueprint draft
Created: 2026-06-10
Scope: Value Proof experiment infrastructure planning, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint defines a future experiment engine for V1700 Value Proof.

The engine's purpose is not to prove value by existing. Its purpose is to run controlled, preregistered, blind comparisons between a pure LLM baseline and a V1700 structured pipeline.

## 2. Core hypothesis

```text
V1700 structured literary OS + controlled LLM assistance produces better literary output than a pure LLM baseline under controlled evaluation.
```

## 3. Required inputs

- value proof preregistration template
- value proof minimum fixture spec
- LLM boundary ladder
- narrative corpus source policy
- narrative corpus minimum fixture
- formula signal runtime bridge
- prompt packet definitions

## 4. Engine modules

### 4.1 Preregistration Loader

Responsibilities:

- load preregistered experiment plan
- lock threshold
- lock arms
- lock evaluator policy
- reject missing required fields

### 4.2 Prompt Packet Builder

Responsibilities:

- generate identical base prompt for Arm A and Arm B
- apply allowed V1700 structure only to Arm B
- enforce target length
- record prompt hashes

### 4.3 Arm Config Registry

Responsibilities:

- record provider
- record model
- record temperature
- record max token budget
- record allowed context
- record forbidden context

### 4.4 Output Capture Layer

Responsibilities:

- store generated outputs by hidden arm label
- record length
- record generation metadata
- prevent evaluator-visible arm labels

### 4.5 Blind Packet Generator

Responsibilities:

- randomize output order
- strip provider metadata
- strip arm labels
- produce evaluator packets

### 4.6 Evaluator Response Collector

Responsibilities:

- collect preference
- collect confidence
- collect dimension scores
- collect brief rationale
- preserve evaluator anonymity if needed

### 4.7 Aggregator

Responsibilities:

- compute Arm B preference rate
- compute per-dimension averages
- compute confidence-weighted preference
- compute length deviation report
- compute statistical test if sample permits
- emit limitations

### 4.8 Gate Reporter

Responsibilities:

- compare result with preregistered threshold
- emit PASS / FAIL / INCONCLUSIVE / NOT_RUN
- include evidence path
- prevent overclaiming

## 5. Required records

```text
ValueProofExperimentRecord
PreregistrationRecord
PromptPacketRecord
ArmConfigRecord
OutputCaptureRecord
BlindPacketRecord
EvaluatorResponseRecord
AggregationResultRecord
LengthControlReport
GateDecisionRecord
```

## 6. Allowed first implementation scope

The first implementation may be scaffold-only:

- load static fixture
- create prompt packets
- create blind packets from stored sample outputs
- collect manual evaluator responses
- aggregate manually entered results

Forbidden at first entry:

- autonomous provider orchestration
- hidden prompt mutation
- live corpus retrieval without source policy
- automatic roadmap promotion

## 7. Gate states

```text
NOT_RUN
DESIGN_READY
FIXTURE_READY
MVE_RUNNING
MVE_COMPLETE
FULL_EXPERIMENT_RUNNING
FULL_EXPERIMENT_COMPLETE
PASS
FAIL
INCONCLUSIVE
```

## 8. Blocking failures

- experiment run without preregistration
- threshold changed after outputs are seen
- evaluator sees arm labels
- Arm B receives unregistered hidden advantage
- length control not reported
- source policy omitted
- result reported as proof when sample is insufficient

## 9. Final decision

The Value Proof experiment engine is suitable as Page18 Option A only after Page18 entry state is updated.

Before that, this document remains planning-only.
