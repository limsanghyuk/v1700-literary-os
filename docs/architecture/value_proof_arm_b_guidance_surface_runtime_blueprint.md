# Value Proof Arm B Guidance Surface Runtime Blueprint

Status: implementation blueprint  
Created: 2026-06-16  
Scope: advisory-only Value Proof Arm B guidance consumer

## Purpose

This runtime blueprint defines the next consumer after the Writer IDE advisory consumer.

The surface converts writer-visible advisory cards into preregistration-safe Arm B guidance for future Value Proof experiments.

It does not start Page18 and does not run a Value Proof experiment.

## Inputs

- `release/current/writer_ide_advisory_pack/writer_ide_advisory_consumer_report.json`
- `docs/architecture/value_proof_experiment_engine_blueprint.md`
- `docs/templates/value_proof_preregistration_template.md`
- `docs/fixtures/value_proof_minimum_fixture_spec.md`

## Output pack

```text
release/current/value_proof_arm_b_guidance_pack/
  value_proof_arm_b_guidance_cards.json
  value_proof_preregistration_warning.json
  value_proof_arm_b_guidance_board.json
  value_proof_arm_b_guidance_validation_report.json
  value_proof_arm_b_guidance_surface_report.json
```

## Runtime model

```text
writer IDE advisory consumer report
-> focus work selection
-> Arm B allowed guidance projection
-> preregistration boundary warning
-> guidance board
-> validation report
```

## Arm B rule

Arm B may use only preregistered formula guidance.

Allowed:

```text
metadata-only corpus refs
writer IDE advisory surface cards
formula signal refs
learnable critic review-only explanation
```

Forbidden:

```text
raw script text
unregistered prompt mutation
post-output threshold change
canonical mutation
evaluator-visible arm label
```

## Boundary

```text
provider_default_calls = 0
runtime_training_enabled = false
canonical_mutation_allowed = false
advisory_only = true
page18_runtime_opened = false
```

## Promotion blockers

```text
value_proof_preregistration_required
arm_a_b_prompt_hash_required
blind_evaluator_packet_required
approval_boundary_required
```

## Blocking failures

- no guidance cards
- mixed work IDs
- any card permits canonical mutation
- any card lacks preregistration requirement
- board is visible to evaluator
- board allows provider generation
- board allows canonical mutation

## Next integration target

After local Codex validation, the next candidate is:

```text
Value Proof Arm B preregistration packet builder
```

That step should still not start Page18 runtime. It should only prepare prompt packet contracts and hashes.
