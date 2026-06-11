# Writer IDE Advisory Panel Renderer Blueprint

Status: PROPOSED_SCAFFOLD
Created: 2026-06-10
Scope: render-only blueprint after Option B Manual Static Review

## 1. Purpose

Define a renderer that turns `writer_ide_static_flow_result.json` and `manual_static_review_result.json` into a UI-facing advisory panel model.

This blueprint does not open Page18 runtime implementation.

## 2. Inputs

```text
fixtures/option_b_validation/writer_ide_static_flow_result.json
fixtures/option_b_validation/manual_static_review_result.json
fixtures/option_b_validation/formula_signal_mapping_result.json
```

## 3. Output

```text
fixtures/option_b_validation/writer_ide_advisory_panel_render_packet.json
```

## 4. Renderer contract

A render packet must include:

```text
render_packet_id
renderer_version
source_result_refs
panel_cards
review_state_summary
blocked_action_summary
manual_review_queue
page18_status
stage243_status
```

## 5. Panel card fields

```text
panel_id
formula_signal_id
formula_name
surface_label
source_record_ids
source_record_types
advisory_summary
manual_review_status
allowed_user_actions
blocked_user_actions
evidence_refs
```

## 6. Boundary invariants

```text
provider_status = DISABLED
generation_status = DISABLED
memory_write_status = DISABLED
canonical_mutation_status = NO_CANONICAL_MUTATION
value_proof_status = NOT_PROOF_PREREGISTRATION_REQUIRED
learnable_critic_status = NO_COEFFICIENT_UPDATE_AUDIT_REQUIRED
page18_status = NOT_OPENED
stage243_status = NOT_CREATED
```

## 7. UX layout proposal

```text
Left rail: Scene / source record navigator
Center: selected advisory card
Right rail: formula boundary and evidence inspector
Bottom: manual review decision queue
```

## 8. Acceptance criteria

```text
manual_static_review_result overall_status == PASS
panel_count == review_object_count
no panel can trigger generation
no panel can mutate canon
no panel can update weights
manual review remains pending unless a human decision record exists
```

## 9. Next implementation candidate

```text
tools/writer_ide_advisory_panel_renderer.py
tests/test_writer_ide_advisory_panel_renderer.py
fixtures/option_b_validation/writer_ide_advisory_panel_render_packet.json
```
