# Learnable Critic Record Contract

Status: contract draft
Created: 2026-06-07
Scope: LearnableCritic planning contract
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This contract defines the required record structure for a future LearnableCritic layer.

The LearnableCritic remains advisory. It does not become canonical story authority, formula authority, or hidden memory.

## 2. Required record groups

```text
LearnableCriticConfig
CriticInputSourceRecord
FormulaSignalRef
CorpusSignalRef
CoefficientStateRef
CoefficientDiffRef
DeterministicSeedRef
AlignmentResultRef
RollbackRef
HumanReviewRef
AdvisoryOutputRef
```

## 3. LearnableCriticConfig

Fields:

```text
critic_id
critic_name
critic_axis
allowed_input_types
allowed_output_types
coefficient_schema_ref
source_policy_ref
approval_policy_ref
status
```

## 4. CriticInputSourceRecord

Fields:

```text
input_source_id
critic_id
source_record_id
source_record_type
source_class
rights_status
formula_signal_ref
corpus_signal_ref
value_proof_ref
provenance_ref
```

## 5. AdvisoryOutputRecord

Fields:

```text
advisory_output_id
critic_id
input_source_refs
output_type
score_or_label
explanation
confidence
suggested_action
canonical_mutation_allowed: false
review_status
```

## 6. Rules

- critic output is advisory by default
- every input must be source-linked
- every source must carry source_class and rights_status
- every coefficient change must use a coefficient audit record
- human review is required before any promotion
- no hidden preference update
- no Node authority override
- no raw provider output into core authority

## 7. Blocking failures

- input source missing
- source_class missing
- rights_status missing
- advisory output lacks explanation
- canonical_mutation_allowed is true
- coefficient change without audit record
- hidden preference update detected
- critic output promoted without human review

## 8. Integration targets

- docs/architecture/learnable_critic_bridge_blueprint.md
- docs/contracts/coefficient_audit_record_contract.md
- docs/architecture/formula_to_corpus_mapping_blueprint.md
- docs/fixtures/value_proof_preregistration_template.md

## 9. Final decision

This contract may be used for planning and future schema design.

It does not implement LearnableCritic runtime behavior.
