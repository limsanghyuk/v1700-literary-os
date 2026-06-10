# Formula Catalog Normalization Report

Status: review draft
Created: 2026-06-07
Scope: Uploaded formula archives, V1700 formula lineage, Claude/literary-os formula references
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This report normalizes formula references across uploaded formula archives and the current V1700 planning context.

It does not implement formulas. It creates a planning-level catalog so later architecture can map formulas to corpus fields, LearnableCritic records, and value proof metrics.

## 2. Source documents

Uploaded formula archive:

```text
적용 공식-20260607T122627Z-3-001.zip
```

Inspected documents:

```text
Sovereign OS_ 수리 서사학 대통일 명세서 (V2.0 - Dynamics & Stochasticity).docx
V1700_FORMULA_SYSTEM_STAGE126_TO_STAGE184_EVOLUTION_REPORT.md.docx
sovereign_os_formula_spec_v1.1.docx
V1700 공식 대정리.docx
formula_evolution_v485_to_v620.docx
Literary_OS_Formula_Master_Reference.docx
sovereign_os_formula_spec_v2.0.docx
```

Related planning documents:

```text
docs/reviews/dual_model_context_uploaded_formula_db_consolidation_report.md
docs/reviews/literary_os_v745_to_v1700_absorption_matrix.md
docs/architecture/learnable_critic_bridge_blueprint.md
docs/architecture/post_roadmap_value_proof_gate_blueprint.md
docs/architecture/narrative_corpus_database_blueprint.md
```

## 3. Lineage labels

Every formula must be labeled as one of:

- GPT_V1700_FORMULA
- SOVEREIGN_OS_FORMULA_SPEC
- CLAUDE_LITERARY_OS_FORMULA
- SHARED_HISTORICAL_FORMULA
- UPLOADED_USER_FORMULA_ARCHIVE
- DUPLICATE_OR_OVERLAP
- UNRESOLVED_LINEAGE

## 4. Normalized formula groups

### 4.1 Dynamic Recursive State Equation

Canonical label:

```text
DRSE
```

Lineage:

```text
SOVEREIGN_OS_FORMULA_SPEC / GPT_V1700_FORMULA / UPLOADED_USER_FORMULA_ARCHIVE
```

Function:

- model dynamic story state transition
- update narrative state across scene or event progression
- provide state continuity basis

V1700 planning target:

- formula_to_corpus_mapping_blueprint
- LearnableCritic bridge
- NarrativeStateTensor calibration

Status:

```text
ACCEPT_FOR_V1700_PLANNING
```

### 4.2 Narrative State Tensor

Canonical label:

```text
NST
```

Function:

- multi-dimensional representation of narrative state
- likely dimensions: character, conflict, emotion, time, causality, tension, reader signal

V1700 planning target:

- narrative_corpus_schema_v0_1
- writer IDE right panel
- Value Proof metrics

Status:

```text
ACCEPT_FOR_V1700_PLANNING
```

### 4.3 Narrative Fitness Score

Canonical label:

```text
NFS
```

Function:

- aggregate quality or fitness score
- may combine tension, coherence, payoff, novelty, emotional momentum, and genre fit

Boundary:

NFS cannot replace blind human evaluation in Value Proof.

V1700 planning target:

- Value Proof metric companion
- LearnableCritic advisory output

Status:

```text
ACCEPT_WITH_BOUNDARY
```

### 4.4 Gradient coefficient update

Canonical label:

```text
COEFFICIENT_UPDATE
```

Function:

- adjust formula coefficients using learning or calibration signal

Boundary:

Requires:

- coefficient state
- coefficient diff
- deterministic seed
- source signal
- audit log
- rollback record
- human review before promotion

V1700 planning target:

- coefficient_audit_record_contract
- LearnableCriticRecord

Status:

```text
ACCEPT_WITH_AUDIT_AND_ROLLBACK
```

### 4.5 Emotional Momentum

Canonical label:

```text
EMOTIONAL_MOMENTUM
```

Function:

- track emotional movement across scenes or character interactions
- measure emotional acceleration, reversal, sustain, or dissipation

V1700 planning target:

- SceneRecord emotional_start / emotional_end
- CharacterArcRecord behavior_shift
- Value Proof dimensions

Status:

```text
ACCEPT_FOR_V1700_PLANNING
```

### 4.6 Character Interaction Matrix

Canonical label:

```text
CIM
```

Function:

- matrix of character relationships, pressure, influence, alliance, conflict, and hidden dependency

V1700 planning target:

- CharacterRecord
- RelationshipGraphRecord
- Corpus graph adapter
- Writer IDE left zone

Status:

```text
ACCEPT_FOR_V1700_PLANNING
```

### 4.7 Triangle Tension

Canonical label:

```text
TRIANGLE_TENSION
```

Function:

- model three-node tension among characters, goals, institutions, or values

V1700 planning target:

- Conflict_Axis
- CharacterArcRecord
- SceneBlueprintRecord
- tension curve metrics

Status:

```text
ACCEPT_FOR_V1700_PLANNING
```

### 4.8 RAG / BM25 / RRF retrieval fusion

Canonical label:

```text
RETRIEVAL_FUSION
```

Function:

- combine lexical and semantic retrieval for story memory, corpus examples, and reference search

Boundary:

Must respect corpus source policy and rights labels.

V1700 planning target:

- narrative_corpus_source_policy
- corpus retrieval adapter
- writer IDE reference panel

Status:

```text
ACCEPT_WITH_RIGHTS_BOUNDARY
```

### 4.9 Fourier tension curve

Canonical label:

```text
TENSION_CURVE_FOURIER
```

Function:

- represent macro tension curve as periodic or frequency-like structure
- compare scene arcs, episode arcs, and season arcs

V1700 planning target:

- Value Proof metric companion
- SceneRecord tension_delta
- EpisodeOrChapterRecord turning points

Status:

```text
ACCEPT_FOR_V1700_PLANNING
```

### 4.10 ASD / GIG self-healing and causal graph logic

Canonical label:

```text
CAUSAL_SELF_HEALING
```

Function:

- detect and repair causality gaps
- maintain graph integrity across story events

Boundary:

Must remain advisory unless a future writer approval contract promotes a repair.

V1700 planning target:

- CausalityMatrixRecord
- Writer IDE critic panel
- LearnableCritic explanation record

Status:

```text
ACCEPT_WITH_WRITER_APPROVAL_BOUNDARY
```

### 4.11 Governance / evaluation / evolution / hub authority layers

Canonical label:

```text
AUTHORITY_LAYER_FORMULAS
```

Function:

- model evaluation body, governance body, evolution body, procedure/hub/package authority

V1700 planning target:

- post-roadmap integrity self-verification
- clean release authority
- Page18 entry criteria

Status:

```text
ACCEPT_FOR_V1700_PLANNING
```

## 5. Duplicate and overlap resolution

Potential overlaps:

| Overlap | Resolution |
|---|---|
| DRSE vs NarrativeStateTensor update | DRSE is transition rule; NST is state representation |
| Narrative Fitness vs Value Proof result | Fitness is internal metric; Value Proof is external validation |
| Emotional Momentum vs tension curve | emotional momentum is affective movement; tension curve is structural pressure movement |
| RAG retrieval vs corpus DB | retrieval is access mechanism; corpus DB is governed data store |
| LearnableCritic vs formula authority | LearnableCritic calibrates; it does not delete formula authority |
| causal self-healing vs canonical rewrite | self-healing proposes repair; writer approval controls canonical change |

## 6. Required normalized catalog records

Future contract should define:

```text
FormulaCatalogRecord
FormulaLineageRecord
FormulaAliasRecord
FormulaInputSchemaRef
FormulaOutputSchemaRef
FormulaCorpusMappingRef
FormulaCriticMappingRef
FormulaValueProofMappingRef
FormulaBoundaryRule
FormulaAuditRequirement
```

## 7. Mapping targets

Every accepted formula must map to at least one of:

- corpus field
- critic record
- value proof metric
- writer IDE panel
- release authority rule
- GitNexus trace or evidence document

## 8. High-priority next formulas for mapping

Priority 1:

- DRSE
- Narrative State Tensor
- Narrative Fitness Score
- Emotional Momentum
- Character Interaction Matrix
- Causality Matrix linkage

Priority 2:

- RAG/BM25/RRF retrieval fusion
- Fourier tension curve
- Triangle Tension
- Critic thresholds

Priority 3:

- self-healing causal graph logic
- governance/hub authority formulas
- RL/MAE reward logic

## 9. Final recommendation

Do not add new formulas before normalization.

First create:

```text
docs/architecture/formula_to_corpus_mapping_blueprint.md
```

Then create contracts for:

```text
FormulaCatalogRecord
FormulaLineageRecord
FormulaCorpusMappingRef
CoefficientAuditRecord
```

## 10. Final decision

The uploaded formula archive is accepted as a planning source.

It is not automatically runtime-authoritative.

Formula authority must be normalized, mapped, audited, and then connected to corpus and critic records before implementation.
