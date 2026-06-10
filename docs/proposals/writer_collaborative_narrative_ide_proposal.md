# Writer Collaborative Narrative IDE Proposal

Status: proposal draft
Created: 2026-06-04
Scope: Page18+ planning, no implementation

## 1. Purpose

This proposal defines a future writer-facing collaborative Narrative IDE for V1700.

The IDE is not an autonomous writing replacement. It is a workspace where the writer remains the final authority while V1700 provides structured memory, critic signals, rewrite candidates, evidence, and production bridges.

## 2. Core design principle

Writer authority is primary.

AI, formulas, critics, and agents are advisory unless a future explicit approval contract promotes a specific output.

## 3. Proposed 3-zone UI

### Left zone — Story memory and control

Purpose:

- work registry
- story bible
- character records
- relationship graph
- world rules
- formula ledger
- corpus references
- version history
- authority warnings

### Center zone — Writing surface

Purpose:

- scene editor
- chapter editor
- screenplay view
- outline view
- revision diff
- writer-approved candidate insertion
- comment and review overlay

### Right zone — Critic and assistant panel

Purpose:

- EAT8D / NarrativeStateTensor advisory output
- tension and emotional momentum notes
- character consistency notes
- dialogue subtext notes
- trope and cliche warnings
- rewrite candidate comparison
- value proof experiment hooks
- LearnableCritic explanations

## 4. Collaboration model

Roles:

- Writer
- Editor
- Reviewer
- Producer
- Critic agent
- Continuity agent
- Dialogue agent
- Production bridge agent

Rules:

- Writer approves canonical changes.
- Reviewer comments are not canonical state.
- Critic outputs are advisory.
- Agent suggestions must identify source, confidence, and affected scene.
- No hidden memory update.
- No silent preference mutation.

## 5. Required records

- WriterSessionRecord
- EditorCommentRecord
- CriticSuggestionRecord
- RewriteCandidateRecord
- ApprovalDecisionRecord
- SceneDiffRecord
- AuthorityWarningRecord
- CorpusReferenceRecord
- LearnableCriticExplanationRecord

## 6. MVP proposal

MVP should not start as a full app.

MVP should start as a deterministic prototype with:

- one work
- one scene
- one character record
- one critic panel
- one rewrite candidate comparison
- one approval log
- no automatic canonical mutation

## 7. Risks

| Risk | Mitigation |
|---|---|
| AI becomes hidden co-author | approval records required |
| UI hides warnings | warning panel fixed in left zone |
| writer loses control | canonical mutation requires explicit approval |
| too many agents create noise | capability-scoped panels only |
| corpus suggestions become plagiarism risk | provenance and rights status shown |

## 8. Integration points

- Narrative Corpus Database
- Post-Roadmap Value Proof Gate
- Learnable Critic Bridge
- Page15 collaboration records
- Page16 screenplay production bridge
- Page17 plugin and studio policy records

## 9. Acceptance criteria before implementation

- UI authority model approved
- role permissions defined
- canonical mutation policy defined
- warning display policy defined
- corpus provenance display policy defined
- MVP boundary approved
- no Page18 implementation opened yet

## 10. Recommended next step

Create a UI/UX wireframe blueprint and WriterSessionRecord schema draft.
