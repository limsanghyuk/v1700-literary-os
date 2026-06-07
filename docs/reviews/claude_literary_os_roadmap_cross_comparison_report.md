# Claude literary-os Roadmap Cross-Comparison Report

Status: review draft
Created: 2026-06-07
Scope: Compare limsanghyuk/literary-os V745+ roadmap with V1700 post-roadmap planning
Target repository: limsanghyuk/v1700-literary-os
External reference repository: limsanghyuk/literary-os

## 1. Purpose

This report reviews the roadmap of the Claude-developed `limsanghyuk/literary-os` model and compares it with the current V1700 post-roadmap planning conversation.

The goal is to identify gaps in V1700 planning before Page18 or Stage243+ is opened.

This report is a planning and review document only. It does not open Page18 and does not create Stage243.

## 2. Source basis

External source files reviewed from `limsanghyuk/literary-os`:

- RELEASE_INFO.txt
- docs/sessions/2026-06-02_home_continuation_playbook.md
- docs/sessions/2026-06-02_phase_efg_planning_handoff_v1.md
- docs/sessions/2026-06-02_phaseE_validation_first_handoff_v1.md

V1700 source files reviewed:

- docs/roadmaps/post_roadmap_long_range_priority_roadmap.md
- docs/proposals/page18_plus_post_roadmap_evolution_proposal.md
- docs/architecture/post_roadmap_value_proof_gate_blueprint.md
- docs/architecture/learnable_critic_bridge_blueprint.md
- docs/architecture/narrative_corpus_database_blueprint.md
- docs/proposals/writer_collaborative_narrative_ide_proposal.md

## 3. Claude literary-os current baseline

`literary-os` is currently recorded as:

```text
Literary OS V745
Version: 13.0.0
Phase D complete
ADR-208 latest
SP-D.4 complete
Gates: 97
Tests: 10788+ PASS
Preflight: 13-step ALL PASS
```

The model is therefore a runtime-heavy execution system with release gates, tests, preflight, plugin sandboxing, federated learning, disaster recovery, and Phase E preparation.

## 4. Claude roadmap after V745

The Claude roadmap after V745 is not immediate feature expansion. It is a validation-first Phase E entry.

### 4.1 Phase E entrance

The core statement is:

```text
Phase E = SP-E.0 integrity recovery -> low-cost pre-experiment -> minimum real validation slice -> go/no-go.
```

The central unresolved hypothesis is:

```text
structured system + LLM > pure LLM baseline
```

This is explicitly marked as not yet proven.

### 4.2 SP-E.0 integrity recovery

The first post-V745 step is SP-E.0, focused on release self-verification.

Claude roadmap tasks:

- add G_INTEGRITY_MANIFEST
- regenerate SHA256SUMS and test_inventory at the end of the release process
- fail release if regenerated metadata does not match
- restore ADR-37 and ADR-38 or mark gaps explicitly
- add ADR continuity gate

### 4.3 Value proof

Claude roadmap elevates the validation gate to G_VALUE_PROOF.

Experiment model:

- arm A: pure LLM
- arm B: structure + LLM
- optional arm C: commercial tool baseline
- same prompt
- same length
- same token budget
- blind randomized evaluation
- MVE: 10~15 scenes, 2~3 writers
- full experiment: 40~60 scenes, 5+ writers
- preregistered threshold: B preference >= 60 percent, p < 0.05 if sample size permits

### 4.4 LearnableCritic

Claude roadmap redefines formula as:

```text
learnable analytical prior / critic
```

It is not a replacement for AI, and not a final author. It is a controllable guardrail whose coefficients can be calibrated by recorded learning loops.

### 4.5 LLM relaxation roadmap

Claude roadmap proposes a staged relaxation:

```text
LLM-0: through V745, no external LLM in core generation/evaluation authority
LLM-1: Phase E, critic/* assistance only
LLM-1.5: Phase F, full 5-axis critic + draft generation
LLM-2.0: Phase G, generation primary
LLM-2.5: autonomous generation-evaluation loop boundary
```

The transition is gate-based and rollbackable.

### 4.6 Phase E/F/G ranges

Claude roadmap frames future phases as:

```text
Phase E: V746~V795, LLM-1
Phase F: V796~V875, LLM-1.5
Phase G: V876~V955, LLM-2.0~2.5 + business track
```

Phase E includes corpus 50 works, LLM-1 critic, UI, RLAIF, and exit gate.
Phase F includes corpus 200 works, full AI critic axes, draft generation boundary, multilingual track.
Phase G includes generation-primary mode, autonomous evaluation loop, B2B SaaS, marketplace, billing and tenant gates.

## 5. Current V1700 roadmap baseline

V1700 is currently in post-roadmap planning after Page17 / Stage242.

Current V1700 baseline:

```text
Page17: PASS_WITH_GITNEXUS_OUTPUT
Stage242: PASS_WITH_GITNEXUS_OUTPUT
Page18 implementation: absent
Stage243+ implementation: absent
Mode: post-roadmap authority review and planning
```

Current V1700 long-range priority tiers:

```text
P0 Authority constraints
P1 Authority cleanup and V745 absorption matrix
P2 Value proof layer
P3 Narrative corpus database
P4 Writer collaborative Narrative IDE
P5 Learnable Critic bridge
P6 Multi-agent supervision layer
P7 Execution engine planning
P8 Productization and release authority
```

V1700 already recognizes the need to keep Page18 closed until entry criteria are written and accepted.

## 6. Cross-comparison

| Area | Claude literary-os roadmap | V1700 current planning | Gap |
|---|---|---|---|
| Runtime maturity | Strong execution system with tests, gates, preflight | Strong authority system, weaker runtime engine | V1700 needs runtime bridge |
| Release integrity | SP-E.0 explicitly repairs stale manifest/checksum/test inventory | Authority cleanup exists, but not yet self-verification pipeline | Add V1700 integrity self-check plan |
| Value proof | G_VALUE_PROOF with MVE/full experiment | Value Proof Gate blueprint exists | Needs preregistration template and fixture |
| Corpus | Phase E corpus 50, Phase F corpus 200 | Corpus DB blueprint exists | Needs source policy, schema, pilot records |
| UI/UX | Phase E 3-zone UI | Writer IDE proposal exists | Needs wireframe blueprint and session contracts |
| LearnableCritic | Formula as learnable analytical critic | Learnable Critic blueprint exists | Needs record contracts and audit fixture |
| LLM boundary | LLM-0 -> LLM-1 -> LLM-1.5 -> LLM-2.0/2.5 | LLM assistance planned but not staged in detail | Need V1700 LLM boundary ladder |
| Multi-agent | Later autonomous/evaluation loop with safety gates | Multi-agent supervision planned | Needs capability scope/disagreement contracts |
| Business/Product | Phase G SaaS, marketplace, billing | Productization deferred to P8 | Acceptable, but needs later business gate mapping |
| Authority governance | Less page/stage authority than V1700 | Very strong GitNexus/page/stage authority | V1700 advantage |

## 7. Key deficiencies in V1700 planning

### 7.1 Missing concrete V745 absorption matrix

V1700 already identifies this as the next document, but it has not yet been written.

Impact:

Without this matrix, V1700 risks importing Claude runtime concepts without V1700-compatible contracts.

Required document:

```text
docs/reviews/literary_os_v745_to_v1700_absorption_matrix.md
```

### 7.2 Missing integrity self-verification plan

Claude roadmap has SP-E.0 for release self-verification. V1700 has authority cleanup but no explicit equivalent of:

- regenerate checksum at release end
- regenerate inventory at release end
- fail release if metadata is stale
- ADR continuity gate

Required document:

```text
docs/architecture/v1700_post_roadmap_integrity_self_verification_blueprint.md
```

### 7.3 Missing preregistration template

V1700 has a Value Proof Gate blueprint but not the preregistered experiment packet.

Required documents:

```text
docs/fixtures/value_proof_preregistration_template.md
docs/fixtures/value_proof_minimum_fixture_spec.md
```

### 7.4 Missing LLM boundary ladder

Claude roadmap has LLM-0 to LLM-2.5 stages. V1700 needs its own version that respects Node authority, canonical story authority, provider boundaries, and advisory-only evaluation.

Required document:

```text
docs/architecture/v1700_llm_boundary_ladder_blueprint.md
```

### 7.5 Missing corpus source policy and schema

V1700 has a corpus database blueprint, but not the source policy and schema.

Required documents:

```text
docs/policies/narrative_corpus_source_policy.md
docs/architecture/narrative_corpus_schema_v0_1.md
```

### 7.6 Missing IDE wireframe and session contracts

V1700 has a writer collaborative IDE proposal, but not wireframes or user/session authority contracts.

Required documents:

```text
docs/architecture/writer_narrative_ide_wireframe_blueprint.md
docs/contracts/writer_session_record_contract.md
docs/contracts/approval_decision_record_contract.md
```

### 7.7 Missing LearnableCritic contracts

V1700 has a Learnable Critic blueprint, but not machine-readable contracts.

Required documents:

```text
docs/contracts/learnable_critic_record_contract.md
docs/contracts/coefficient_audit_record_contract.md
docs/fixtures/learnable_critic_audit_fixture_spec.md
```

### 7.8 Missing multi-agent supervision contracts

V1700 has multi-agent supervision in the roadmap but no contract layer.

Required documents:

```text
docs/architecture/multi_agent_supervision_blueprint.md
docs/contracts/agent_capability_scope_contract.md
docs/contracts/agent_disagreement_record_contract.md
```

## 8. Recommended revised priority order

The previous V1700 P0~P8 roadmap remains valid, but this cross-comparison adds sharper ordering.

### P0 — Keep implementation closed

- Keep Page18 closed.
- Keep Stage243+ absent.
- Preserve Page10~Page12 and Stage185 warnings.

### P1 — Absorption and integrity

1. Create V745-to-V1700 Absorption Matrix.
2. Create V1700 integrity self-verification blueprint.
3. Decide Page10~Page12 refresh policy.
4. Decide Stage185 policy.

### P2 — Value proof readiness

1. Refine Value Proof Gate.
2. Create preregistration template.
3. Create minimum experiment fixture.
4. Define evaluator policy.

### P3 — Corpus and rights

1. Create corpus source policy.
2. Create schema v0.1.
3. Create hand-curated pilot fixture.

### P4 — LLM and LearnableCritic boundary

1. Create V1700 LLM boundary ladder.
2. Create LearnableCritic record contracts.
3. Create coefficient audit fixture.

### P5 — Writer IDE and multi-agent supervision

1. Create writer IDE wireframe blueprint.
2. Create writer session and approval contracts.
3. Create multi-agent supervision blueprint.
4. Create agent capability and disagreement contracts.

### P6 — Page18 entry decision

Only after P1~P5 documents exist should Page18 Entry Criteria be finalized.

## 9. Final assessment

Claude literary-os is ahead in runtime execution maturity.

V1700 is ahead in authority, lineage, page/stage governance, and GitNexus evidence discipline.

The optimal path is not to merge one into the other directly. The correct path is:

```text
V745 runtime lessons
→ V1700 absorption matrix
→ integrity self-verification
→ value proof gate
→ corpus and rights schema
→ learnable critic contracts
→ writer IDE and multi-agent supervision
→ Page18 entry criteria
```

## 10. Immediate next action

Create the following document next:

```text
docs/reviews/literary_os_v745_to_v1700_absorption_matrix.md
```

This is the highest-leverage next document because it converts comparison into actionable absorb / reject / defer decisions.

## 11. Final decision

Do not open Page18 yet.

Do not create Stage243 yet.

First complete cross-model absorption, self-verification, value proof, corpus, LLM boundary, LearnableCritic, writer IDE, and multi-agent contract planning.
