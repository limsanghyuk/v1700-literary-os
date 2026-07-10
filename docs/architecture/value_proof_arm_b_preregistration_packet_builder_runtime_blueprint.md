# Value Proof Arm B Preregistration Packet Builder Runtime Blueprint

Status: implementation blueprint  
Created: 2026-06-16  
Scope: preregistration packet scaffold for Arm B guidance

## Purpose

This blueprint defines the consumer after `value_proof_arm_b_guidance_surface`.

Its purpose is to freeze Arm A and Arm B prompt packet metadata, hashes, allowed context, forbidden context, and threshold placeholders before any Value Proof experiment begins.

It does not start Page18 and does not run an experiment.

## Inputs

```text
release/current/value_proof_arm_b_guidance_pack/value_proof_arm_b_guidance_surface_report.json
```

Fallback input:

```text
release/current/writer_ide_advisory_pack/writer_ide_advisory_consumer_report.json
```

## Output pack

```text
release/current/value_proof_arm_b_preregistration_pack/
  arm_a_prompt_packet.json
  arm_b_prompt_packet.json
  arm_config_registry.json
  value_proof_preregistration_lock_record.json
  value_proof_arm_b_preregistration_validation_report.json
  value_proof_arm_b_preregistration_packet_report.json
```

## Runtime model

```text
Arm B guidance surface report
-> Arm A baseline prompt packet metadata
-> Arm B structured guidance packet metadata
-> stable packet hashes
-> arm config registry
-> preregistration lock record
-> validation report
```

## Arm A rule

Arm A is pure LLM baseline metadata only.

Allowed:

```text
base_task_brief
target_length
genre_hint
```

Forbidden:

```text
formula_signal_refs
writer_ide_surface_cards
learnable_critic_explanation
raw_script_text
```

## Arm B rule

Arm B can include preregistered V1700 guidance only.

Allowed context is copied from the guidance board. Forbidden context remains locked.

## Boundary

```text
provider_default_calls = 0
runtime_training_enabled = false
canonical_mutation_allowed = false
page18_runtime_opened = false
experiment_started = false
```

## Blocking failures

- guidance surface is not pass
- prompt packet hash is missing
- Arm A and Arm B packet hashes are identical
- Arm B permits raw script text
- Arm B permits provider generation
- experiment is already started
- Page18 runtime is opened

## Local execution

Because this web session cannot run the local repository test suite, local Codex must execute the package and test after this scaffold.

Suggested local command:

```powershell
python -m pytest tests/test_value_proof_arm_b_preregistration_packet_builder.py -q
```

## Next integration target

```text
Value Proof blind evaluator packet builder
```

This next step should still not run Page18. It should only prepare blind packet metadata and evaluator-facing packet boundaries.
