# P8.1 Local Validation Rerun Report 2026-07-05

## Scope

Codex cloned the remote authority branch, copied the four missing `full_season_*` P8.1 inputs into the local hub, replaced the temporary validator with the protocol-aligned validator, and reran P8.1 local validation.

Remote source:

```text
repo: https://github.com/limsanghyuk/v1700-literary-os.git
branch: corpus-absorption-formula-bridge-handoff
local clone: C:\AI_Codex\codex-work\gpt_remote
remote HEAD: 0105346ff71bc362eb148e75787af41bf7f57d60
```

Local target:

```text
C:\AI_Codex\codex-work\gpt\release\current\season_wiring_pack
```

## Synced Input Files

```text
full_season_candidate_package_fixture_v1.json
full_season_candidate_package_schema_v1.json
full_season_hard_rule_self_check_v1.json
full_season_validation_protocol_p8_1.json
```

Fingerprints:

```text
fixture sha256: 8fb74d834284119f04430e77e8804627131954a8a0ca1ca3e3ff7f8d180ad725
schema sha256: 9778be229aba2820c9d3b5c7d0734bf4dba4822b977f67b57136ec858a7d920f
self_check sha256: 4d91ab5478bae3212138704ec34234a73de322cc4e7bbef087d553fbd83a24c9
protocol sha256: f0332942d5f0c5a41e5237e5b4fc1c7f9b7413e8f4f34d95223fcd132aeb3cd9
```

## Validator

```text
tools/validate_full_season_p8_1.py
```

The validator performs:

```text
JSON parse validation
Draft 2020-12 jsonschema validation
cross-level integrity reference checks
boundary invariant checks
Gate A / Scorecard permission calculation
```

It does not perform:

```text
provider call
live prose generation
canonical mutation
training update
adapter promotion
promotion claim
P9 Scorecard Preflight
```

## Result

Output:

```text
release/current/season_wiring_pack/full_season_validation_result_p8_1.json
```

Summary:

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

Warnings:

```text
series_to_season_integrity: not_run
season_to_episode_integrity: not_run
episode_to_sequence_integrity: not_run
sequence_to_scene_integrity: not_run
scene_to_renderer_packet_integrity: not_run
plant_payoff_integrity: not_run
character_arc_integrity: not_run
relationship_arc_integrity: not_run
causal_spine_integrity: not_run
hook_chain_integrity: not_run
genre_rhythm_integrity: not_run
```

## Interpretation

The prior blocker `blocked_missing_required_inputs` is resolved.

P8.1 now passes JSON parse, schema validation, cross-level reference presence checks, and boundary invariants. It remains `pass_with_warning` because 11 deeper instantiated integrity checks are still marked `not_run`.

Gate A is still not ready because the imported P8 hard-rule self-check reports:

```text
hard_rule_pass_from_self_check: false
```

Therefore:

```text
P9 Scorecard Preflight: blocked
Macro Planner Promotion: blocked
Full Author Promotion: blocked
Live Generation Readiness: blocked
```

## Next Required Step

```text
Rerun or fix the P8 hard-rule gate until hard_rule_pass is true.
Then rerun P8.1 validation.
Only if gate_a_ready_after_validation becomes true may P9 Scorecard Preflight be considered.
```

## Authority Note

The local hub path `C:\AI_Codex\codex-work\gpt` is still not a Git repository. The remote clone at `C:\AI_Codex\codex-work\gpt_remote` is a Git working tree. Local hub results have not been pushed to the remote authority unless separately copied/committed there.
