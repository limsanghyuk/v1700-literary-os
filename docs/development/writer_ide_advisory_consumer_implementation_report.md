# Writer IDE Advisory Consumer Implementation Report

Status: implemented  
Date: 2026-06-16  
Branch: `corpus-absorption-formula-bridge-handoff`

## Goal

This step implements the next ranked continuation after the LearnableCritic audit fixture:

```text
Writer IDE advisory consumer
```

The purpose is to convert existing advisory outputs into a writer-visible, review-locked surface that can be read by both the local Codex workflow and the web ChatGPT project workflow.

## What was added

Code:

```text
src/v1700/writer_ide_advisory_consumer/
tools/run_writer_ide_advisory_consumer.py
tests/test_writer_ide_advisory_consumer.py
```

Hub-facing docs:

```text
docs/architecture/writer_ide_advisory_consumer_runtime_blueprint.md
docs/development/writer_ide_advisory_consumer_implementation_report.md
```

Generated evidence:

```text
release/current/writer_ide_advisory_pack/
```

## Runtime behavior

The consumer reads:

- formula signal store report
- writer IDE advisory cards
- LearnableCritic audit report

Then it builds:

- `WriterSessionRecord`
- `LearnableCriticExplanationRecord`
- `ApprovalBoundaryWarning`
- focus-work visible advisory cards
- review-locked advisory board

## Important behavior

The implementation keeps three important rules visible:

1. the board is tied to one focus work
2. LearnableCritic output is visible but not promotable by itself
3. canonical mutation remains blocked behind `ApprovalDecisionRecord`

## Safe interpretation

This is not a full IDE and not a canonical writing engine.

It is:

- a projection layer
- a visibility layer
- an approval-boundary layer
- a hub-recorded evidence layer

## Expected output meaning

The output pack answers these practical questions for the web project:

- what the writer would see right now
- which signals are visible in left/center/right zones
- what remains blocked
- what record must exist before any canonical mutation

## Current run snapshot

From the latest local run:

```text
focus_work_id: 10부
surface_card_count: 4
signal_ref_count: 3
corpus_ref_count: 1
promotion_blocker_count: 3
```

## Validation expectations

The consumer passes only if:

- all cards remain advisory
- all cards stay on one work
- left, center, and right zones exist
- approval warning exists
- board promotion blockers exist

## Continuity effect

This step closes the gap between:

```text
formula signal registry
-> LearnableCritic audit pack
-> actual writer-visible advisory surface
```

That makes the next steps easier to reason about in the web project because the advisory chain is no longer abstract.

## Next recommended step

The next ranked continuation is:

```text
Value Proof Arm B guidance surface
```

That step should consume the same formula signal store and should preserve the same review-only boundary discipline.
