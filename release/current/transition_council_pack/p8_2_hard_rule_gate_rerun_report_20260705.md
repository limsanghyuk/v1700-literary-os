# P8.2 Hard-Rule Gate Rerun / Fix Report

Date: 2026-07-05  
Status: P8.2 design-authority rerun contract loaded to remote hub  
Scope: Stage243 / hard-rule gate / P8.1 pass_with_warning / Gate A blocking state

## 0. Executive Summary

P8.1 has now been rerun after the four missing full-season input files were synchronized from the remote authority branch into the local hub.

The previous blocker was:

```text
blocked_missing_required_inputs
```

That blocker is now resolved.

Current P8.1 state:

```text
json_parse_pass: true
schema_validation_pass: true
schema_error_count: 0
cross_level_integrity_pass: true
integrity_error_count: 0
integrity_warning_count: 11
boundary_invariants_pass: true
overall_validation_status: pass_with_warning
hard_rule_pass_from_self_check: false
gate_a_ready_after_validation: false
scorecard_preflight_allowed: false
```

Therefore P8.2 does not authorize P9.

P8.2 classifies the current state as:

```text
hard_rule_pass: false
final_verdict: manual_review_required
Gate A: blocked
P9 Scorecard Preflight: blocked
```

## 1. Created Artifact

Created:

```text
release/current/season_wiring_pack/full_season_hard_rule_gate_rerun_p8_2.json
```

Purpose:

```text
Define the correct hard-rule rerun/fix decision after P8.1 pass_with_warning.
Separate reference-level validation pass from deeper instantiated narrative-integrity execution.
Prevent premature scorecard execution.
```

## 2. Reasoning

P8.1 proves that these checks now pass:

```text
JSON parse
schema validation
reference presence checks
boundary invariants
```

However, P8.1 does not prove that the deeper instantiated narrative checks have been executed.

The following checks remain not_run:

```text
series_to_season_integrity
season_to_episode_integrity
episode_to_sequence_integrity
sequence_to_scene_integrity
scene_to_renderer_packet_integrity
plant_payoff_integrity
character_arc_integrity
relationship_arc_integrity
causal_spine_integrity
hook_chain_integrity
genre_rhythm_integrity
```

Therefore these warnings cannot be silently converted into hard-rule pass.

## 3. P8.2 Decision

The P8.2 decision is:

```text
Do not run P9.
Do not mark Gate A ready.
Do not claim Macro Planner Promotion.
Do not claim Full Author Promotion.
Do not claim Live Generation Readiness.
```

Required next step:

```text
Run or implement the 11 deeper integrity checks locally.
Then produce a P8.2 deeper integrity result.
Then create or update hard-rule self-check v2.
Then rerun P8.1 validation.
```

## 4. Why Codex-Local Is Required

ChatGPT can define the P8.2 contract and decision policy.

Codex-local is required for actual execution because the checks must inspect local metadata artifacts and inventories, including:

```text
full_season_candidate_package_fixture_v1.json
full_season_validation_result_p8_1.json
seqcard_snapshot_v5_manifest.json
episode_arc_inventory_v5.json
sequence_blueprint_inventory_v5.json
seqcard_v5_p8_1_schema_mapping.json
```

## 5. Required Local Outputs

Codex-local should produce:

```text
release/current/season_wiring_pack/full_season_deeper_integrity_result_p8_2.json
release/current/season_wiring_pack/full_season_hard_rule_self_check_v2.json
release/current/transition_council_pack/p8_2_local_deeper_integrity_execution_report_20260705.md
```

If the local result still contains manual_review_required or failed hard rules, P9 remains blocked.

## 6. Boundary

P8.2 must not perform:

```text
provider call
live prose generation
canonical mutation
training update
adapter promotion
promotion claim
P9 Scorecard Preflight
```

## 7. Final Decision

P8.2 remote design-authority rerun contract is complete.

Current official state:

```text
P8.1: pass_with_warning
P8.2: manual_review_required
Gate A: blocked
P9: blocked
Promotion: blocked
```
