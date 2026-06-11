# Formula Measurement Lab Blueprint

Status: PROPOSED_SCAFFOLD
Created: 2026-06-10
Scope: empirical measurement and calibration planning for V1700 formulas

## 1. Purpose

Create a measurement layer that evaluates whether V1700 literary formulas correlate with human review, benchmark outcomes, and regression evidence.

## 2. Non-goals

```text
no runtime training
no active coefficient update
no automatic formula promotion
no Page18 implementation
no Stage243+ creation
```

## 3. Core components

```text
HumanRatingDataset
FormulaSignalExtractor
FormulaHumanCorrelationReport
FalsePositiveFalseNegativeMatrix
FormulaResidualAnalyzer
CoefficientCandidateRegistry
ShadowEvaluationRunner
RegressionRiskReport
HumanApprovalRecord
RollbackPlan
```

## 4. Measurement targets

```text
NarrativeFitnessScore
NarrativeStateTensor8D
EmotionalMomentum
CharacterInteractionMatrix
DRSE / causality transition
RAG retrieval score
Gate26 graph contradiction advisory
```

## 5. Required metrics

```text
human_correlation
calibration_error
false_positive_rate
false_negative_rate
genre_stability
adversarial_robustness
regression_failure_count
explainability_score
```

## 6. Formula update rule

A measured formula may only create a candidate.

```text
current_formula -> measurement_report -> coefficient_candidate -> shadow_eval -> regression_gate -> human_approval -> bounded_update
```

## 7. Candidate record fields

```text
candidate_id
formula_id
current_coefficients
proposed_coefficients
dataset_ref
human_rating_ref
shadow_eval_report_ref
regression_report_ref
expected_gain
known_risk
approval_status
applied
rollback_ref
```

## 8. Acceptance criteria

```text
measurement dataset is frozen
source provenance is recorded
human ratings are separated from formula outputs
candidate update does not mutate active formula
shadow eval passes before approval
regression report has zero blocking failure
human approval is required for active promotion
```

## 9. Next implementation candidate

```text
tools/formula_measurement_lab.py
tests/test_formula_measurement_lab.py
fixtures/formula_measurement/formula_measurement_plan.json
fixtures/formula_measurement/coefficient_candidate_registry.json
```
