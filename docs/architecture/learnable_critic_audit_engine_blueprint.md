# Learnable Critic Audit Engine Blueprint

Status: blueprint draft
Created: 2026-06-10
Scope: LearnableCritic audit engine planning, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint defines a future audit engine for LearnableCritic coefficient changes.

It does not implement learning. It defines how future learning or calibration must be recorded, reviewed, and rolled back.

## 2. Core principle

No hidden learning.

Every coefficient change must be:

- source-linked
- diff-recorded
- seed-recorded
- alignment-tested
- rollbackable
- human-reviewed before promotion

## 3. Required inputs

- LearnableCritic record contract
- coefficient audit record contract
- LearnableCritic audit fixture spec
- formula signal runtime bridge
- narrative corpus source policy
- Value Proof records if used as alignment basis

## 4. Audit engine modules

### 4.1 Coefficient State Loader

Loads current CoefficientStateRecord.

### 4.2 Input Source Validator

Validates CriticInputSourceRecord source class and rights status.

### 4.3 Calibration Run Recorder

Records learning rate, iteration count, loss or error metric, and deterministic seed.

### 4.4 Diff Builder

Creates CoefficientDiffRecord with before and after states.

### 4.5 Alignment Reporter

Compares before and after advisory alignment against a declared target signal.

### 4.6 Rollback Builder

Creates RollbackRecord pointing to a valid prior coefficient state.

### 4.7 Human Approval Gate

Requires HumanApprovalRecord before any coefficient state is promoted.

## 5. Required records

```text
CoefficientStateRecord
CriticInputSourceRecord
CalibrationRunRecord
DeterministicSeedRecord
CoefficientDiffRecord
AlignmentResultRecord
RollbackRecord
HumanApprovalRecord
```

## 6. Allowed first implementation scope

First implementation may only validate a static fixture.

Allowed:

- load fixture records
- validate required fields
- validate before/after state linkage
- validate seed presence
- validate rollback target
- emit audit report

Forbidden:

- actual coefficient optimization
- hidden learning loop
- automatic coefficient promotion
- canonical story mutation

## 7. Audit report states

```text
NOT_RUN
FIXTURE_VALID
FIXTURE_INVALID
DIFF_VALID
DIFF_INVALID
ROLLBACK_READY
APPROVAL_REQUIRED
APPROVED_FOR_PROMOTION
REJECTED
```

## 8. Blocking failures

- coefficient changed without diff
- missing before state
- missing after state
- missing source signal
- missing deterministic seed
- missing rollback record
- missing human approval for promotion
- restricted source used without approval
- critic output mutates canonical state

## 9. Page18 suitability

This is suitable as Page18 Option D only if:

- Page18 entry state is ready
- source policy is approved
- LearnableCritic fixture is reviewed
- canonical mutation remains forbidden

## 10. Final decision

LearnableCritic audit engine must be audit-first, not learning-first.

It may validate future learning infrastructure only after traceability is proven.
