# Learnable Critic Bridge Blueprint

Status: blueprint draft
Created: 2026-06-04
Scope: Page18+ planning, no implementation

## 1. Purpose

This blueprint defines how V1700 may evolve from fixed formula advisory signals toward a learnable but auditable critic layer.

The Learnable Critic is not a final writer, not canonical story authority, and not hidden memory.

## 2. Core principle

Learning is allowed only if it remains:

- explicit
- auditable
- reversible
- source-linked
- bounded
- advisory until promoted by future authority

## 3. Candidate inputs

- Narrative Corpus Database metadata
- Value Proof evaluation results
- writer-approved revision records
- critic disagreement records
- reader response metadata
- formula score calibration records

## 4. Required records

- LearnableCriticConfig
- CriticInputSourceRecord
- CoefficientStateRecord
- CoefficientDiffRecord
- DeterministicSeedRecord
- TrainingOrCalibrationRunRecord
- AlignmentResultRecord
- RollbackRecord
- HumanApprovalRecord
- AdvisoryOutputRecord

## 5. Update algorithm outline

```text
collect approved source records
freeze current coefficient state
run bounded calibration step
produce coefficient diff
record deterministic seed and run metadata
compare critic output before and after
record alignment result
require review before promotion
allow rollback
```

## 6. Hard boundaries

- no hidden coefficient update
- no hidden user preference update
- no direct canonical story mutation
- no Node authority override
- no raw provider output into core authority
- no automatic promotion from advisory to hard gate

## 7. Multi-agent supervision model

Potential agents:

- Formula Critic
- Corpus Analyst
- Continuity Critic
- Dialogue Critic
- Emotion Critic
- Reader Signal Critic
- Safety and Rights Reviewer
- Principal Authority Reviewer

Rules:

- each agent must have a capability scope
- each output must be traceable
- disagreement must be preserved
- final promotion requires authority review

## 8. Integration with formulas

The Learnable Critic does not remove formulas.

It can:

- calibrate coefficients
- compare formula outputs against human preference records
- identify weak axes
- propose formula variants
- explain why a coefficient changed

It cannot:

- delete formula authority
- silently replace formula ledger
- turn advisory scores into canonical decisions

## 9. Integration with Value Proof Gate

Value Proof results should become calibration evidence only after:

- experiment plan is preregistered
- evaluator records are complete
- arm labels are preserved but hidden during evaluation
- result threshold is computed
- failure is recorded honestly

## 10. Acceptance criteria before implementation

- input source policy approved
- coefficient schema defined
- rollback policy approved
- human approval boundary approved
- multi-agent capability scopes defined
- evidence path defined
- no Page18 implementation opened yet

## 11. Recommended next step

Create a LearnableCriticRecord schema draft and coefficient audit fixture.
