# Page18 Limited Scope Options Blueprint

Status: blueprint draft
Created: 2026-06-10
Scope: limited Page18 scope planning, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint decomposes the allowed Page18 scopes defined in `docs/roadmaps/page18_entry_criteria.md` into bounded, low-risk implementation candidates.

It does not open Page18. It only defines what Page18 may be allowed to contain after entry criteria are satisfied.

## 2. Baseline

Current baseline:

```text
Page17: PASS_WITH_GITNEXUS_OUTPUT
Stage242: PASS_WITH_GITNEXUS_OUTPUT
Page18 implementation: absent
Stage243+ implementation: absent
Page18 entry state: DECISIONS_PENDING
```

## 3. Scope selection rule

Page18 must begin with one limited scope only.

Do not combine all scopes into a broad execution engine at first entry.

Allowed first-entry policy:

```text
one primary scope
one optional supporting scope
no autonomous generation
no canonical mutation
no unlicensed full-text ingestion
```

## 4. Option A — Value Proof Infrastructure

### 4.1 Purpose

Build only the machinery required to prepare, run, and report a controlled Value Proof experiment.

### 4.2 Allowed components

- preregistration file writer
- prompt packet builder
- arm configuration registry
- blind packet generator
- evaluator response schema
- aggregation report generator
- value proof gate report skeleton

### 4.3 Required inputs

- `value_proof_preregistration_template.md`
- `value_proof_minimum_fixture_spec.md`
- LLM boundary ladder
- corpus source policy

### 4.4 Forbidden components

- production writing engine
- autonomous scene generator
- final manuscript writer
- hidden provider context
- post-hoc threshold adjustment

### 4.5 Exit evidence

```text
experiments/value_proof/preregister.json
experiments/value_proof/blind_packets/
experiments/value_proof/aggregate_report.md
release/current/value_proof_gate_report.md
```

### 4.6 Risk

Medium.

Reason: It may involve provider output later, but the first implementation can be scaffolding only.

## 5. Option B — Corpus and Formula Mapping Infrastructure

### 5.1 Purpose

Build only metadata corpus fixture and formula signal mapping support.

### 5.2 Allowed components

- metadata-only corpus fixture loader
- schema validator
- source-class validator
- formula-to-corpus mapping validator
- FormulaSignalRecord fixture generator

### 5.3 Required inputs

- narrative corpus source policy
- narrative corpus schema v0.1
- narrative corpus minimum fixture spec
- formula catalog normalization report
- formula-to-corpus mapping blueprint

### 5.4 Forbidden components

- full-text ingestion
- unlicensed content storage
- training pipeline
- automatic coefficient update

### 5.5 Exit evidence

```text
fixtures/narrative_corpus_minimum/fixture.json
fixtures/narrative_corpus_minimum/source_review.md
fixtures/formula_signal_mapping/minimal_mapping_report.md
```

### 5.6 Risk

Low to medium.

Reason: It can be metadata-only and deterministic if source policy is enforced.

## 6. Option C — Writer IDE Planning Prototype

### 6.1 Purpose

Build only a non-canonical writer review prototype that displays structured state, critic notes, and candidate comparisons.

### 6.2 Allowed components

- local UI mock or static prototype
- writer session record viewer
- approval decision mock flow
- formula signal panel
- corpus reference panel
- critic suggestion panel

### 6.3 Required inputs

- writer narrative IDE wireframe blueprint
- writer session record contract
- approval decision record contract
- LLM boundary ladder
- agent capability scope contract

### 6.4 Forbidden components

- automatic canonical write
- hidden memory update
- provider-autonomous drafting
- final text generation authority

### 6.5 Exit evidence

```text
docs/ui/page18_writer_ide_static_flow.md
fixtures/writer_session/minimal_session.json
fixtures/approval_decision/minimal_decision.json
```

### 6.6 Risk

Low if kept static and non-canonical.

## 7. Option D — LearnableCritic Audit Prototype

### 7.1 Purpose

Build only audit fixture and coefficient diff handling, not a full learning runtime.

### 7.2 Allowed components

- coefficient state fixture
- coefficient diff validator
- deterministic seed record validator
- rollback record validator
- human approval record validator

### 7.3 Required inputs

- LearnableCritic bridge blueprint
- LearnableCritic record contract
- coefficient audit record contract
- LearnableCritic audit fixture spec
- formula-to-corpus mapping blueprint

### 7.4 Forbidden components

- live hidden learning
- automatic coefficient promotion
- canonical mutation from critic output
- provider-based preference update without record

### 7.5 Exit evidence

```text
fixtures/learnable_critic_audit/minimal_fixture.json
fixtures/learnable_critic_audit/audit_report.md
```

### 7.6 Risk

Medium.

Reason: Even audit-only coefficient handling needs strict no-hidden-learning boundaries.

## 8. Recommended first Page18 scope

Recommended first scope:

```text
Option B — Corpus and Formula Mapping Infrastructure
```

Reason:

- lowest rights-managed implementation risk
- directly uses uploaded DB and formula materials
- supports Value Proof, LearnableCritic, Writer IDE, and multi-agent layers
- can remain deterministic and metadata-only

Recommended optional supporting scope:

```text
Option A — Value Proof Infrastructure scaffolding only
```

## 9. Scope decision matrix

| Criterion | Option A | Option B | Option C | Option D |
|---|---|---|---|---|
| Implementation risk | Medium | Low-Medium | Low | Medium |
| Uses uploaded DB | Indirect | Direct | Indirect | Indirect |
| Uses uploaded formulas | Indirect | Direct | Indirect | Direct |
| Enables Value Proof | Direct | Strong support | Medium support | Medium support |
| Rights risk | Medium | Low if metadata-only | Low | Low |
| Canonical mutation risk | Low | Low | Medium if not controlled | Medium |
| Recommended order | 2 | 1 | 4 | 3 |

## 10. Final rule

Page18 may only choose a scope after the entry state moves out of DECISIONS_PENDING.

The first Page18 implementation should be narrow, reversible, evidence-producing, and non-canonical.
