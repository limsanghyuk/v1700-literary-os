# Approval Decision Record Contract

Status: contract draft
Created: 2026-06-09
Scope: writer approval and canonical mutation boundary
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This contract defines how a candidate, suggestion, formula signal, critic output, or LLM output may be approved or rejected.

Canonical story mutation requires explicit approval.

## 2. Required record

```text
ApprovalDecisionRecord
```

## 3. Required fields

```text
approval_decision_id
writer_session_id
work_id
subject_record_id
subject_record_type
decision_type
decision_status
decider_role
decider_id_optional
reason
approved_change_ref
scene_diff_ref
created_at
```

## 4. Subject record types

```text
RewriteCandidateRecord
CriticSuggestionRecord
LLMOutputCandidateRecord
FormulaSignalRecord
LearnableCriticAdvisoryOutputRecord
AgentDisagreementRecord
SceneDiffRecord
CorpusReferenceRecord
```

## 5. Decision types

```text
APPROVE_CANONICAL_INSERTION
APPROVE_CANONICAL_REVISION
APPROVE_AS_REFERENCE_ONLY
REJECT
REQUEST_REVISION
DEFER
LOCK_FOR_REVIEW
```

## 6. Decision statuses

```text
DRAFT
APPROVED
REJECTED
DEFERRED
REVOKED
SUPERSEDED
```

## 7. Decider roles

```text
WRITER
EDITOR
PRINCIPAL_AUTHORITY_REVIEWER
RIGHTS_REVIEWER
RELEASE_AUTHORITY
```

## 8. Canonical mutation rule

Canonical mutation is allowed only if:

```text
decision_type in [APPROVE_CANONICAL_INSERTION, APPROVE_CANONICAL_REVISION]
decision_status = APPROVED
scene_diff_ref is present
writer_session_id is present
```

## 9. Rejection rule

A rejected candidate must not be inserted later unless a new ApprovalDecisionRecord supersedes the rejection.

## 10. Source and rights rule

If a decision references corpus or external source material, the related source policy record must remain linked.

## 11. Blocking failures

- canonical change without approval
- approval missing subject record
- approval missing decider role
- canonical approval missing SceneDiffRecord
- rejected candidate inserted without superseding decision
- rights warning ignored without reviewer decision

## 12. Final decision

ApprovalDecisionRecord is the required boundary between advisory output and canonical story state.

No future V1700 IDE or execution engine should bypass it.
