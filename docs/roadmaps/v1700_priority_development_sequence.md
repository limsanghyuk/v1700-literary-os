# V1700 Priority Development Sequence

Status: ACTIVE_SEQUENCE
Created: 2026-06-12
Scope: prioritized implementation order derived from accumulated V1700 proposals, blueprints, reviews, fixtures, and result artifacts.

## 1. Purpose

Convert accumulated planning documents into an executable development order.

This sequence preserves current boundaries:

```text
Page18 implementation: NOT_OPENED
Stage243+: NOT_CREATED
Provider generation: DISABLED
Memory write: DISABLED
Canon mutation: DISABLED
Weight update: DISABLED
```

## 2. P0 — Immediate development

### P0.1 Frontend Component Contracts

Purpose: define UI component payload contracts for the already-reviewed frontend renderer blueprint.

Artifacts:

```text
docs/contracts/frontend_component_contracts.md
fixtures/option_b_validation/frontend_component_contracts_packet.json
```

Depends on:

```text
writer_ide_advisory_panel_render_packet.json
writer_ide_render_packet_review_result.json
frontend_renderer_blueprint_packet.json
```

### P0.2 Canonical Record Store contracts

Purpose: define canonical records before database implementation.

Artifacts:

```text
docs/contracts/canonical_record_store_contract.md
fixtures/canonical_record_store/minimum_records.json
```

Depends on:

```text
canonical_record_store_rag_blueprint.md
v1700_deficiency_registry.md
```

### P0.3 Safe RAG contract

Purpose: separate SafeSurfaceRAG from ProtectedAuthorRAG before retrieval implementation.

Artifacts:

```text
docs/contracts/rag_retrieval_packet_contract.md
fixtures/rag/minimum_retrieval_cases.json
```

Depends on:

```text
canonical_record_store_rag_blueprint.md
```

### P0.4 Formula Measurement Lab minimum plan

Purpose: prepare measurement without active coefficient update.

Artifacts:

```text
fixtures/formula_measurement/formula_measurement_plan.json
fixtures/formula_measurement/coefficient_candidate_registry.json
```

Depends on:

```text
formula_measurement_lab_blueprint.md
formula_signal_mapping_result.json
```

## 3. P1 — Short-term development

### P1.1 Agent Action Record contract

Purpose: make AI agent activity visible, auditable, and permission-bound.

Artifacts:

```text
docs/contracts/agent_action_record_contract.md
fixtures/agent_board/minimum_agent_actions.json
```

### P1.2 Frontend renderer static prototype plan

Purpose: define static frontend implementation plan after component contracts.

Artifacts:

```text
docs/architecture/writer_ide_static_frontend_prototype_plan.md
```

### P1.3 Claude MultiWork preflight fixtures

Purpose: absorb Claude/literary-os MultiWork concepts as V1700 contracts only.

Artifacts:

```text
fixtures/multiwork/project_isolation_cases.json
fixtures/multiwork/shared_character_readonly_cases.json
```

### P1.4 GitNexus evidence gap registry

Purpose: isolate early bridge evidence gaps without blocking current lightweight UI scaffold.

Artifacts:

```text
docs/reviews/gitnexus_evidence_gap_registry.md
```

## 4. P2 — Mid-term development

```text
canonical_record_store_validator.py
rag_retrieval_validator.py
agent_board_packet_builder.py
formula_measurement_lab.py
writer_ide_static_frontend_prototype
multiwork_isolation_validator.py
```

P2 implementation must remain local, deterministic, and non-mutating until its validators pass.

## 5. P3 — Long-term development

```text
Formula Ledger v2
Canonical Formula Registry
MultiWork release chain
Graph contradiction advisory / Gate26 advisory
Bounded self-learning shadow evaluation
Human-approved coefficient update pipeline
Production CI/CD and release automation closure
```

## 6. Blocked or deferred

The following remain blocked until separate approval:

```text
Page18 runtime implementation
Stage243+ creation
provider generation
memory write
canon mutation
active coefficient update
auto-repair mutation
live provider RAG
cross-work retrieval without license edge
```

## 7. Promotion rule

A P0/P1 artifact can advance only when:

```text
contract exists
fixture exists
validator or review exists
result artifact exists
boundary invariants remain preserved
human or release governor decision is recorded when required
```

## 8. Current next action

```text
Create Frontend Component Contracts as lightweight contract + packet.
```
