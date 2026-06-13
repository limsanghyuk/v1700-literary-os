# Frontend Component Contracts

Status: LIGHTWEIGHT_CONTRACT
Created: 2026-06-13
Scope: minimum component contracts for the Writer IDE advisory frontend blueprint.

## 1. Purpose

Define minimal UI component contracts for rendering the reviewed Writer IDE advisory panel packet.

This is not a frontend implementation and does not open Page18 or Stage243+.

## 2. Inputs

```text
fixtures/option_b_validation/frontend_renderer_blueprint_packet.json
fixtures/option_b_validation/writer_ide_advisory_panel_render_packet.json
fixtures/option_b_validation/writer_ide_render_packet_review_result.json
```

## 3. Component contracts

### AdvisoryCard

Required fields:

```text
card_id
panel_id
formula_signal_id
formula_name
surface_label
manual_review_status
display_mode
evidence_refs
```

Rules:

```text
display_mode == read_only_advisory
manual_review_status defaults to PENDING_REVIEW
no mutation event is emitted
```

### FormulaBoundaryBadge

Required fields:

```text
value_proof_status
learnable_critic_status
blocked_events
```

Rules:

```text
must show NOT_PROOF when applicable
must show NO_WEIGHT_UPDATE when applicable
```

### SourceRecordChip

Required fields:

```text
source_record_id
source_record_type
source_record_summary_ref
```

Rules:

```text
raw manuscript is not displayed
protected author-only content requires separate policy edge
```

### EvidenceRefList

Required fields:

```text
evidence_ref_id
evidence_ref_path
evidence_ref_type
```

Rules:

```text
all cards require at least two evidence refs
```

### ManualReviewControl

Required fields:

```text
review_object_id
allowed_decisions
default_decision
required_reviewer_role
```

Rules:

```text
default_decision == PENDING_REVIEW
allowed decisions do not perform mutation
```

### BlockedActionNotice

Required fields:

```text
blocked_events
boundary_status
```

Rules:

```text
blocked events must include generate_prose, write_memory, mutate_canon, update_weight, open_page18_runtime
```

## 4. Event boundary

Allowed:

```text
select_card
inspect_source_record_summary
inspect_evidence_ref
mark_review_decision_draft
```

Blocked:

```text
generate_prose
write_memory
mutate_canon
update_weight
open_page18_runtime
```

## 5. Acceptance criteria

```text
frontend_renderer_blueprint_packet.status == LIGHTWEIGHT_BLUEPRINT_READY
writer_ide_render_packet_review_result.overall_status == PASS
all component payloads preserve read_only_advisory mode
no component can perform mutation
```

## 6. Next candidate

```text
fixtures/option_b_validation/frontend_component_contracts_packet.json
```
