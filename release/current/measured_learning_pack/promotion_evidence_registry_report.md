# Promotion Evidence Registry Report

Date: 2026-07-03

## Result

Codex created:

```text
release/current/measured_learning_pack/promotion_evidence_registry.json
```

## Current Status

```text
Stage: Stage243
Live generation readiness: blocked
Macro Planner Promotion: blocked
Full Author Promotion: blocked
Page18 runtime: closed
provider_default_calls: 0
Pass4-Pass7 preflight fixtures: completed
Macro Planner Candidate fixtures: completed contract preflight
Blind Structural Evaluation fixture: completed fixture-only
Multi-candidate Blind Structural Evaluation set: completed fixture-only with threshold warning
```

## Evidence Summary

Structural evidence is partial:

```text
SeqCard v5 records: 41,168
SeqCard v5 files: 648
EpisodeArc v5 files: 648
SequenceBlueprint v5 files: 648
SequenceBlueprint v5 records: 6,146
Series count by filename: 33
Taxonomy-16 present in core/core2: true
Linkage v5 exact_episode: 476
Linkage v5 series_only: 1
Linkage v5 unmatched: 171
```

P8.1 local validation rerun after syncing remote full-season input files:

```text
json_parse_pass: true
schema_validation_pass: true
schema_error_count: 0
cross_level_integrity_pass: true
integrity_warning_count: 11
boundary_invariants_pass: true
overall_validation_status: pass_with_warning
hard_rule_pass_from_self_check: false
gate_a_ready_after_validation: false
scorecard_preflight_allowed: false
```

Craft-axis evidence is measured but narrow:

```text
SP-E.10 Path B v3: 5/5 ADOPT
Final W1: 0.808
Final CI lower: 0.7592
Scope: show-vs-flat-tell craft preference only
```

## Blocked Claims

```text
Macro Planner: blocked
Full Author: blocked
Live Page18 Generation: blocked
Adapter/model promotion from 4070 evidence: blocked
```

## Completed Multi-Candidate Blind Structural Evaluation

```text
blind_structural_evaluation_multicandidate_set.json: created
negative_control_macro_fixtures.json: created
heldout_season_structure_fixtures.json: created
macro_planner_metric_thresholds.json: created
macro_planner_multicandidate_evaluation_report.json/md: created
candidate_count: 6
heldout_pass_rate: 1.0
negative_control_fail_rate: 1.0
promotion_claim: false
threshold_gap_warning: true
```

Warning: negative controls are separated by hard-rule failures. Weighted score alone is not sufficient for Macro Planner promotion.

## Next Codex Work

```text
1. Real held-out metadata-only structure packs
2. Hard-rule vs weighted-score threshold separation
3. Gate B human review protocol
4. Remote authority confirmation if GitHub/remote is chosen as authority
```

## Completed Contract Preflight

```text
Pass4 RetrievalPacket fixture: created
Pass5 DraftPacket fixture-only envelope: created
Pass6 GateResult fixture: created
Pass7 PanelResult fixture: created
Pass4-Pass7 preflight report: created
```

## Completed Macro Candidate Preflight

```text
SeasonArc fixture: created
EpisodeArc fixture: created
SceneGrid fixture: created
Plant/Payoff fixture: created
CharacterArc fixture: created
Macro Planner Candidate preflight report: created
```

## Completed Blind Structural Evaluation Fixture

```text
Scoring rubric: created
Blind evaluation fixture: created
Macro planner evaluation report: created
candidate_count: 1
mean_weighted_score: 1.0
promotion_claim: false
```

No raw text, vectors, tokens, adapter weights, provider calls, runtime training, or canonical mutation were used.
