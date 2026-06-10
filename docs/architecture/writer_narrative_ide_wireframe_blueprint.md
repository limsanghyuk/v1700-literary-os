# Writer Narrative IDE Wireframe Blueprint

Status: blueprint draft
Created: 2026-06-07
Scope: writer collaborative Narrative IDE planning
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint defines a writer-facing IDE layout for future V1700 execution-engine planning.

It is not implementation. It specifies UI/UX authority boundaries and core panels.

## 2. Core principle

The writer remains final authority.

V1700 provides:

- memory
- structure
- formula signals
- corpus references
- critic notes
- rewrite candidates
- value proof hooks
- LearnableCritic explanations

V1700 does not silently mutate canonical manuscript state.

## 3. Three-zone layout

### 3.1 Left zone — Story memory and authority

Panels:

- Work registry
- Story bible
- Character records
- Relationship graph
- World rules
- Formula ledger
- Corpus references
- Source rights warnings
- Authority warnings
- Version history

### 3.2 Center zone — Writing surface

Panels:

- Scene editor
- Chapter editor
- Screenplay view
- Outline view
- Revision diff
- Candidate insertion preview
- Comment overlay
- Approval decision panel

### 3.3 Right zone — Critic and assistant layer

Panels:

- NarrativeStateTensor advisory signal
- Emotional momentum signal
- Tension curve signal
- Character continuity signal
- Dialogue subtext note
- Cliche and trope warning
- Rewrite candidate comparison
- LearnableCritic explanation
- Value Proof experiment note

## 4. Authority workflow

```text
writer edits or requests candidate
V1700 produces advisory signals and candidates
writer compares outputs
writer approves / rejects / revises
approval is logged
only approved output can become canonical
```

## 5. Required UI records

Future contracts:

```text
WriterSessionRecord
EditorCommentRecord
CriticSuggestionRecord
RewriteCandidateRecord
ApprovalDecisionRecord
SceneDiffRecord
AuthorityWarningRecord
CorpusReferenceRecord
LearnableCriticExplanationRecord
```

## 6. Warning display rules

Warnings must be visible for:

- source rights uncertainty
- unresolved formula conflict
- corpus provenance problem
- canonical mutation request
- LLM boundary violation
- critic disagreement
- unapproved coefficient change

## 7. MVP boundary

The first IDE prototype should include only:

- one work
- one scene
- one character record
- one formula signal
- one corpus reference
- one rewrite candidate comparison
- one approval log

No automatic canonical mutation.

## 8. Integration with planning documents

- narrative_corpus_schema_v0_1
- formula_to_corpus_mapping_blueprint
- v1700_llm_boundary_ladder_blueprint
- learnable_critic_record_contract
- post_roadmap_value_proof_gate_blueprint

## 9. Blocking failures

- candidate inserted without approval
- rights warning hidden
- formula signal shown as final truth
- LLM output shown as canonical
- hidden session memory update
- missing scene diff

## 10. Final decision

The Writer Narrative IDE is accepted for planning.

Implementation remains blocked until Page18 Entry Criteria are satisfied.
