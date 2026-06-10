# Post-Roadmap Long-Range Priority Roadmap

Status: consolidation draft
Created: 2026-06-04
Scope: V1700 after Page17 / Stage242
Mode: planning only, no Page18 implementation

## 1. Purpose

This roadmap consolidates the planning documents produced after Page17 / Stage242 into an ordered long-range roadmap.

It does not open Page18. It does not create Stage243. It organizes priorities so that the project can later decide whether Page18 should begin.

## 2. Current authority baseline

Current terminal point:

- Page17: PASS_WITH_GITNEXUS_OUTPUT
- Stage242: PASS_WITH_GITNEXUS_OUTPUT
- Page18 implementation: absent
- Stage243+ implementation: absent
- Current mode: post-roadmap authority review and planning

Carry-forward warnings:

- Page10 GitNexus evidence refresh remains pending.
- Page11 GitNexus evidence refresh remains pending.
- Page12 GitNexus evidence refresh remains pending.
- Stage185 remains local-known and not hub official.

## 3. Source planning documents

This roadmap consolidates:

- docs/development/conversation_planning_to_hub_protocol.md
- docs/roadmaps/page18_plus_post_roadmap_evolution_plan.md
- docs/proposals/page18_plus_post_roadmap_evolution_proposal.md
- docs/architecture/narrative_corpus_database_blueprint.md
- docs/proposals/writer_collaborative_narrative_ide_proposal.md
- docs/architecture/post_roadmap_value_proof_gate_blueprint.md
- docs/architecture/learnable_critic_bridge_blueprint.md

## 4. Priority model

Priority tiers:

- P0: non-negotiable authority constraints
- P1: required before any clean release or Page18 entry
- P2: required before value proof execution
- P3: required before collaborative writer tool design
- P4: required before learnable critic implementation
- P5: required before multi-agent supervision
- P6: required before execution engine build
- P7: required before productization
- P8: future roadmap expansion

## 5. P0 — Authority constraints

### P0.1 Keep Page18 closed

Decision:

Page18 must not open until Page18 Entry Criteria are written and accepted.

Reason:

Page17 already routes to post-roadmap authority review. Opening Page18 immediately would violate the current release readiness hold.

### P0.2 Preserve warnings

Decision:

Page10~Page12 warnings and Stage185 warning must remain visible until resolved by evidence or explicit policy.

### P0.3 Document-first operation

Decision:

Planning insights from conversations must be committed as planning documents before any implementation entry.

## 6. P1 — Authority cleanup and absorption matrix

### P1.1 Authority Closure Decision

Deliverable:

```text
release/current/post_roadmap_authority_closure_decision.md
```

Purpose:

- decide Page10~Page12 refresh policy
- decide Stage185 hub-official policy
- decide clean package policy
- decide warning-preservation policy

Exit criteria:

- each warning is marked refresh / preserve / defer
- no hidden warning remains
- no Page18 implementation appears

### P1.2 V745-to-V1700 Absorption Matrix

Deliverable:

```text
docs/reviews/literary_os_v745_to_v1700_absorption_matrix.md
```

Purpose:

Map literary-os V745 / Phase E concepts into V1700.

Required rows:

- RULE-0 preflight
- 13-step preflight
- Survival Matrix
- G_CONNECTIVITY
- release block conditions
- SP-E.0 integrity recovery
- G_VALUE_PROOF
- LLM-1 critic boundary
- LearnableCritic
- Phase F/G staged relaxation
- cost, safety, and alignment gates

Exit criteria:

- every row has absorb / reject / defer decision
- accepted items have target V1700 artifact type
- rejected items have reason

## 7. P2 — Value proof layer

### P2.1 Value Proof Gate refinement

Existing draft:

```text
docs/architecture/post_roadmap_value_proof_gate_blueprint.md
```

Next refinement:

- add preregistration template
- add evaluator policy
- define minimum corpus fixture
- define LLM provider boundary
- define cost cap
- define evidence path

### P2.2 Minimum experiment fixture

Future deliverable:

```text
docs/fixtures/value_proof_minimum_fixture_spec.md
```

Purpose:

Define a small, controlled experiment before any execution engine expansion.

Expected arms:

- arm A: pure LLM baseline
- arm B: V1700 structured pipeline
- optional arm C: commercial baseline

Decision rule:

- fail closed if value proof does not meet preregistered threshold

## 8. P3 — Narrative corpus database

Existing draft:

```text
docs/architecture/narrative_corpus_database_blueprint.md
```

Next required documents:

```text
docs/policies/narrative_corpus_source_policy.md
docs/architecture/narrative_corpus_schema_v0_1.md
docs/fixtures/narrative_corpus_minimum_fixture_spec.md
```

Purpose:

Build a rights-aware metadata database for Korean dramas, global dramas, Japanese animation, novels, web novels, and screenplays where legally available.

Priority order:

1. rights and source policy
2. schema v0.1
3. hand-curated pilot records
4. value proof fixture connection
5. LearnableCritic calibration connection

Boundary:

No uncontrolled copyrighted full-text ingestion.

## 9. P4 — Writer collaborative Narrative IDE

Existing draft:

```text
docs/proposals/writer_collaborative_narrative_ide_proposal.md
```

Next required documents:

```text
docs/architecture/writer_narrative_ide_wireframe_blueprint.md
docs/contracts/writer_session_record_contract.md
docs/contracts/approval_decision_record_contract.md
```

Purpose:

Design a writer-in-the-loop tool where the writer remains final authority.

Priority UI model:

- left zone: story memory, formula, corpus, warnings
- center zone: writing surface
- right zone: critic, rewrite candidate, tensor, value proof and LearnableCritic panels

Boundary:

No automatic canonical mutation.

## 10. P5 — Learnable Critic bridge

Existing draft:

```text
docs/architecture/learnable_critic_bridge_blueprint.md
```

Next required documents:

```text
docs/contracts/learnable_critic_record_contract.md
docs/contracts/coefficient_audit_record_contract.md
docs/fixtures/learnable_critic_audit_fixture_spec.md
```

Purpose:

Move from fixed formula advisory signals to learnable but auditable critic calibration.

Boundary:

- no hidden coefficient update
- no hidden preference update
- no direct canonical story mutation
- no Node authority override
- no hard-gate promotion without authority review

## 11. P6 — Multi-agent supervision layer

Future documents:

```text
docs/architecture/multi_agent_supervision_blueprint.md
docs/contracts/agent_capability_scope_contract.md
docs/contracts/agent_disagreement_record_contract.md
```

Candidate agents:

- Formula Critic
- Corpus Analyst
- Continuity Critic
- Dialogue Critic
- Emotion Critic
- Reader Signal Critic
- Rights and Safety Reviewer
- Principal Authority Reviewer

Boundary:

Agents are supervised advisory roles, not autonomous authority holders.

## 12. P7 — Execution engine planning

Future documents:

```text
docs/architecture/literary_execution_engine_entry_blueprint.md
docs/roadmaps/page18_entry_criteria.md
```

Purpose:

Define when V1700 may move from authority/planning system toward actual writing execution engine.

Minimum entry criteria:

- authority closure decision exists
- Page10~Page12 warning policy resolved
- Stage185 policy resolved
- V745 absorption matrix complete
- value proof blueprint refined
- corpus source policy approved
- LearnableCritic bridge refined
- writer IDE authority model approved
- no contradiction in release readiness report

## 13. P8 — Productization and release authority

Future documents:

```text
docs/roadmaps/productization_and_release_authority_roadmap.md
release/current/post_roadmap_clean_release_decision.md
```

Purpose:

Only after value proof and authority cleanup should the project consider clean packaging, tag, release note, UI prototype, studio workflow, or product packaging.

## 14. Dependency graph

```text
P0 Authority Constraints
  -> P1 Authority Closure + V745 Absorption
    -> P2 Value Proof Gate
      -> P3 Narrative Corpus Database
      -> P5 Learnable Critic Bridge
        -> P6 Multi-Agent Supervision
    -> P4 Writer Collaborative IDE
      -> P7 Execution Engine Entry
        -> P8 Productization and Release Authority
```

## 15. Immediate next recommended action

The next document should be:

```text
docs/reviews/literary_os_v745_to_v1700_absorption_matrix.md
```

Reason:

It is the central bridge between the external executable literary-os V745 model and the V1700 authority system. Without this matrix, later value proof, LearnableCritic, corpus, and execution engine planning may import external concepts without V1700-compatible contracts.

## 16. Final roadmap decision

Approved roadmap direction:

```text
Do not open Page18 yet.
First complete authority cleanup, V745 absorption, value proof design, corpus strategy, writer IDE strategy, LearnableCritic strategy, and multi-agent supervision planning.
```

Implementation remains blocked until entry criteria are explicitly satisfied.
