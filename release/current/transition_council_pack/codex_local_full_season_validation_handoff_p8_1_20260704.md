# Codex Local Full-Season Validation Handoff P8.1

Date: 2026-07-04  
Status: local execution handoff prepared  
Scope: JSON/schema validation and cross-level integrity execution

## 0. Purpose

This handoff defines the local Codex validation work required after P8 hard-rule self-check.

The remote hub now contains the validation protocol:

```text
release/current/season_wiring_pack/full_season_validation_protocol_p8_1.json
```

Remote ChatGPT authored the protocol. Local Codex should execute validation against the local repository checkout.

## 1. Required Input Files

Use these files from the repository checkout:

```text
release/current/season_wiring_pack/full_season_candidate_package_fixture_v1.json
release/current/season_wiring_pack/full_season_candidate_package_schema_v1.json
release/current/season_wiring_pack/full_season_hard_rule_self_check_v1.json
release/current/season_wiring_pack/full_season_validation_protocol_p8_1.json
```

## 2. Required Local Checks

Run the checks in this order:

```text
1. JSON parse validation
2. Schema validation
3. Cross-level integrity execution
4. Boundary invariant check
5. Validation result packet creation
```

## 3. Expected Output File

Create:

```text
release/current/season_wiring_pack/full_season_validation_result_p8_1.json
```

## 4. Required Result Fields

The result file should include:

```text
json_parse_pass
schema_validation_pass
cross_level_integrity_pass
boundary_invariants_pass
overall_validation_status
gate_a_ready_after_validation
scorecard_preflight_allowed
required_next_actions
```

## 5. Decision Rules

Use this decision order:

```text
JSON parse failure -> fail_validation
Schema validation failure -> fail_validation
Blocking cross-level finding -> manual_review_required or fail_validation
Boundary invariant failure -> blocked
All required checks pass -> pass or pass_with_warning
```

Scorecard preflight is allowed only if validation status permits and hard-rule status permits.

## 6. Current Expected State

Before local execution, the expected state is:

```text
validation_executed: false
gate_a_ready: false
scorecard_preflight_allowed: false
```

Do not mark Gate A ready without completed validation evidence.

## 7. Commit Requirement

After local validation, commit and push:

```text
release/current/season_wiring_pack/full_season_validation_result_p8_1.json
```

Then update the transition council packet with the validation result summary.

## 8. Boundary

No provider call, live prose generation, canonical mutation, training update, or promotion claim is allowed during this validation task.

## 9. Final Instruction

Execute local validation only. Do not promote Macro Planner, Full Author, or live generation readiness from this step.
