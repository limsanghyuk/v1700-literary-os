# Conversation Planning to Hub Protocol

Status: planning protocol draft
Created: 2026-06-04
Scope: post-roadmap planning conversations
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This protocol records how planning outcomes from user conversations should be preserved in the hub.

The purpose is not to auto-implement every discussion. The purpose is to prevent loss of architectural decisions, planning assumptions, rejected alternatives, and next-step proposals.

## 2. Operating rule

When a conversation produces a stable planning decision, proposal, design draft, risk analysis, or roadmap direction, create or update a repository document.

Do not open a new implementation page or stage unless the required entry criteria are satisfied.

## 3. Document-first sequence

Use this sequence:

```text
conversation insight
→ planning note / proposal / blueprint draft
→ hub commit
→ later prioritization review
→ roadmap consolidation
→ only then implementation entry decision
```

## 4. What must be pushed

Push the following when they become stable enough:

- planning summaries
- proposal drafts
- architecture blueprints
- decision matrices
- risk registers
- rejected strategy notes
- entry criteria
- value proof design
- data strategy design
- UI/UX collaboration model drafts
- learnable critic and multi-agent control proposals

## 5. What must not be pushed as implementation

Do not push implementation scaffolds when the user is still planning.

Do not create Page18 or Stage243+ while release readiness remains in authority review.

Do not remove Page10~Page12 warnings or Stage185 warning unless evidence is pushed and gate files are updated.

## 6. Current planning baseline

Current baseline:

- Page17: PASS_WITH_GITNEXUS_OUTPUT
- Stage242: PASS_WITH_GITNEXUS_OUTPUT
- Page18 implementation: absent
- Stage243+ implementation: absent
- Current mode: planning and post-roadmap authority review

## 7. Current planning backlog

The following drafts should be prepared before any Page18 implementation:

1. literary_os_v745_to_v1700_absorption_matrix
2. post_roadmap_value_proof_gate_blueprint
3. learnable_critic_bridge_blueprint
4. narrative_corpus_database_blueprint
5. writer_collaborative_narrative_ide_proposal
6. page18_entry_criteria
7. long_range_roadmap_consolidation

## 8. Review cadence

After several planning documents accumulate, perform a priority review and consolidate them into a long-range roadmap.

The roadmap should distinguish:

- authority cleanup
- evidence refresh
- value proof
- corpus and database
- UI/UX and writer collaboration
- learnable critic
- multi-agent supervision
- execution engine implementation
- release authority

## 9. Final rule

Planning documents may be created immediately.

Implementation must wait for entry criteria.
