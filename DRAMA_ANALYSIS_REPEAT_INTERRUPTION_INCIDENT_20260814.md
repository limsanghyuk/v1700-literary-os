# Drama Analysis — Repeated Interruption Incident 2026-08-14

## Scope

Active work: `국희` THICK authoring.

Durable state after the repeated interruption:
- locked THICK sequences: 118 / 148
- last locked: `국희_16_S08`
- next durable sequence: `국희_17_S01`
- EP17–EP20 durable THICK semantic specs: 0
- EP17–EP20 durable THICK atomic records: 0
- EP17–EP20 durable THICK audits: 0

No Block03 semantic corruption was detected. Chat/source-reading progress beyond EP16 is not canonical progress because no `CHECKPOINT_LOCKED` semantic transaction exists for it.

## Root cause

The failure was not a drama-analysis quality failure. The assistant attempted to combine too many execution phases inside one response:

`EP17–20 source reading -> 30 THICK semantic transactions -> whole-work gate -> R5 -> R8 -> DB integration -> checksums -> ZIP -> fresh extraction -> hub promotion`

This violated the already-authoritative response lease and phase-separation rules. Documentation alone did not prevent the assistant from overcommitting the turn.

A second contributing factor was progress wording: source reading was reported before any durable THICK transaction was locked. Therefore a response interruption could make chat progress look ahead of durable disk progress.

## Non-overridable correction

1. Source reading without a `CHECKPOINT_LOCKED` THICK transaction is not progress.
2. Maximum newly authored THICK sequences per assistant response remains 3 and is mechanically enforced.
3. A response that authors THICK semantics must stop after closing its lease. It may not begin whole-work validation, R5, R8, DB integration, packaging, fresh extraction, or hub promotion.
4. Each later phase requires its own durable PASS evidence before the next phase can begin.
5. User requests such as “finish the block” describe the target milestone, not permission to override interruption-safety limits.
6. If the assistant response ends unexpectedly, the next response reconciles disk state and continues only from durable `next_seq_id`.

## Required mechanical control

Use `tools/drama_analysis_phase_guard.py` for long THICK work. The guard:
- caps one semantic lease at 3 commits;
- rejects a fourth commit;
- rejects out-of-order phase transitions;
- requires durable evidence to pass a phase;
- keeps source-reading-only activity out of progress accounting.

## Current recovery point

`국희_17_S01`.

The 25-work canonical authority remains unchanged until all 148 sequences, whole-work gates, R5/R8, integration, packaging, fresh extraction, and hub promotion pass in order.
