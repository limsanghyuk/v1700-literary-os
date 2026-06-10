# Learnable Critic Audit Fixture Spec

Status: fixture spec draft
Created: 2026-06-09
Scope: future LearnableCritic audit planning
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This fixture spec defines the minimum auditable sample for testing a future LearnableCritic coefficient update workflow.

It does not implement learning. It defines the evidence bundle required before implementation.

## 2. Minimum fixture contents

```text
1 FormulaCatalogRecord
1 FormulaSignalRecord
1 CriticInputSourceRecord
1 CoefficientStateRecord before update
1 CalibrationRunRecord
1 DeterministicSeedRecord
1 CoefficientDiffRecord
1 CoefficientStateRecord after update
1 AlignmentResultRecord
1 RollbackRecord
1 HumanApprovalRecord
```

## 3. Required source class

All input records must use allowed source classes from:

```text
docs/policies/narrative_corpus_source_policy.md
```

Unknown or restricted source classes are not allowed in this fixture.

## 4. Minimum test scenario

Scenario:

```text
A scene has weak emotional progression.
FormulaSignalRecord emits low emotional momentum score.
LearnableCritic proposes coefficient adjustment.
Adjustment is recorded with before/after coefficient state.
Alignment is checked.
Rollback target is recorded.
Human reviewer approves or rejects promotion.
```

## 5. Fixture pass criteria

The fixture is valid only if:

- all source records are linked
- before and after coefficient states exist
- coefficient diff is explicit
- deterministic seed exists
- alignment result is recorded
- rollback target exists
- human approval status exists
- advisory output does not mutate canonical state

## 6. Blocking failures

- hidden coefficient update
- missing seed
- missing source signal
- missing rollback record
- missing human approval
- restricted source used without approval
- canonical mutation from critic output

## 7. Output path proposal

Future fixture may live at:

```text
fixtures/learnable_critic_audit/minimal_fixture.json
fixtures/learnable_critic_audit/README.md
```

## 8. Final rule

No LearnableCritic runtime implementation should proceed until this audit fixture is defined and reviewed.
