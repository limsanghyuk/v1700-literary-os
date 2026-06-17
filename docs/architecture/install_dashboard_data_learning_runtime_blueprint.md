# Install, Dashboard, Data, and Measured Learning Runtime Blueprint

Status: candidate architecture blueprint
Created: 2026-06-18
Branch: corpus-absorption-formula-bridge-handoff
Baseline: stage242

## Non-Opening Rule

This blueprint defines candidate productization layers only. It does not open Page18, create Stage243, enable runtime training, or start provider execution.

## Architecture Goal

Add the missing product surfaces needed to turn V1700 from a research-grade literary authority system into an installable, observable, writer-centered literary OS.

## Layer A — Install and Environment Bootstrap

### Responsibilities

```text
install profile selection
dependency validation
secret boundary validation
local corpus path validation
release gate status display
provider adapter policy check
```

### CLI shape

```text
v1700 doctor
v1700 install --profile local
v1700 install --profile dashboard
v1700 verify-secrets
v1700 check-corpus --metadata-only
v1700 run-gates --stage stage242
```

### Runtime profiles

```text
local_research
local_writer_studio
local_codex_execution
team_dashboard
controlled_production_candidate
```

### Output pack

```text
release/current/install_runtime_pack/install_profile.json
release/current/install_runtime_pack/environment_preflight_report.json
release/current/install_runtime_pack/secret_boundary_report.json
release/current/install_runtime_pack/install_validation_report.json
```

## Layer B — Dashboard and UI/UX Console

### Dashboard panels

```text
1 Authority Timeline
2 Release Gate Console
3 Corpus Safety Console
4 Formula Signal Explorer
5 Narrative Graph Viewer
6 Writer Studio Board
7 Value Proof Observatory
8 Approval Boundary Inbox
9 Install Health Panel
10 Learning Candidate Panel
```

### Permission model

```text
writer: advisory cards, drafts, approval decisions
operator: gates, install health, evidence reports
reviewer: blind evaluation assignments
admin: runtime profile and plugin capability policy
```

### Dashboard state sources

```text
release/current/*.json
release/current/*_pack/*.json
docs/development/*.md
docs/architecture/*.md
manifests/*.json
```

### Output pack

```text
release/current/dashboard_pack/dashboard_panel_manifest.json
release/current/dashboard_pack/dashboard_route_manifest.json
release/current/dashboard_pack/dashboard_permission_policy.json
release/current/dashboard_pack/dashboard_validation_report.json
```

## Layer C — Data Construction and Measurement Foundry

### Measurement schema groups

```text
corpus_feature_measurements
formula_signal_measurements
narrative_tensor_measurements
writer_interaction_measurements
generation_output_measurements
blind_evaluation_measurements
release_gate_measurements
```

### Minimum metric definitions

```text
continuity_score
character_arc_consistency
conflict_progression_score
foreshadowing_resolution_score
style_coherence_score
reader_preference_rate
revision_acceptance_rate
approval_latency
boundary_violation_count
```

### Dataset lifecycle

```text
raw local-only source
metadata extraction
feature snapshot
measurement event
quality report
approved dataset manifest
learning candidate record
```

### Output pack

```text
release/current/data_measurement_pack/measurement_event_schema.json
release/current/data_measurement_pack/metric_definition_registry.json
release/current/data_measurement_pack/evaluation_dataset_manifest.json
release/current/data_measurement_pack/data_quality_report.json
release/current/data_measurement_pack/privacy_boundary_report.json
```

## Layer D — Measured Learning Loop

### Allowed learning modes

```text
prompt_policy_improvement
retrieval_ranking_improvement
formula_weight_calibration
rubric_weight_calibration
adapter_experiment_candidate
```

### Forbidden by default

```text
hidden runtime training
automatic production promotion
training on unapproved raw text
writer telemetry without consent
unlogged model improvement
irreversible personalization
```

### Promotion gates

```text
learning candidate manifest exists
approval record exists
rollback record exists
Value Proof result exists
release gate passes
Dashboard shows active policy
```

### Output pack

```text
release/current/measured_learning_pack/learning_candidate_registry.json
release/current/measured_learning_pack/improvement_hypothesis_registry.json
release/current/measured_learning_pack/prompt_policy_change_proposal.json
release/current/measured_learning_pack/learning_effect_report.json
release/current/measured_learning_pack/learning_approval_record.json
```

## Productization Priority

Install and dashboard should not wait until all advanced agents exist. They should be introduced after Page21 because writer-visible product feedback is needed before personalization, plugin expansion, or multi-agent runtime.

## Final Boundary

```text
Page18 remains closed until evidence completion.
Stage243 is not created by this blueprint.
Runtime training remains disabled.
Provider execution remains gated by ProviderExecutionPolicy.
Raw protected text remains local-only.
```
