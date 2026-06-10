# Writer IDE MVP Interaction Flow Blueprint

Status: blueprint draft
Created: 2026-06-10
Scope: Writer Narrative IDE MVP flow planning, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint defines the minimum interaction flow for a non-canonical Writer Narrative IDE MVP.

The goal is to test writer review, advisory signals, and approval records without granting automatic canonical mutation authority.

## 2. MVP boundary

The MVP should include only:

- one work
- one scene
- one or two characters
- one FormulaSignalRecord
- one corpus reference
- one critic suggestion
- one rewrite candidate
- one approval decision

No automatic canonical write is allowed.

## 3. Flow overview

```text
open writer session
load work metadata
load scene metadata
show formula signal
show corpus reference
show critic suggestion
show rewrite candidate
writer reviews candidate
writer approves / rejects / requests revision
create ApprovalDecisionRecord
if approved, create SceneDiffRecord candidate
canonical mutation remains separate and gated
```

## 4. Screen zones

### 4.1 Left panel

- work metadata
- character summary
- corpus reference
- source and rights status
- formula lineage label

### 4.2 Center panel

- current scene text or scene metadata placeholder
- candidate preview
- diff preview
- writer notes

### 4.3 Right panel

- FormulaSignalRecord explanation
- critic suggestion
- agent warnings
- LLM boundary label
- approval decision form

## 5. Required records

```text
WriterSessionRecord
CorpusReferenceRecord
FormulaSignalRecord
CriticSuggestionRecord
RewriteCandidateRecord
ApprovalDecisionRecord
SceneDiffRecord
AuthorityWarningRecord
```

## 6. Canonical mutation boundary

Approval does not necessarily mutate canonical state.

MVP should separate:

```text
APPROVE_AS_REFERENCE_ONLY
APPROVE_CANONICAL_INSERTION
APPROVE_CANONICAL_REVISION
```

Canonical insertion or revision requires a SceneDiffRecord and explicit approval.

## 7. LLM boundary

MVP may use only preloaded sample candidates or LLM-1 advisory behavior if later approved.

No autonomous drafting loop.

## 8. Failure states

- candidate inserted without approval
- rights warning hidden
- formula signal shown as final truth
- LLM output unlabeled
- session state updated without audit
- rejected candidate reused without superseding approval

## 9. Test fixture

Future fixture path:

```text
fixtures/writer_ide_mvp/minimal_session.json
fixtures/writer_ide_mvp/minimal_candidate.json
fixtures/writer_ide_mvp/minimal_approval.json
```

## 10. Final decision

Writer IDE MVP should remain a review and approval interface first.

It should not become an automatic writing engine in its first version.
