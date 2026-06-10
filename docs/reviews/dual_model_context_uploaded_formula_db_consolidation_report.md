# Dual-Model Context and Uploaded Formula/DB Consolidation Report

Status: review draft
Created: 2026-06-07
Scope: planning consolidation after new uploaded formula and database archives
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This report consolidates the current planning context after the user uploaded additional formula and database archives.

It also records a strict distinction between two parallel development tracks:

1. GPT/V1700 track — `limsanghyuk/v1700-literary-os`
2. Claude/literary-os track — `limsanghyuk/literary-os`

These tracks must not be confused. They may cross-reference and absorb ideas through explicit review documents, but they are separate model lineages.

## 2. Non-confusion rule

### 2.1 GPT / V1700 track

Current nature:

- page/stage authority system
- GitNexus evidence discipline
- contract / manifest / release gate governance
- Page08~Page17 roadmap completed through Stage242
- current mode: post-roadmap planning and authority review
- Page18 implementation remains absent
- Stage243+ implementation remains absent

Current strength:

- authority, lineage, governance, canonical story boundaries, approval discipline

Current weakness:

- not yet a complete runtime writing engine
- needs value proof, corpus, UI/UX, execution engine, and runtime bridge

### 2.2 Claude / literary-os track

Current nature:

- runtime-heavy executable literary engine
- Python package implementation
- tests, release gates, preflight, plugin sandboxing, FL/DR/observability
- latest reviewed baseline: V745 / v13.0.0 / Phase D Exit
- next direction: Phase E validation-first entry

Current strength:

- runtime execution maturity and test/gate infrastructure

Current weakness:

- less explicit page/stage authority and GitNexus governance than V1700

### 2.3 Integration principle

Do not merge directly.

Use this path instead:

```text
Claude literary-os runtime lessons
→ V1700 absorption matrix
→ accept / reject / defer decision
→ V1700-compatible contract / gate / evidence mapping
→ later implementation only after entry criteria
```

## 3. Uploaded archive inventory

### 3.1 Formula archive

Uploaded file:

```text
적용 공식-20260607T122627Z-3-001.zip
```

SHA256:

```text
152b114c1767a1be387e5d8dfa27c75a5d45b4cae1d1ba46f28a524689f742b4
```

Files inspected:

```text
적용 공식/Sovereign OS_ 수리 서사학 대통일 명세서 (V2.0 - Dynamics & Stochasticity).docx
적용 공식/V1700_FORMULA_SYSTEM_STAGE126_TO_STAGE184_EVOLUTION_REPORT.md.docx
적용 공식/sovereign_os_formula_spec_v1.1.docx
적용 공식/V1700 공식 대정리.docx
적용 공식/formula_evolution_v485_to_v620.docx
적용 공식/Literary_OS_Formula_Master_Reference.docx
적용 공식/sovereign_os_formula_spec_v2.0.docx
```

### 3.2 Database archive

Uploaded file:

```text
drive-download-20260605T122610Z-3-001.zip
```

SHA256:

```text
ce130705ecc7212ae9391bb7e81130c4abf303b5ebe8ec18b7be62cd58ae3225
```

Files inspected:

```text
[V21.0 Master DB 물리적 로우 데이터 덤프_ PART 1 _ 2].docx
[V21.0 Master DB 물리적 로우 데이터 덤프_ PART 2_ 2].docx
[V21.0 Master DB 물리적 로우 데이터 덤프_ 영화.docx
```

## 4. Formula archive findings

The formula archive provides a layered mathematical and engineering foundation for narrative control.

### 4.1 Core formula themes

Observed themes:

- DRSE dynamic recursive state equation
- Narrative State Tensor
- narrative time dilation
- temporal decay
- concurrency collision
- narrative fitness score
- gradient descent coefficient update
- MAE/RL reward logic
- emotional momentum
- character interaction matrix
- triangle tension
- RAG/BM25/RRF retrieval fusion
- Fourier tension curve
- ASD/GIG self-healing and causal graph logic
- cross-lineage release authority
- governance, evaluation, evolution, hub/package authority layers

### 4.2 V1700 Stage126 to Stage184 evolution

The uploaded Stage126 to Stage184 report states that Stage126 was mainly a narrative physics, reward, emotional momentum, character graph, RAG, tension curve, stability, quality, prediction, safety, and integrity formula catalog.

The Stage184 evolution adds:

```text
Layer 13 — Evaluation Body
Layer 14 — Governance Body
Layer 15 — Evolution Body
Layer 16 — Procedure / Hub / Package Authority
```

Planning implication:

V1700 already has a substantial formula and authority base. The next step should not be inventing more formulas randomly. It should be:

```text
formula catalog normalization
→ formula-to-stage mapping
→ formula-to-data schema mapping
→ formula-to-LearnableCritic mapping
→ formula-to-ValueProof measurement mapping
```

### 4.3 Sovereign OS formula specifications

The formula specs v1.1 and v2.0 record a deterministic, local, no-live-LLM narrative physics engine orientation.

Planning implication:

This reinforces the V1700 boundary:

- formulas remain interpretable control and critique mechanisms
- LLM support is allowed only through staged boundary rules
- LearnableCritic may calibrate formulas but must not erase formula authority

### 4.4 Literary OS formula master reference and v485 to v620 evolution

The uploaded formula master and v485 to v620 evolution documents show a long formula lineage from V480/V485 through V620.

Notable trajectory:

- early deterministic narrative physics
- LoRA fine-tuning formulas
- RLHF loop formulas
- MultiWork collaboration formulas
- pipeline and governance expansion

Planning implication:

The absorption matrix must account for formula lineage across both tracks. Some formulas belong to Claude/literary-os runtime history. Some belong to GPT/V1700 authority history. They should be mapped explicitly before use.

## 5. Database archive findings

The database archive provides structured narrative analysis records, not raw unstructured prose.

### 5.1 K-Drama Master Database dumps

Two documents contain `K_Drama_Master_Database version="19.0_Engine"` physical migration dumps.

Approximate inspected records:

```text
PART 1: 50 Drama_Entry records
PART 2: 50 Drama_Entry records
```

Observed schema components:

- Drama_Entry
- Section_00_Core_Philosophy
- Master_Theme
- Conflict_Axis
- Section_01_Lorebook_Database
- Character
- Key_Object
- Section_02_Macro_Architecture_and_Causality
- Causality_Matrix
- Trigger
- Resolution
- Residue
- Section_03_Sub_Writer_Rendering_Engine
- Dialogue_Tone
- Style_Module
- Critic_Thresholds
- Tone_Penalty

Planning implication:

This is directly relevant to the planned `Narrative Corpus Database Blueprint`. It means V1700 does not need to start from an empty corpus schema. It can use these physical row dumps as a schema seed, subject to rights and provenance policy.

### 5.2 Cinematic Master DB dump

The movie document uses `ReplicationEngine_Universal_Narrative version="21.0_Cinematic_Sovereign"`.

Approximate inspected records:

```text
Movie dump: 79 Drama_Entry records
```

Additional schema components include:

- Core_Dilemma
- Catastrophe_Source
- Logic_Consistency
- Rendering_Engine
- Scene_Blueprint
- Scene_Blueprint_V8
- Tragic_Engine

Planning implication:

The corpus database should support not only Korean dramas but also film/cinematic narrative records. The current V1700 corpus blueprint should be expanded into a universal narrative schema that can ingest drama, film, animation, and novel metadata records through typed adapters.

## 6. Impact on current V1700 planning

### 6.1 Existing plan remains valid

The existing long-range priority roadmap remains valid:

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

### 6.2 New uploaded data sharpens P3 and P5

The uploads make two areas more concrete:

1. P3 Narrative Corpus Database
2. P5 Learnable Critic Bridge

The formula documents supply the formula/critic side.

The DB dumps supply the corpus/schema side.

These should now be treated as paired planning assets.

## 7. Revised planning gaps after upload

### Gap 1 — Formula-to-corpus mapping is missing

Required document:

```text
docs/architecture/formula_to_corpus_mapping_blueprint.md
```

Purpose:

Map formulas like DRSE, NarrativeStateTensor, FitnessScore, EmotionalMomentum, CIM, RAG, tension curve, and governance gates to corpus fields like Master_Theme, Conflict_Axis, Character, Key_Object, Trigger, Resolution, Residue, Dialogue_Tone, and Critic_Thresholds.

### Gap 2 — Corpus source policy must distinguish user-provided structured DB from external copyrighted sources

Required document:

```text
docs/policies/narrative_corpus_source_policy.md
```

Purpose:

Classify:

- user-provided structured analysis DB
- public-domain text
- licensed material
- metadata-only analysis records
- restricted copyrighted full text

### Gap 3 — Schema v0.1 should use uploaded DB schema as seed

Required document:

```text
docs/architecture/narrative_corpus_schema_v0_1.md
```

Seed tables:

- WorkRecord
- DramaEntryRecord
- CorePhilosophyRecord
- LorebookRecord
- CharacterRecord
- KeyObjectRecord
- CausalityMatrixRecord
- SceneBlueprintRecord
- CriticThresholdRecord
- AudienceSignalRecord

### Gap 4 — Formula catalog normalization is missing

Required document:

```text
docs/reviews/formula_catalog_normalization_report.md
```

Purpose:

Resolve overlap between:

- GPT V1700 formula catalog
- Sovereign OS formula specs
- Literary OS formula master reference
- v485 to v620 evolution formulas
- Stage126 to Stage184 formula evolution

### Gap 5 — Dual-model lineage policy is missing

Required document:

```text
docs/policies/dual_model_lineage_policy.md
```

Purpose:

Prevent confusion between:

- GPT/V1700 authority kernel
- Claude/literary-os runtime engine
- shared formula references
- shared corpus assets
- future absorption decisions

## 8. Updated priority order after upload

The next planning sequence should now be:

```text
P1-A: dual_model_lineage_policy
P1-B: literary_os_v745_to_v1700_absorption_matrix
P1-C: formula_catalog_normalization_report
P1-D: v1700_post_roadmap_integrity_self_verification_blueprint
P2-A: value_proof_preregistration_template
P2-B: value_proof_minimum_fixture_spec
P3-A: narrative_corpus_source_policy
P3-B: narrative_corpus_schema_v0_1
P3-C: formula_to_corpus_mapping_blueprint
P4-A: v1700_llm_boundary_ladder_blueprint
P5-A: learnable_critic_record_contract
P5-B: coefficient_audit_record_contract
P6-A: writer_narrative_ide_wireframe_blueprint
P6-B: multi_agent_supervision_blueprint
P7: page18_entry_criteria
```

## 9. Final decision

The uploaded files do not invalidate the current roadmap. They strengthen it.

The key new conclusion is:

```text
V1700's next planning layer should connect formulas and corpus records before any execution-engine implementation.
```

Therefore, the immediate next planning work should be:

1. dual model lineage policy
2. formula catalog normalization
3. narrative corpus source policy
4. narrative corpus schema v0.1
5. formula-to-corpus mapping blueprint

Page18 remains closed.

Stage243+ remains absent.

Implementation remains blocked until entry criteria are explicitly satisfied.
