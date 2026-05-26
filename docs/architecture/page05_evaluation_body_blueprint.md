# Page05 Blueprint — Evaluation Body

## 1. Architecture

```text
V1700 Page05 Evaluation Body
├── Stage167 Evaluation Contract
├── Stage168 Local Evaluation Packet Store
├── Stage169 Deterministic Quality and Continuity Evaluator
├── Stage170 Regression and Negative Fixture Harness
├── Stage171 Evaluation Boundary and Leakage Preflight
└── Stage172 Page05 Release Seal
```

Page05 receives sealed Page04 render evidence and compiles it into deterministic evaluation evidence. It is not a generator, not a publisher, and not a repair executor.

## 2. Proposed repository layout

```text
docs/proposals/page05_evaluation_body_proposal.md
docs/architecture/page05_evaluation_body_blueprint.md
docs/development/page05_developer_handoff.md
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
release/current/stage167_*.json
...
release/current/stage172_*.json
```

## 3. Core contracts

### EvaluationArtifactEnvelope

```json
{
  "artifact_id": "eval_artifact_001",
  "project_id": "project_alpha",
  "source_stage": "stage166",
  "source_artifact_ref": "release/current/stage166_page04_release_seal_report.json",
  "artifact_type": "surface_draft|render_plan|render_packet|quality_preflight",
  "visibility": "surface|internal|hidden",
  "checksum": "sha256:...",
  "created_from": "sealed_page04_artifact",
  "provider_calls": 0,
  "write_policy": "read_only"
}
```

### EvaluationRubric

```json
{
  "rubric_id": "page05_default_surface_rubric",
  "rubric_version": "1.0",
  "quality_threshold": 0.80,
  "regression_delta_threshold": 0.05,
  "continuity_hard_fail_allowed": 0,
  "boundary_violation_allowed": 0,
  "metrics": [
    {"metric_id": "surface_structure_score", "weight": 0.20, "range": [0.0, 1.0]},
    {"metric_id": "scene_continuity_score", "weight": 0.20, "range": [0.0, 1.0]},
    {"metric_id": "character_consistency_score", "weight": 0.20, "range": [0.0, 1.0]},
    {"metric_id": "world_consistency_score", "weight": 0.15, "range": [0.0, 1.0]},
    {"metric_id": "payoff_alignment_score", "weight": 0.15, "range": [0.0, 1.0]},
    {"metric_id": "node2_surface_safety_score", "weight": 0.10, "range": [0.0, 1.0]}
  ]
}
```

### EvaluationVerdict

```json
{
  "verdict_id": "verdict_001",
  "evaluation_packet_id": "packet_001",
  "quality_score": 0.0,
  "continuity_violation_index": 0,
  "regression_delta_index": 0.0,
  "boundary_violation_count": 0,
  "deterministic_checksum": "sha256:...",
  "status": "PASS|BLOCK",
  "block_reasons": []
}
```

## 4. Deterministic algorithms

### Metric normalization

```text
normalize(value, min, max) = clamp((value - min) / (max - min), 0.0, 1.0)
```

### Quality score

```text
quality_score = Σ(normalized_metric_i × rubric_weight_i)
```

Validation:

```text
Σ(rubric_weight_i) == 1.0
0.0 <= normalized_metric_i <= 1.0
```

### Continuity violation index

```text
continuity_violation_index = hard_violation_count + Σ(soft_violation_weight_i)
```

Hard block:

```text
if hard_violation_count > 0:
    status = BLOCK
```

### Regression delta index

```text
regression_delta_index = Σ(abs(current_metric_i - baseline_metric_i) × drift_weight_i)
```

Hard block:

```text
if regression_delta_index > regression_delta_threshold:
    status = BLOCK
```

### Boundary override

```text
if boundary_violation_count > 0:
    status = BLOCK
```

Boundary override must run after score calculation and before verdict finalization so no aggregate score can mask leakage.

## 5. Stage evidence

### Stage167

```text
contract_schema_valid = true
rubric_weights_valid = true
provider_evaluation_enabled = false
boundary_override_defined = true
stage168_packet_store_ready = true
```

### Stage168

```text
packet_store_read_only = true
packet_ids_unique = true
stage166_refs_resolvable = true
load_order_deterministic = true
stage169_evaluator_ready = true
```

### Stage169

```text
quality_channel_pass = true
continuity_channel_pass = true
deterministic_checksum_stable = true
provider_default_calls = 0
stage170_regression_harness_ready = true
```

### Stage170

```text
safe_fixture_pass = true
negative_fixture_blocks = true
raw_reveal_leak_fixture_blocks = true
provider_call_fixture_blocks = true
mutation_command_fixture_blocks = true
regression_snapshot_stable = true
stage171_boundary_preflight_ready = true
```

### Stage171

```text
provider_default_calls = 0
node2_raw_reveal_access = 0
evaluation_write_enabled = false
memory_write_enabled = false
canon_mutation_enabled = false
runtime_training_enabled = false
auto_repair_apply_enabled = false
stage172_release_seal_ready = true
```

### Stage172

```text
page05_stage_chain_pass = true
page05_artifact_index_complete = true
page05_invariant_freeze_pass = true
page05_regression_snapshot_pass = true
page05_boundary_freeze_pass = true
stage173_governance_contract_ready = true
```

## 6. Gate order

```text
Stage166 release gate
→ Stage167 evaluation contract gate
→ Stage168 packet store gate
→ Stage169 evaluator gate
→ Stage170 regression harness gate
→ Stage171 boundary preflight gate
→ Stage172 Page05 release seal gate
```

Each gate must fail closed when required upstream reports are missing, stale, malformed, or failed.

## 7. Test matrix

| Test class | Required behavior |
|---|---|
| contract serialization | valid objects serialize and invalid objects block |
| rubric validation | weights must equal 1.0 per group |
| score determinism | same input returns same checksum |
| quality block | low quality fixture blocks |
| continuity block | hard continuity break blocks |
| regression block | unexpected metric drift blocks |
| boundary block | raw reveal, provider call, mutation command block |
| stale evidence block | stale Stage166 evidence blocks |
| release seal block | missing Stage167~171 report blocks |

## 8. Page05 exit criteria

```text
all Stage167~171 gates pass
provider_default_calls == 0
node2_raw_reveal_access == 0
boundary_violation_count == 0
runtime_training_enabled == false
memory_write_enabled == false
canon_mutation_enabled == false
auto_repair_apply_enabled == false
stage173_governance_contract_ready == true
```
