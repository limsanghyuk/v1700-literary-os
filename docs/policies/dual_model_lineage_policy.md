# Dual Model Lineage Policy

Status: policy draft
Created: 2026-06-07
Scope: GPT/V1700 track and Claude/literary-os track separation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This policy prevents confusion between two parallel literary model development tracks:

1. GPT/V1700 track — `limsanghyuk/v1700-literary-os`
2. Claude/literary-os track — `limsanghyuk/literary-os`

The two tracks may exchange ideas through documented absorption review, but they are not the same model and must not be merged implicitly.

## 2. Track definitions

### 2.1 GPT/V1700 track

Primary repository:

```text
limsanghyuk/v1700-literary-os
```

Nature:

- page/stage authority system
- GitNexus evidence discipline
- contract, manifest, and release gate governance
- Page08~Page17 roadmap completed through Stage242
- current mode: post-roadmap planning and authority review
- Page18 implementation absent
- Stage243+ implementation absent

Primary strength:

- authority governance
- lineage trace
- canonical story boundary
- human approval boundary
- review/share/production/plugin boundary

Primary weakness:

- not yet a complete executable writing engine
- needs runtime bridge, value proof, corpus schema, writer IDE, LearnableCritic, and multi-agent supervision planning

### 2.2 Claude/literary-os track

Primary repository:

```text
limsanghyuk/literary-os
```

Nature:

- runtime-heavy executable literary engine
- Python package implementation
- tests, release gates, preflight, plugin sandboxing, FL/DR/observability
- latest reviewed baseline: V745 / v13.0.0 / Phase D Exit
- next direction: Phase E validation-first entry

Primary strength:

- executable runtime architecture
- test/gate/preflight infrastructure
- Phase E/F/G transition planning

Primary weakness:

- less explicit V1700-style page/stage authority and GitNexus evidence governance

## 3. Non-confusion rules

### Rule 1 — No implicit identity

A concept, formula, module, gate, or document from one track is not automatically authoritative in the other track.

### Rule 2 — No direct merge

Do not directly merge Claude/literary-os runtime decisions into V1700.

Use an absorption path:

```text
external idea
→ absorption matrix row
→ accept / reject / defer
→ V1700-compatible contract mapping
→ V1700-compatible gate mapping
→ evidence path mapping
→ implementation only after entry criteria
```

### Rule 3 — Shared formulas need lineage labels

Formula references must identify their lineage:

- GPT/V1700 formula
- Sovereign OS formula spec
- Claude/literary-os runtime formula
- shared historical formula
- uploaded user formula archive
- unresolved or duplicate formula

### Rule 4 — Shared corpus assets need rights and source labels

Corpus records must identify their source class:

- user-provided structured analysis DB
- user-owned source
- public-domain source
- licensed source
- metadata-only analysis record
- restricted copyrighted full text
- unknown or unresolved source

### Rule 5 — Runtime evidence is not authority evidence by itself

Claude runtime tests, gates, or outputs do not automatically become V1700 authority evidence.

They can become evidence only after:

- absorption matrix acceptance
- target V1700 artifact definition
- GitNexus-compatible trace path
- V1700 release gate or review document update

### Rule 6 — V1700 authority does not replace runtime validation

V1700 page/stage authority does not prove runtime literary quality.

Runtime quality must be tested by:

- value proof experiment
- corpus-backed evaluation
- blind writer or reader review
- preregistered threshold
- effect size or transparent result reporting

## 4. Accepted interaction types

Allowed:

- cross-comparison reports
- absorption matrix entries
- formula normalization reports
- corpus schema mapping
- value proof designs
- LearnableCritic bridge designs
- runtime integrity bridge designs
- implementation proposals after entry criteria

Not allowed:

- silent copying of modules
- silent reuse of gates
- silent formula authority transfer
- silent corpus ingestion
- Page18 or Stage243+ implementation without entry criteria

## 5. Required review artifacts

Before any Claude/literary-os concept is absorbed into V1700, create or update:

```text
docs/reviews/literary_os_v745_to_v1700_absorption_matrix.md
```

For formulas:

```text
docs/reviews/formula_catalog_normalization_report.md
```

For corpus/data:

```text
docs/policies/narrative_corpus_source_policy.md
docs/architecture/narrative_corpus_schema_v0_1.md
```

For formula/data connection:

```text
docs/architecture/formula_to_corpus_mapping_blueprint.md
```

## 6. Decision statuses

Every cross-track concept must be assigned one of:

- ACCEPT_FOR_V1700_PLANNING
- ACCEPT_FOR_V1700_IMPLEMENTATION_AFTER_ENTRY_GATE
- DEFER_PENDING_EVIDENCE
- REJECT_FOR_AUTHORITY_CONFLICT
- REJECT_FOR_RIGHTS_OR_SOURCE_RISK
- REJECT_FOR_RUNTIME_SCOPE_MISMATCH

## 7. Current immediate sequence

The next ordered work is:

```text
P1-A dual_model_lineage_policy
P1-B literary_os_v745_to_v1700_absorption_matrix
P1-C formula_catalog_normalization_report
P1-D v1700_post_roadmap_integrity_self_verification_blueprint
P2-A value_proof_preregistration_template
P2-B value_proof_minimum_fixture_spec
P3-A narrative_corpus_source_policy
P3-B narrative_corpus_schema_v0_1
P3-C formula_to_corpus_mapping_blueprint
```

## 8. Final policy statement

The GPT/V1700 and Claude/literary-os tracks are complementary but separate.

V1700 may learn from Claude's executable runtime maturity.

Claude/literary-os may inform V1700's runtime bridge.

But all absorption into V1700 must pass through documented policy, mapping, gate, and evidence review.
