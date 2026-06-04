# Post-Roadmap Value Proof Gate Blueprint

Status: blueprint draft
Created: 2026-06-04
Scope: Page18+ planning, no implementation

## 1. Purpose

This blueprint defines the gate that should prove whether V1700 structure plus controlled LLM assistance produces better literary output than a pure LLM baseline.

This is not a demo gate. It is a preregistered value proof gate.

## 2. Core hypothesis

```text
V1700 structured literary OS + controlled LLM assistance > pure LLM baseline
```

The comparison must be evaluated by blinded human readers or writers under controlled output conditions.

## 3. Experiment arms

### Arm A — Pure LLM baseline

- same prompt
- same target length
- same token budget
- no V1700 structure

### Arm B — V1700 structured pipeline

- same prompt
- same target length
- same token budget
- V1700 structure, critic, memory, or formula guidance allowed within declared boundary

### Optional Arm C — Commercial tool baseline

- only if rights and tool terms allow
- must be disclosed in preregistration

## 4. Required controls

- same input prompt
- same output length target
- same token budget
- same language
- randomized order
- blinded evaluation
- no evaluator sees arm labels
- no post-hoc threshold change
- all exclusions preregistered

## 5. Preregistered threshold

Initial proposal:

```text
Arm B preference >= 60 percent
p < 0.05 if sample size permits
effect size reported
```

If sample size is too small for p-value reliability, report descriptive preference, confidence interval, and effect size without overclaiming.

## 6. Evaluation dimensions

Minimum dimensions:

- story coherence
- scene tension
- character believability
- dialogue subtext
- emotional progression
- originality and cliche avoidance
- reader engagement
- genre fit

## 7. Required records

- ValueProofExperimentPlan
- PreregisteredThresholdRecord
- PromptRecord
- ArmConfigurationRecord
- OutputArtifactRecord
- BlindEvaluationPacket
- EvaluatorProfileRecord
- PreferenceResultRecord
- EffectSizeReport
- FailureDecisionRecord

## 8. Fail-closed decision rule

If Arm B fails the threshold, the project must not open execution-engine expansion based on the failed experiment.

Failure routes to:

- critic redesign
- corpus improvement
- formula calibration
- prompt/control redesign
- smaller repeat experiment

Failure must not route to uncontrolled feature expansion.

## 9. Integration with V1700

This gate should connect to:

- Narrative Corpus Database
- Learnable Critic Bridge
- Formula Ledger v2
- NarrativeStateTensor advisory layer
- Writer Collaborative Narrative IDE

## 10. Acceptance criteria before implementation

- experiment schema approved
- evaluator policy approved
- minimum corpus policy approved
- LLM boundary policy approved
- cost policy approved
- evidence path defined
- no Page18 implementation opened yet

## 11. Recommended next step

Create a preregistration template and minimal experiment fixture.
