# Formula Signal Mapping Minimal Report Blueprint

Status: blueprint draft
Created: 2026-06-10
Scope: future minimal formula signal mapping report
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This document defines the structure of the future minimal mapping report connecting formula groups to metadata-only corpus records.

It is intended for Page18 Option B planning.

## 2. Future report location

Proposed path:

```text
fixtures/formula_signal_mapping/minimal_mapping_report.md
```

## 3. Required report sections

```text
1. Mapping purpose
2. Fixture source summary
3. Formula groups covered
4. Corpus record types covered
5. Field-level mapping table
6. FormulaSignalRecord inventory
7. Placeholder vs calculated signal status
8. Rights and source policy compliance
9. Validation result
10. Blocking failures
11. Next recommended mapping
```

## 4. Required mapping table columns

```text
formula_group
formula_id
source_record_type
source_record_id
input_field_names
output_signal_type
output_signal_label_or_value
explanation_summary
review_status
```

## 5. Minimum formula groups

First report should cover:

```text
NARRATIVE_STATE_TENSOR_SIGNAL
EMOTIONAL_MOMENTUM_SIGNAL
CHARACTER_INTERACTION_SIGNAL
CAUSALITY_TRANSITION_SIGNAL
NARRATIVE_FITNESS_COMPANION_SIGNAL
```

## 6. Minimum corpus records

First report should include mappings to:

```text
WorkRecord
CharacterRecord
CausalityMatrixRecord
SceneBlueprintRecord
RelationshipGraphRecord
CriticThresholdRecord
```

## 7. Placeholder status labels

```text
PLACEHOLDER_SIGNAL
MANUAL_REVIEW_SIGNAL
FIXTURE_SIGNAL
CALCULATED_SIGNAL
```

The report must not treat placeholder signals as proof of formula performance.

## 8. Validation outcome labels

```text
VALID_FOR_SCHEMA_WIRING
VALID_FOR_UI_WIRING
VALID_FOR_VALUE_PROOF_PREREGISTRATION
VALID_FOR_LEARNABLE_CRITIC_AUDIT
REJECTED
```

## 9. Blocking failures

- missing formula_id
- missing source_record_id
- input fields do not exist in schema
- source policy missing
- rights status missing
- placeholder signal reported as calculated proof
- mapping uses restricted full text

## 10. Final decision

The minimal mapping report is required before formula signals are used by Value Proof, LearnableCritic, or Writer IDE prototypes.
