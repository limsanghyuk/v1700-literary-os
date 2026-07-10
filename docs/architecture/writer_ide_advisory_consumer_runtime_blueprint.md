# Writer IDE Advisory Consumer Runtime Blueprint

Status: implementation blueprint  
Created: 2026-06-16  
Scope: advisory-only Writer IDE surface consumer

## Purpose

This runtime blueprint defines the first Writer IDE-facing consumer that turns existing formula signal and LearnableCritic audit artifacts into a review-locked advisory surface.

The goal is not to implement a full IDE. The goal is to prove what the writer would see, what remains blocked, and what evidence must be recorded before any canonical mutation.

## Inputs

- `release/current/formula_signal_store_pack/formula_signal_store_report.json`
- `release/current/formula_signal_store_pack/writer_ide_advisory_cards.json`
- `release/current/learnable_critic_audit_pack/learnable_critic_audit_report.json`

## Output pack

The consumer writes:

```text
release/current/writer_ide_advisory_pack/
  writer_session_record.json
  learnable_critic_explanation_record.json
  approval_boundary_warning.json
  writer_ide_surface_cards.json
  writer_ide_advisory_board.json
  writer_ide_advisory_validation_report.json
  writer_ide_advisory_consumer_report.json
```

## Runtime model

```text
existing formula signal cards
-> focus work selection
-> left/right advisory card projection
-> center approval-boundary review card
-> writer session record
-> learnable critic explanation record
-> approval boundary warning
-> review-locked board
```

## Focus work rule

The primary work should come from the current LearnableCritic audit signal when available.

Fallback order:

1. `selected_formula_signal` from LearnableCritic audit report
2. first `work_id` available in Writer IDE advisory cards

## Surface zones

The advisory consumer preserves the three-zone blueprint:

- `left`: corpus grounding and reference context
- `center`: approval boundary and decision warning
- `right`: formula/tensor/critic advisory signals

## Authority boundary

The consumer is valid only if:

- every visible card remains advisory
- `canonical_mutation_allowed` is false everywhere
- LearnableCritic explanation remains review-only
- approval boundary warning is visible
- promotion blockers are recorded on the board

## Writer session boundary

The initial session shape is:

```text
session_scope = LEARNABLE_CRITIC_REVIEW
llm_boundary_level = LLM-0
session_status = LOCKED_FOR_REVIEW
```

That means:

- a writer-visible session exists
- an audit trail exists
- no canonical insertion is permitted

## Promotion blockers

The board must record at least:

- `approval_decision_required`
- `scene_diff_required_for_canonical_change`
- `learnable_critic_output_remains_advisory`

## Blocking failures

- focus surface mixes multiple works
- any card is non-advisory
- approval warning is absent
- center review zone is absent
- board claims canonical mutation is allowed
- LearnableCritic explanation bypasses approval contract

## Next integration target

After this consumer, the next natural consumer is:

- Value Proof Arm B guidance surface

That step should reuse the same focus-work discipline and the same approval visibility rule.
