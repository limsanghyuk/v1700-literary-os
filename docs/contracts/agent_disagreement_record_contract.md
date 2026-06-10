# Agent Disagreement Record Contract

Status: contract draft
Created: 2026-06-09
Scope: future V1700 supervised multi-agent planning
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This contract defines how disagreements between advisory agents must be recorded and preserved.

Disagreement must not be hidden, overwritten, or silently resolved by an agent.

## 2. Required record

```text
AgentDisagreementRecord
```

## 3. Required fields

```text
disagreement_id
subject_record_id
subject_record_type
agent_refs
claim_a
claim_b
claim_c_optional
supporting_evidence_refs
source_policy_refs
severity
conflict_type
recommended_resolution
final_reviewer_role
final_reviewer_decision
review_status
created_at
updated_at
```

## 4. Conflict types

```text
FORMULA_VS_CORPUS
CRITIC_VS_WRITER_INTENT
CONTINUITY_VS_DIALOGUE
EMOTION_VS_PLOT
RIGHTS_VS_CREATIVE_USE
LLM_OUTPUT_VS_AUTHORITY_BOUNDARY
LEARNABLE_CRITIC_VS_FIXED_FORMULA
VALUE_PROOF_INTERPRETATION_CONFLICT
```

## 5. Severity levels

```text
LOW
MEDIUM
HIGH
BLOCKING
```

## 6. Resolution rule

Agents may recommend a resolution, but they cannot finalize it.

Final resolution requires one of:

- writer approval
- designated human reviewer approval
- Principal Authority Reviewer decision
- future release authority decision

## 7. Required evidence

Every disagreement should reference at least one of:

- formula signal
- corpus record
- source policy record
- writer session record
- value proof record
- LearnableCritic record
- LLM boundary record
- approval decision record

## 8. Blocking failures

- disagreement not recorded
- subject record missing
- agent refs missing
- source-related disagreement missing source policy refs
- final reviewer missing for HIGH or BLOCKING severity
- agent silently resolves conflict without reviewer decision

## 9. Final decision

Disagreement preservation is mandatory for future multi-agent supervision.

No advisory agent may erase or hide conflict records.
