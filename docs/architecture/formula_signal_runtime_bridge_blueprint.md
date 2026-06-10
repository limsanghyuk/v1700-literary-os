# Formula Signal Runtime Bridge Blueprint

Status: blueprint draft
Created: 2026-06-10
Scope: formula signal bridge planning, no implementation
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This blueprint defines a future bridge between normalized formulas and V1700 corpus records.

It does not implement formula computation. It defines how formula signals should be represented, validated, traced, and consumed by later Value Proof, LearnableCritic, Writer IDE, and multi-agent systems.

## 2. Position in roadmap

This bridge supports:

- Page18 Option B: Corpus and Formula Mapping Infrastructure
- Value Proof Arm B guidance
- LearnableCritic audit fixture
- Writer IDE critic panel
- multi-agent supervision

## 3. Inputs

Required input records:

- FormulaCatalogRecord
- FormulaLineageRecord
- WorkRecord
- CharacterRecord
- CausalityMatrixRecord
- SceneBlueprintRecord
- RelationshipGraphRecord
- CriticThresholdRecord

Optional input records:

- AudienceSignalRecord
- GenreEngineRecord
- DialogueFunctionRecord

## 4. Output record

Canonical output:

```text
FormulaSignalRecord
```

Required fields:

```text
formula_signal_id
formula_id
formula_group
source_record_ids
source_record_types
input_field_names
source_class_summary
rights_status_summary
output_signal_type
output_signal_value_or_label
confidence
explanation_summary
critic_mapping_ref
value_proof_mapping_ref
writer_ide_panel_ref
created_at
review_status
```

## 5. Supported first signal groups

First fixture should support only:

```text
NARRATIVE_STATE_TENSOR_SIGNAL
EMOTIONAL_MOMENTUM_SIGNAL
CHARACTER_INTERACTION_SIGNAL
CAUSALITY_TRANSITION_SIGNAL
NARRATIVE_FITNESS_COMPANION_SIGNAL
```

Reason:

These map directly to schema v0.1 and do not require full execution-engine generation.

## 6. Signal generation pipeline

```text
select formula group
select allowed corpus records
validate source classes
validate rights statuses
read declared input fields
emit deterministic placeholder or calculated signal
attach explanation
attach trace links
set review status
```

## 7. Deterministic placeholder mode

Before full runtime implementation, the bridge may emit placeholder signals if clearly labeled:

```text
PLACEHOLDER_SIGNAL
MANUAL_REVIEW_SIGNAL
FIXTURE_SIGNAL
CALCULATED_SIGNAL
```

Placeholder signals cannot be used as proof of formula performance.

They may be used for schema and UI wiring tests.

## 8. Consumers

### 8.1 Value Proof

Value Proof may use formula signals only if preregistered.

### 8.2 LearnableCritic

LearnableCritic may read signals through CriticInputSourceRecord only.

### 8.3 Writer IDE

Writer IDE may display signals as advisory notes only.

### 8.4 Multi-agent supervision

Agents may cite formula signals only within their capability scope.

## 9. Blocking failures

- FormulaSignalRecord has no source record
- source class missing
- rights status missing
- placeholder signal treated as proof
- formula signal mutates canonical story state
- signal used in Value Proof without preregistration
- signal used for coefficient update without audit trail

## 10. Final decision

Formula signal bridge should be the first runtime-adjacent design layer, but it must remain traceable, metadata-based, and advisory until later gates approve implementation.
