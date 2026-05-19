# V1700 Stage135 Blueprint — LearningQualityGate & Candidate Registry

## 1. Baseline

Stage135 is built on Stage134 — MetaLearner Audit Mode.

## 2. Goal

Stage135 adds a deterministic LearningQualityGate that converts Stage134 audit output into a candidate registry without permitting runtime learning or model updates.

## 3. Non-goals

- No runtime training.
- No active learning.
- No model weight updates.
- No AutoRepair mutation.
- No canon auto-resolution.
- No LOSDB write path yet.

## 4. Package Structure

```text
src/v1700/learning_quality_gate/
  contracts.py
  gate.py
  preflight.py
  report.py

src/v1700/stage135/
  stage135_runner.py

src/v1700/gates/stage135_release_gate.py

tools/run_stage135_learning_quality_gate.py
tools/run_stage135_release_gate.py

tests/test_stage135_learning_quality_gate.py
```

## 5. Candidate Decisions

```text
ACCEPT_CANDIDATE
REJECT_CANDIDATE
REVIEW_ONLY
```

Review-required cases are never converted into training examples. They are recorded as review-only candidates.

## 6. Release Gate

The release gate validates Stage134 baseline, candidate-only mode, zero learning, zero training trigger, zero mutation, provider-zero, Node2 boundary, raw manuscript leakage zero, and documentation/manifest evidence.
