# Coefficient Audit Record Contract

Status: contract draft
Created: 2026-06-07
Scope: auditable coefficient update planning
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This contract defines how formula or critic coefficients may be changed in a future LearnableCritic layer.

No coefficient may change silently.

## 2. Required records

```text
CoefficientStateRecord
CoefficientDiffRecord
DeterministicSeedRecord
CalibrationRunRecord
AlignmentResultRecord
RollbackRecord
HumanApprovalRecord
```

## 3. CoefficientStateRecord

Fields:

```text
coefficient_state_id
critic_id
formula_id
coefficient_name
coefficient_value
coefficient_version
created_at
source_basis
review_status
```

## 4. CoefficientDiffRecord

Fields:

```text
coefficient_diff_id
before_state_id
after_state_id
changed_fields
old_values
new_values
change_reason
source_signal_refs
calibration_run_ref
```

## 5. DeterministicSeedRecord

Fields:

```text
seed_id
seed_value
run_id
randomization_scope
reproducibility_note
```

## 6. CalibrationRunRecord

Fields:

```text
calibration_run_id
critic_id
input_source_refs
formula_signal_refs
value_proof_refs
learning_rate
iteration_count
loss_or_error_metric
seed_ref
created_at
```

## 7. AlignmentResultRecord

Fields:

```text
alignment_result_id
calibration_run_id
before_alignment
after_alignment
improvement_delta
failure_notes
overfit_warning
human_review_required
```

## 8. RollbackRecord

Fields:

```text
rollback_id
coefficient_diff_id
rollback_target_state_id
rollback_reason
rollback_status
performed_at
```

## 9. HumanApprovalRecord

Fields:

```text
approval_id
coefficient_diff_id
reviewer_role
approval_status
approval_note
approved_at
```

## 10. Rules

- every coefficient change requires before and after state
- every change requires source signal refs
- every calibration run requires deterministic seed
- every promotion requires human review
- every change must be rollbackable
- failed calibration must be recorded honestly

## 11. Blocking failures

- coefficient changed without CoefficientDiffRecord
- missing before or after state
- missing deterministic seed
- missing source signal refs
- missing rollback target
- automatic promotion without human approval
- coefficient update hidden from review

## 12. Final decision

Coefficient updates are allowed only as auditable planning and future runtime operations.

They must never become hidden model memory or hidden preference mutation.
