# Writer Session Record Contract

Status: contract draft
Created: 2026-06-09
Scope: future Writer Narrative IDE planning
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This contract defines a writer session record for future V1700 collaborative writing workflows.

The writer remains final authority. Session records preserve what was shown, suggested, approved, rejected, or revised.

## 2. Required record

```text
WriterSessionRecord
```

## 3. Required fields

```text
writer_session_id
work_id
session_scope
active_scene_refs
active_character_refs
active_corpus_refs
active_formula_signal_refs
active_agent_refs
llm_boundary_level
started_at
ended_at
session_status
```

## 4. Session scope values

```text
OUTLINE_REVIEW
SCENE_DRAFTING
SCENE_REVISION
DIALOGUE_REVISION
CHARACTER_ARC_REVIEW
VALUE_PROOF_PREPARATION
CORPUS_ANALYSIS
LEARNABLE_CRITIC_REVIEW
```

## 5. Session status values

```text
DRAFT
ACTIVE
PAUSED
COMPLETED
ABANDONED
LOCKED_FOR_REVIEW
```

## 6. Required linked records

A writer session may link to:

- RewriteCandidateRecord
- CriticSuggestionRecord
- AgentDisagreementRecord
- ApprovalDecisionRecord
- SceneDiffRecord
- CorpusReferenceRecord
- LearnableCriticExplanationRecord
- LLMOutputCandidateRecord

## 7. Session authority rules

- session activity does not automatically mutate canonical story state
- rewrite candidates remain non-canonical until approved
- critic suggestions remain advisory
- LLM output remains candidate or advisory only
- corpus references must preserve source class and rights status

## 8. Required UI audit trail

Every session should preserve:

```text
shown_to_writer
suggested_by_system
suggested_by_agent
accepted_by_writer
rejected_by_writer
modified_by_writer
pending_review
```

## 9. Blocking failures

- session has no work_id
- active source references lack source policy
- LLM boundary level missing for LLM-assisted session
- canonical state changed without ApprovalDecisionRecord
- rejected candidate inserted later without approval

## 10. Final decision

WriterSessionRecord is required before future Writer Narrative IDE implementation.

It does not implement the IDE and does not grant autonomous write authority.
