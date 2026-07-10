# Codex Local P8.2 Deeper Integrity Handoff

Date: 2026-07-05  
Status: local execution handoff prepared  
Scope: P8.2 / 11 deeper integrity checks / hard-rule gate rerun/fix

## 0. Purpose

P8.1 rerun now passes parse, schema, reference-presence, and boundary checks, but remains `pass_with_warning` because 11 deeper integrity checks are still `not_run`.

This handoff tells Codex-local what must be executed next.

## 1. Input Files

Use the current local or remote-authority working tree and inspect these files:

```text
release/current/season_wiring_pack/full_season_candidate_package_fixture_v1.json
release/current/season_wiring_pack/full_season_validation_result_p8_1.json
release/current/season_wiring_pack/full_season_hard_rule_gate_rerun_p8_2.json
release/current/data_foundry_pack/seqcard_snapshot_v5_manifest.json
release/current/data_foundry_pack/episode_arc_inventory_v5.json
release/current/data_foundry_pack/sequence_blueprint_inventory_v5.json
release/current/data_foundry_pack/seqcard_v5_p8_1_schema_mapping.json
release/current/data_foundry_pack/schema_registry.json
release/current/measured_learning_pack/promotion_evidence_registry.json
```

If any required input is missing, write a blocked result and do not continue to P9.

## 2. Required Checks

Execute or implement these 11 checks:

```text
1. series_to_season_integrity
2. season_to_episode_integrity
3. episode_to_sequence_integrity
4. sequence_to_scene_integrity
5. scene_to_renderer_packet_integrity
6. plant_payoff_integrity
7. character_arc_integrity
8. relationship_arc_integrity
9. causal_spine_integrity
10. hook_chain_integrity
11. genre_rhythm_integrity
```

Each check must produce one of:

```text
pass
pass_with_warning
manual_review_required
fail_hard_rule
blocked
```

## 3. Minimal Execution Logic

### 3.1 series_to_season_integrity

Verify:

```text
series_id consistency
season_id consistency
target_episode_count consistency
season goal reference consistency
central conflict axis consistency
entry/exit state presence
```

### 3.2 season_to_episode_integrity

Verify:

```text
EpisodeArcChain coverage of target episode count
episode order continuity
entry/exit state continuity
midpoint/crisis/climax/resolution reference presence where expected
ending hook or transition support
```

### 3.3 episode_to_sequence_integrity

Verify:

```text
episode nodes have sequence targets or sequence count evidence
v5 EpisodeArc sequence_count is usable as support metadata
missing or impossible sequence count cases are reported
```

### 3.4 sequence_to_scene_integrity

Verify:

```text
sequence scene spans are coherent
member_scene_nos are in valid order when available
scene counts are compatible with sequence budgets
no required sequence transition is unsupported by scene evidence
```

### 3.5 scene_to_renderer_packet_integrity

Verify:

```text
scene blueprint references have renderer packet references
renderer packet counts are compatible with scene blueprint counts
renderer packets do not claim authority over long-range structure
```

### 3.6 plant_payoff_integrity

Verify metadata-level evidence for:

```text
orphan plant risk
payoff without plant risk
impossible timing risk
unresolved critical setup risk
```

If the fixture lacks enough plant/payoff details, mark `manual_review_required`, not pass.

### 3.7 character_arc_integrity

Verify metadata-level evidence for:

```text
character state change support
belief/motivation transition support
agency collapse risk
unsupported reversal risk
```

If the fixture lacks enough character detail, mark `manual_review_required`, not pass.

### 3.8 relationship_arc_integrity

Verify metadata-level evidence for:

```text
relationship state change support
relationship reversal cause
status change consistency
unmotivated rupture or reconciliation risk
```

### 3.9 causal_spine_integrity

Verify metadata-level evidence for:

```text
causal dependency continuity
missing cause risk
unsupported effect risk
unmotivated reversal risk
stakes regression risk
```

### 3.10 hook_chain_integrity

Verify metadata-level evidence for:

```text
hook to downstream consequence linkage
isolated cliffhanger risk
episode-end hook coverage
sequence-end transition support
```

### 3.11 genre_rhythm_integrity

Verify metadata-level evidence for:

```text
scene function distribution balance
sequence rhythm variation
conflict/peril/revelation/hook distribution compatibility
genre mode consistency
monotony risk
```

## 4. Required Output Files

Create:

```text
release/current/season_wiring_pack/full_season_deeper_integrity_result_p8_2.json
release/current/season_wiring_pack/full_season_hard_rule_self_check_v2.json
release/current/transition_council_pack/p8_2_local_deeper_integrity_execution_report_20260705.md
```

## 5. Required Result Schema

`full_season_deeper_integrity_result_p8_2.json` should include:

```text
document_type
version
created_at
source_validation_result
source_p8_2_contract
input_files_present
check_results
pass_count
pass_with_warning_count
manual_review_required_count
fail_hard_rule_count
blocked_count
overall_deeper_integrity_status
hard_rule_recommendation
gate_a_recommendation
scorecard_preflight_recommendation
```

`full_season_hard_rule_self_check_v2.json` should include:

```text
document_type
version
source_p8_1_result
source_deeper_integrity_result
hard_rule_pass
final_verdict
gate_a_ready
scorecard_preflight_allowed
blocking_findings
warning_findings
required_next_actions
promotion_status
```

## 6. Decision Rules

Use these rules:

```text
Any blocked check -> hard_rule_pass false
Any fail_hard_rule check -> hard_rule_pass false
Any manual_review_required check -> hard_rule_pass false unless explicitly waived by human review
Only pass/pass_with_warning checks and no blocking findings -> hard_rule_pass may become true
P9 may be considered only if hard_rule_pass true and gate_a_ready true
```

## 7. Boundary

Do not perform:

```text
provider call
live prose generation
canonical mutation
training update
adapter promotion
promotion claim
P9 Scorecard Preflight
```

## 8. Push Requirement

After local execution, push the generated result files to the remote authority branch:

```text
repo: https://github.com/limsanghyuk/v1700-literary-os.git
branch: corpus-absorption-formula-bridge-handoff
```

Report the commit SHA.
