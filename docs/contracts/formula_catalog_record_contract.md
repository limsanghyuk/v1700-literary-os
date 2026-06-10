# Formula Catalog Record Contract

Status: contract draft
Created: 2026-06-10
Scope: normalized formula catalog records
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This contract defines the normalized record structure for formula catalog entries used by V1700 planning, formula signal mapping, Value Proof, LearnableCritic, Writer IDE, and multi-agent supervision.

## 2. Required records

```text
FormulaCatalogRecord
FormulaLineageRecord
FormulaAliasRecord
FormulaInputSchemaRef
FormulaOutputSchemaRef
FormulaBoundaryRule
```

## 3. FormulaCatalogRecord fields

```text
formula_id
formula_name
formula_group
canonical_label
lineage_ref
alias_refs
purpose
input_schema_refs
output_schema_refs
allowed_consumer_refs
boundary_rule_refs
review_status
created_at
updated_at
```

## 4. Formula lineage labels

```text
GPT_V1700_FORMULA
SOVEREIGN_OS_FORMULA_SPEC
CLAUDE_LITERARY_OS_FORMULA
SHARED_HISTORICAL_FORMULA
UPLOADED_USER_FORMULA_ARCHIVE
DUPLICATE_OR_OVERLAP
UNRESOLVED_LINEAGE
```

## 5. Formula groups

Initial supported groups:

```text
DRSE
NARRATIVE_STATE_TENSOR
NARRATIVE_FITNESS_SCORE
EMOTIONAL_MOMENTUM
CHARACTER_INTERACTION_MATRIX
TRIANGLE_TENSION
RETRIEVAL_FUSION
TENSION_CURVE_FOURIER
CAUSAL_SELF_HEALING
AUTHORITY_LAYER_FORMULAS
```

## 6. Allowed consumers

```text
FORMULA_SIGNAL_RUNTIME_BRIDGE
VALUE_PROOF_PREREGISTRATION
LEARNABLE_CRITIC_AUDIT
WRITER_IDE_ADVISORY_PANEL
MULTI_AGENT_SUPERVISION
RELEASE_AUTHORITY_REVIEW
```

## 7. Boundary rules

Every formula must declare whether it is:

```text
ADVISORY_ONLY
VALID_FOR_SCHEMA_WIRING
VALID_FOR_UI_WIRING
VALID_FOR_VALUE_PROOF_PREREGISTRATION
VALID_FOR_LEARNABLE_CRITIC_AUDIT
NOT_VALID_FOR_RUNTIME_USE
```

## 8. Blocking failures

- missing formula_id
- missing formula_group
- missing lineage_ref
- unresolved lineage used as authoritative formula
- duplicate formula without alias or merge decision
- formula used without declared input/output schema refs
- formula treated as canonical story authority

## 9. Final decision

FormulaCatalogRecord is required before any formula can emit a FormulaSignalRecord for downstream V1700 systems.
