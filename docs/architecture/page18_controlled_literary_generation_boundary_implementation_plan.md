# Page18 Controlled Literary Generation Boundary Implementation Plan

Status: implementation plan prepared
Created: 2026-06-18
Branch: corpus-absorption-formula-bridge-handoff
Baseline: stage242
Precondition: page18_opening_gate_checklist prepared

## Purpose

This plan defines the first Page18 implementation unit after policy review and opening gate preparation.

It does not open Page18 runtime, does not create Stage243, does not execute provider generation, and does not capture generated prose.

## Implementation Goal

Create a controlled literary generation boundary that freezes the following before any generation execution:

```text
generation request
context packet
narrative constraints
provider execution policy
output capture schema
canonical mutation blocker
validation report
```

## New Package Layout

```text
src/v1700/literary_generation_boundary/
  __init__.py
  contracts.py
  report.py

src/v1700/generation_context_packet/
  __init__.py
  contracts.py
  report.py

src/v1700/output_capture_schema/
  __init__.py
  contracts.py
  report.py

tools/run_page18_generation_boundary_preflight.py

tests/test_page18_generation_boundary.py
```

## Required Records

### LiteraryGenerationRequest

Fields:

```text
request_id
work_id
mode
base_task_brief_ref
target_length_policy
genre_hint
allowed_context_refs
forbidden_context_refs
provider_execution_policy_ref
output_capture_schema_ref
canonical_mutation_blocker_ref
```

### GenerationContextPacket

Fields:

```text
context_packet_id
work_id
metadata_only_corpus_refs
formula_signal_refs
narrative_tensor_refs
writer_advisory_refs
value_proof_packet_refs
raw_script_text_allowed=false
```

### NarrativeConstraintPacket

Fields:

```text
constraint_packet_id
work_id
continuity_constraints
character_arc_constraints
conflict_progression_constraints
foreshadowing_constraints
style_boundary_refs
```

### ProviderExecutionPolicy

Fields:

```text
policy_id
provider_default_calls=0
provider_generation_allowed=false
credentials_externalized=true
secret_logging_allowed=false
requires_explicit_execution_phase=true
```

### OutputCaptureSchema

Fields:

```text
schema_id
output_capture_started=false
capture_allowed=false
capture_path_policy
generated_output_hash_required=true
canonical_mutation_allowed=false
```

### CanonicalMutationBlocker

Fields:

```text
blocker_id
canonical_mutation_allowed=false
requires_approval_decision_record=true
requires_rollback_record=true
blocked_mutation_targets
```

### GenerationBoundaryValidationReport

Fields:

```text
status
issues
provider_default_calls
runtime_training_enabled
canonical_mutation_allowed
page18_runtime_opened
stage243_created
forbidden_context_detected
raw_script_text_allowed
```

## Output Pack

```text
release/current/literary_generation_boundary_pack/generation_boundary_report.json
release/current/literary_generation_boundary_pack/literary_generation_request.json
release/current/literary_generation_boundary_pack/generation_context_packet.json
release/current/literary_generation_boundary_pack/narrative_constraint_packet.json
release/current/literary_generation_boundary_pack/provider_execution_policy.json
release/current/literary_generation_boundary_pack/output_capture_schema.json
release/current/literary_generation_boundary_pack/canonical_mutation_blocker.json
release/current/literary_generation_boundary_pack/page18_generation_boundary_validation_report.json
```

## Test Requirements

```text
request exists and references all boundary records
context packet contains metadata-only refs only
provider_default_calls remains 0
provider_generation_allowed=false
output_capture_started=false
capture_allowed=false
canonical_mutation_allowed=false
page18_runtime_opened=false
stage243_created=false
raw_script_text_allowed=false
forbidden context list blocks raw_script_text and unregistered prompt mutation
```

## Local Command Sequence

```powershell
python tools/run_page18_generation_boundary_preflight.py
python -m pytest tests/test_page18_generation_boundary.py -q
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_stage242_release_gate.py
python tools/run_release_gate.py
```

## Explicit Non-Goals

```text
no provider generation
no generated prose capture
no experiment start
no canonical manuscript mutation
no runtime training
no Stage243 creation
no raw protected corpus text in prompt packets
```

## Promotion Rule

A successful Page18 boundary implementation may promote the project from:

```text
ready_for_policy_review
```

to:

```text
page18_boundary_preflight_pass
```

It must not promote to:

```text
page18_runtime_opened
stage243_created
experiment_started
```

## Next Step After This Plan

Implement the package and preflight runner exactly within this scope.

## 2026-06-19 Local Codex Hardening Update

The first implementation pass is now complete as a preflight-only boundary. The generation context packet now carries concrete `metadata_refs` and `proof_packet_refs` with SHA256 digests, including:

```text
corpus_absorption_report
corpus_formula_bridge_report
formula_signal_store_report
local_corpus_db_survey_report
page18_readiness_precheck
page18_policy_review_warning_decision
page18_opening_gate_checklist
value_proof_guidance_report
value_proof_preregistration_report
value_proof_blind_evaluator_report
stage242_release_gate_report
release_gate_report
```

The boundary remains preflight-only:

```text
provider generation: false
output capture started: false
Page18 runtime opened: false
Stage243 created: false
runtime training: false
canonical mutation: false
raw corpus prompt export: false
```
