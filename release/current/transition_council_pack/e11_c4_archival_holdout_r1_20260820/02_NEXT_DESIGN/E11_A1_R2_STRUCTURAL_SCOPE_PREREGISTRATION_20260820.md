# E11 A1-R2 Structural Scope Preregistration

Date: 2026-08-20  
Status: DESIGN_FROZEN_FOR_NEXT_UNUSED_HOLDOUT  
Claim boundary: internal validation only; no promotion claim

## Reason for R2

A1-R1 retained L3 only when controller reason text contained a narrow combination of `회차`, `axis/carrier`, and `완료/전환/확정`. The archival holdout showed that equivalent events were written as `목표가 완결`, `downstream objective class가 바뀜`, or `단계가 끝남`. R1 therefore reduced L3 recall from 66.67% to 0% and is rejected.

R2 must not inspect free-text wording. It uses explicit structural evidence fields fixed before gold unblinding.

## Required Evidence Fields

Every Sequence decision must record these booleans and a short evidence reference:

```text
local_payoff_only
sequence_transaction_terminal
phase_objective_changed
carrier_question_answered
remaining_sequences_require_new_objective_class
global_thread_irreversible
thread_reappears_in_next_context
final_sequence
final_hook_only
```

No drama title, episode number, Sequence number, or reason-string token may be used as an exception.

## Frozen Classifier

```text
if global_thread_irreversible
   and not thread_reappears_in_next_context:
    L4
elif carrier_question_answered
     and remaining_sequences_require_new_objective_class
     and not final_hook_only:
    L3
elif phase_objective_changed
     or (carrier_question_answered and not remaining_sequences_require_new_objective_class):
    L2
elif sequence_transaction_terminal:
    L1
else:
    L0
```

`final_sequence` alone never forces L1 or L3. A final Sequence that only opens a next-episode question is `final_hook_only=true`; a final Sequence that actually settles the current episode carrier may still be L3.

## Intervention Policy

- C2: existing scope-aware hysteresis.
- C4-R2: C2 plus the structural classifier and terminal exit-state policy.
- At `final_sequence=true`, material replanning is suppressed and only exit-state compilation is allowed.
- L4 closure requires both irreversible evidence and absence from the next-context open-thread set.

## Next Holdout

- Exclude all E11 works: 국희, 궁, 녹두꽃, 대물, 대장금, 뉴하트.
- Exclude all R1 archival-holdout works: 개인의취향, 난폭한로맨스, 도깨비, 라이벌, 로망스, 미안하다사랑한다.
- Use at least six works and at least 60 Sequence observations.
- Seal target EpisodePlan, next-episode context, and gold adjudication until all structural fields and C2/C4-R2 decisions are hashed.

## Primary Hypotheses

- H1: C4-R2 accuracy > C2 and ordinal MAE < C2.
- H2: C4-R2 L3 recall is no more than 0.10 below C2.
- H3: C4-R2 L3 precision >= C2 L3 precision.
- H4: final-sequence material rewrites = 0.
- H5: catastrophic stale-carrier <= C2.

H1 cannot authorize adoption when H2 or H5 fails.

## Required Row Ledger

Each row must include the nine evidence booleans, evidence references, C2 and C4-R2 scope predictions, gold scope, both material flags, hindsight-valid status, false-global thread id or null, stale-carrier status, and final-sequence policy result.

## Invalid Run Conditions

- Any holdout read before decision freeze.
- Any reason-string keyword or work-specific exception in classification.
- Missing row-level gold or intervention adjudication.
- Hash mismatch, row-count mismatch, or target/cutoff leakage.
- Rule modification after gold unblinding.
