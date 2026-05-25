# Page05 Proposal — Evaluation Body

## 1. Purpose

Page05 converts sealed Page04 rendering evidence into deterministic evaluation evidence. It evaluates rendered or dry-run surface artifacts against quality, continuity, regression, determinism, and boundary criteria without enabling live provider generation, write paths, runtime training, publication, or automatic repair.

## 2. Baseline

Page05 starts only after Stage166 Page04 Release Seal passes. Required inputs are Stage161 through Stage166 reports and release gates, especially the Stage166 Page04 release seal, invariant freeze, artifact index, regression snapshot, and Stage167 transition criteria.

## 3. Mission

```text
sealed render artifacts
→ evaluation contracts
→ local evaluation packets
→ deterministic quality and continuity evaluation
→ regression and negative fixture verification
→ leakage and boundary preflight
→ Page05 release seal
```

Page05 does not decide publication. It decides whether rendered artifacts are evaluation-ready, regression-safe, boundary-safe, and sufficiently scored for governance review in Page06.

## 4. Stage range

```text
Stage167 — Evaluation Contract
Stage168 — Local Evaluation Packet Store
Stage169 — Deterministic Quality and Continuity Evaluator
Stage170 — Regression and Negative Fixture Harness
Stage171 — Evaluation Boundary and Leakage Preflight
Stage172 — Page05 Release Seal
```

## 5. Non-goals

- No live LLM judge by default
- No provider generation
- No final publication workflow
- No manuscript mutation
- No memory write
- No canon mutation
- No runtime training
- No automatic repair apply
- No cross-project evaluation writeback

## 6. Required evaluation channels

| Channel | Purpose | Blocking condition |
|---|---|---|
| Quality | Surface quality, structure, readability, scene coherence | score below threshold |
| Continuity | Character, world, event, reveal, payoff consistency | hard continuity violation |
| Regression | Change from frozen previous evidence | unexpected regression drift |
| Boundary | Node2 raw reveal, hidden memory, private notes, provider leakage | any violation |
| Determinism | Stable output from same input | checksum mismatch |
| Evidence completeness | Required input reports and fixture outcomes | missing or stale evidence |

A high quality score must never override a boundary violation.

## 7. Stage proposals

### Stage167 — Evaluation Contract

Goal: define typed contracts for evaluation inputs, rubrics, metrics, verdicts, thresholds, and boundary rules.

Required objects:

```text
EvaluationArtifactEnvelope
EvaluationSubject
EvaluationRubric
EvaluationMetric
EvaluationThresholdPolicy
QualityCriterion
ContinuityCriterion
RegressionCriterion
BoundaryCriterion
EvaluationVerdict
EvaluationEvidenceRef
EvaluationAuthorityPolicy
```

Acceptance criteria:

- contracts serialize to JSON
- invalid metric weights block deterministically
- required thresholds are explicit
- provider evaluation is disabled by default
- boundary criteria are non-overridable

### Stage168 — Local Evaluation Packet Store

Goal: store evaluation subjects and packetized evidence locally in read-only mode.

Required components:

```text
JsonEvaluationPacketStore
EvaluationPacketIndex
EvaluationPacketLoadResult
EvaluationPacketDuplicateDetector
EvaluationPacketReadOnlyGuard
EvaluationSubjectResolver
Stage166EvidenceResolver
```

Acceptance criteria:

- evaluation packets are loaded deterministically
- packet IDs are unique
- stage references resolve to existing sealed evidence
- store write attempts are blocked
- corrupted packets produce explainable errors

### Stage169 — Deterministic Quality and Continuity Evaluator

Goal: evaluate quality and continuity with deterministic local metrics.

Metric families:

```text
surface_structure_score
scene_continuity_score
character_consistency_score
world_consistency_score
reveal_safety_score
payoff_alignment_score
render_packet_adherence_score
node2_surface_safety_score
```

Acceptance criteria:

- the same packet produces the same score and checksum
- all weights sum to 1.0 per rubric group
- boundary violation forces BLOCK regardless of score
- continuity hard fail cannot be hidden by aggregate quality

### Stage170 — Regression and Negative Fixture Harness

Goal: prove that evaluation catches regressions and known bad cases.

Required fixture classes:

```text
quality_drop_fixture
continuity_break_fixture
raw_reveal_leak_fixture
hidden_memory_projection_fixture
provider_call_fixture
mutation_command_fixture
stale_stage166_evidence_fixture
checksum_drift_fixture
```

Acceptance criteria:

- safe fixture passes
- each negative fixture blocks for the expected reason
- regression snapshot is deterministic
- fixture coverage is recorded in release evidence

### Stage171 — Evaluation Boundary and Leakage Preflight

Goal: verify that evaluation itself does not leak privileged data or enable forbidden actions.

Checks:

```text
provider_default_calls == 0
node2_raw_reveal_access == 0
evaluation_write_enabled == false
memory_write_enabled == false
canon_mutation_enabled == false
runtime_training_enabled == false
auto_repair_apply_enabled == false
cross_project_write_enabled == false
```

Acceptance criteria:

- no boundary violation is allowed
- all boundary scans are machine-readable
- Node2 projected evaluation reports contain surface-only references
- hidden reveal payloads are blocked

### Stage172 — Page05 Release Seal

Goal: aggregate Stage167 through Stage171 into a Page05 release seal and emit Stage173 entry criteria.

Gate inputs:

```text
Stage166 Page04 release seal report
Stage167 evaluation contract report
Stage168 evaluation packet store report
Stage169 deterministic evaluator report
Stage170 regression harness report
Stage171 boundary preflight report
```

Pass criteria:

```text
all reports pass
quality_channel_pass == true
continuity_channel_pass == true
regression_channel_pass == true
boundary_channel_pass == true
determinism_channel_pass == true
page05_evaluation_body_sealed == true
stage173_governance_contract_ready == true
```

## 8. Deterministic scoring policy

Recommended score shape:

```text
quality_score = Σ(metric_i.normalized_value × metric_i.weight)
continuity_violation_index = count(hard_violations) + weighted_soft_violation_sum
regression_delta_index = Σ(abs(current_metric_i - baseline_metric_i) × drift_weight_i)
boundary_violation_count = count(boundary_blocks)
```

Pass rule:

```text
PASS only if
quality_score >= threshold
AND continuity_violation_index == 0
AND regression_delta_index <= allowed_delta
AND boundary_violation_count == 0
AND provider_default_calls == 0
```

## 9. Deliverables

```text
docs/proposals/stage167_evaluation_contract_proposal.md
...
docs/proposals/stage172_page05_release_seal_proposal.md
docs/architecture/stage167_evaluation_contract_blueprint.md
...
docs/architecture/stage172_page05_release_seal_blueprint.md
src/v1700/evaluation_body_contract/
src/v1700/evaluation_packet_store/
src/v1700/evaluation_engine/
src/v1700/evaluation_regression/
src/v1700/evaluation_boundary_preflight/
src/v1700/page05_release_seal/
tools/run_stage167_evaluation_contract.py
...
tools/run_stage172_release_gate.py
tests/test_stage167_evaluation_contract.py
...
tests/test_stage172_page05_release_seal.py
```

## 10. Final proposal decision

Page05 should be a deterministic evaluation compiler. It should produce the evidence that Page06 governance will use to decide authority, policy, and release promotion readiness. It must not generate, mutate, publish, train, or repair.
