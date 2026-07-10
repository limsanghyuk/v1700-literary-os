# Macro Planner Hard-Rule Gate and Candidate Evaluation v2 Report

Date: 2026-07-03  
Status: Stage243 design artifact  
Scope: Macro Planner Candidate Evaluation v2 / hard-rule gate / scorecard / final verdict

## 0. Executive Summary

This work adds the v2 evaluation layer for Macro Planner Candidate fixtures.

The purpose is to prevent a high weighted score from hiding structural failure.

The central rule is:

```text
Hard-rule gate precedes weighted score.
A critical structural failure disqualifies the candidate even if the weighted score is high.
```

This work does not promote Macro Planner, Full Author, or Live Generation readiness.

```text
Macro Planner Promotion = BLOCKED
Full Author Promotion = BLOCKED
Live Generation Readiness = BLOCKED
```

## 1. Work Method

Following `chatgpt_codex_work_division_protocol.md`, this task was split as follows:

### A. ChatGPT-direct work

Performed directly by ChatGPT:

```text
hard-rule gate design
disqualification rule design
candidate scorecard schema design
final verdict fixture design
evaluation v2 report generation
remote GitHub hub loading
remote fetch verification
```

### B. Codex-local work

Not required for this step.

Reason:

```text
The task is schema, gate, and evaluation-contract design.
It does not require local DB scanning, local JSON parsing, local archive inspection, or local git status.
```

### C. Hub load / verification work

Artifacts were loaded to remote GitHub branch:

```text
limsanghyuk/v1700-literary-os
branch: corpus-absorption-formula-bridge-handoff
```

## 2. Input Authority Used

This design uses the local/remote authority split from `local_remote_seqcard_v4_reconciliation_20260703.md`.

### Local cleaned v4 authority

Used for implementation planning:

```text
seqcard_jsonl_files: 577
episode_meta_files: 577
seqcard_records: 37,166
linkage_v4 exact_episode: 456
linkage_v4 unmatched: 120
schema_registry: 2.1-stage243-v4
```

### Remote source snapshot authority

Used for source ZIP audit:

```text
seqcard_records: 37,800
source: uploaded ZIP aggregate manifest
```

Decision:

```text
Use local cleaned v4 values for implementation planning.
Keep remote source manifest as source snapshot audit.
Do not overwrite the remote source manifest with local cleaned values until cleaned files are pushed and verified remotely.
```

## 3. Created Artifacts

```text
release/current/season_wiring_pack/macro_planner_hard_rule_gate.json
release/current/season_wiring_pack/macro_planner_disqualification_rules.json
release/current/season_wiring_pack/macro_candidate_scorecard_schema.json
release/current/season_wiring_pack/macro_candidate_final_verdict_fixture.json
release/current/season_wiring_pack/macro_planner_evaluation_v2_report.md
release/current/transition_council_pack/chatgpt_direct_work_result_packet_macro_hard_rule_v2_20260703.json
```

## 4. Hard-Rule Gate Design

The hard-rule gate defines five rule groups:

```text
1. safety_boundary
2. season_structure
3. causality_and_payoff
4. character_and_relationship_arc
5. scene_function_coverage
```

The gate policy is:

```text
weighted_score_is_secondary: true
hard_rule_precedes_weighted_score: true
single_critical_failure_disqualifies: true
multiple_major_failures_disqualify: true
minor_failures_can_create_warning_only: true
```

Final verdict precedence:

```text
1. safety_failure
2. critical_hard_rule_failure
3. major_hard_rule_failure_cluster
4. weighted_score_threshold
5. warning_review
```

## 5. Disqualification Rule Design

Rules are classified by severity:

```text
safety: always disqualifies
critical: one occurrence disqualifies
major: one may require review, two or more disqualify
minor: warning or review signal
```

Examples of critical/safety failures:

```text
raw_text_leakage
provider_call_detected
runtime_generation_detected
promotion_claim_detected
missing_season_goal
midpoint_missing
crisis_missing
climax_missing
impossible_episode_order
causality_contradiction
payoff_without_plant
character_arc_discontinuity
```

Examples of major failures:

```text
orphan_plant_without_payoff
unmotivated_reversal
relationship_arc_discontinuity
episode_hook_absent_over_threshold
```

Examples of minor warnings:

```text
scene_function_distribution_collapse
core_core2_pair_incoherence
redundant_scene_cluster
```

## 6. Scorecard Schema

The scorecard schema requires:

```text
candidate_id
candidate_kind
input_authority
safety
hard_rule_evaluation
weighted_metric_evaluation
final_verdict
```

Weighted score dimensions:

```text
season_goal_clarity
episode_arc_coherence
scene_grid_necessity
causal_spine_integrity
plant_payoff_integrity
character_arc_continuity
relationship_arc_continuity
conflict_escalation
hook_sequence_quality
genre_rhythm_balance
```

The scorecard pass is not promotion. It may only support Gate A review.

## 7. Final Verdict Fixture

Two examples are included:

### 7.1 Negative control high-score failure

A candidate with weighted score `0.84` fails because it has a critical hard-rule failure:

```text
payoff_without_plant
```

Verdict:

```text
fail_hard_rule
```

Interpretation:

```text
Weighted score must be ignored when a critical hard rule fails.
```

### 7.2 Heldout pass with warning

A candidate passes hard-rule gate and weighted threshold but has a minor warning:

```text
scene_function_distribution_collapse
```

Verdict:

```text
pass_with_warning
```

Interpretation:

```text
Can be used for Gate A review input only.
Do not declare Macro Planner Promotion.
```

## 8. Promotion Interpretation

This work strengthens Macro Planner Candidate evaluation but does not create promotion evidence by itself.

```text
Fixture creation is not promotion.
Preflight pass is not promotion.
Scorecard pass is not promotion.
Gate A review is not Macro Planner Promotion.
```

Current state remains:

```text
Macro Planner Promotion = BLOCKED
Full Author Promotion = BLOCKED
Live Generation Readiness = BLOCKED
```

## 9. Safety State

The following remain false or blocked:

```text
provider_call_count: 0
runtime_generation: false
raw_text_exported: false
raw_vectors_exported: false
draft_text_exported: false
token_exported: false
adapter_weight_exported: false
promotion_claim: false
Macro Planner Promotion: blocked
Full Author Promotion: blocked
Live Generation Readiness: blocked
```

## 10. Result

The next Macro Planner Candidate evaluation must use the v2 process:

```text
1. Validate safety boundary.
2. Apply hard-rule gate.
3. If hard-rule passes, apply weighted score.
4. Compute final verdict.
5. Interpret result only as candidate/gate evidence, not promotion.
```

## 11. Next Required Step

The next engineering task is:

```text
Stage243 Macro Planner Candidate Gate A Review Packet
```

It should assemble candidate fixtures, hard-rule results, scorecards, final verdicts, and reviewer-facing summary into a Gate A review packet.

This next task can be started by ChatGPT if it is design/schema/report work. Codex is only required if local fixture files must be parsed or scanned.
