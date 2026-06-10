# Formula Signal Record Contract

Status: contract draft
Created: 2026-06-10
Scope: FormulaSignalRecord emitted from formula-to-corpus mapping
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This contract defines the record emitted when a normalized formula reads metadata-only corpus records and produces an advisory signal.

Formula signals are traceable advisory artifacts. They are not canonical story truth by default.

## 2. Required record

```text
FormulaSignalRecord
```

## 3. Required fields

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
signal_type_label
critic_mapping_ref
value_proof_mapping_ref
writer_ide_panel_ref
created_at
review_status
```

## 4. Signal type labels

```text
PLACEHOLDER_SIGNAL
MANUAL_REVIEW_SIGNAL
FIXTURE_SIGNAL
CALCULATED_SIGNAL
```

## 5. Output signal types

Initial allowed output signal types:

```text
NARRATIVE_STATE_TENSOR_SIGNAL
EMOTIONAL_MOMENTUM_SIGNAL
CHARACTER_INTERACTION_SIGNAL
CAUSALITY_TRANSITION_SIGNAL
NARRATIVE_FITNESS_COMPANION_SIGNAL
SOURCE_RISK_SIGNAL
AUTHORITY_WARNING_SIGNAL
```

## 6. Review statuses

```text
DRAFT
VALID_FOR_SCHEMA_WIRING
VALID_FOR_UI_WIRING
VALID_FOR_VALUE_PROOF_PREREGISTRATION
VALID_FOR_LEARNABLE_CRITIC_AUDIT
REJECTED
SUPERSEDED
```

## 7. Consumer rules

### Value Proof

A FormulaSignalRecord may be used only if preregistered.

### LearnableCritic

A FormulaSignalRecord may be used only through CriticInputSourceRecord and coefficient audit records.

### Writer IDE

A FormulaSignalRecord may be displayed only as advisory signal.

### Multi-agent supervision

Agents may cite FormulaSignalRecord only within capability scope.

## 8. Blocking failures

- missing formula_signal_id
- missing formula_id
- missing source_record_ids
- source records unavailable in corpus fixture
- input fields unavailable in schema
- source class or rights status missing
- placeholder signal treated as calculated proof
- signal mutates canonical story state
- signal used for coefficient update without audit
- signal used in Value Proof without preregistration

## 9. Final decision

FormulaSignalRecord is the canonical bridge between formula catalog and corpus metadata, but it remains advisory until another approved contract consumes it.
