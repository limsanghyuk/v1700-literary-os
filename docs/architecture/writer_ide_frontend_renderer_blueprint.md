# Writer IDE Frontend Renderer Blueprint

Status: LIGHTWEIGHT_BLUEPRINT
Created: 2026-06-12
Scope: frontend layout and event-boundary plan only

## Purpose

Define the minimum frontend renderer shape for the already-reviewed Writer IDE advisory panel render packet.

This does not implement a frontend app, Page18 runtime, provider generation, memory write, canon mutation, or weight update.

## Input

```text
fixtures/option_b_validation/writer_ide_advisory_panel_render_packet.json
fixtures/option_b_validation/writer_ide_render_packet_review_result.json
```

## UI regions

```text
left_rail: source record navigator
center_panel: selected advisory card
right_rail: formula and evidence inspector
bottom_bar: manual review decision queue
```

## Component contracts

```text
AdvisoryCard
FormulaBoundaryBadge
SourceRecordChip
EvidenceRefList
ManualReviewControl
BlockedActionNotice
```

## Event boundary

Allowed frontend events:

```text
select_card
inspect_source_record_summary
inspect_evidence_ref
mark_review_decision_draft
```

Blocked frontend events:

```text
generate_prose
write_memory
mutate_canon
update_weight
open_page18_runtime
```

## Acceptance criteria

```text
input review result overall_status == PASS
all cards render as read_only_advisory
manual review status remains pending unless a human decision artifact exists
blocked action notice is visible
no frontend event performs mutation
```

## Next candidate

```text
fixtures/option_b_validation/frontend_renderer_blueprint_packet.json
```
