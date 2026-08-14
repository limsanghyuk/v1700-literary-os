# Drama Analysis — Repeated Interruption Incident 2026-08-14

## Scope and original recovery point

Active work: `국희` THICK authoring.

After the repeated interruption the durable state was 118/148, last `국희_16_S08`, next `국희_17_S01`. Chat/source-reading progress beyond EP16 was not accepted because no `CHECKPOINT_LOCKED` transaction existed.

A later reconciliation also found late/overrun EP17–EP20 semantic files and premature 26-work/R5/R8 candidates. They were quarantined rather than treated as progress.

## Root cause

The failure was not a drama-analysis quality failure and was not caused by the number of sequences in an episode or block. The actual failure mechanism was attempting to execute too many different phases as one long flow:

`source reading -> THICK authoring -> whole-work gate -> R5 -> R8 -> DB integration -> checksums -> ZIP -> fresh extraction -> hub promotion`

A second factor was late/background writer output appearing after the response boundary, and progress wording that made source reading look ahead of durable disk state.

## Temporary mitigation and correction

A temporary 3-sequence-per-response hard cap was introduced immediately after the incident. Subsequent review showed that this cap was over-constrained and conflicted with the developer-defined execution model of blocks of up to 8 episodes. It also targeted sequence count rather than the real failure mode.

**The 3-sequence hard cap is superseded by Block-Atomic V2.**

Current non-overridable rules are:
1. Source reading without `CHECKPOINT_LOCKED` is not progress.
2. One THICK sequence is one atomic semantic transaction and must be durable before the next begins.
3. One execution block may contain at most 8 contiguous episodes; there is no arbitrary per-response sequence-count cap.
4. Completed episodes are rebuilt from current atomic records and checkpointed.
5. Block completion requires durable strong-gate PASS evidence.
6. Whole-work gate, R5, R8, DB integration, packaging, fresh extraction, and hub promotion are later durable phases and may not be hidden inside one mega-script.
7. Background/late semantic writer continuation is forbidden. Late output is quarantined and can be used only as comparison evidence after source reread and revalidation.
8. On interruption, reconcile durable state and resume from exact `next_seq_id` without repeating earlier locked work.

## Mechanical control

`tools/drama_analysis_phase_guard.py` implements Block-Atomic V2. It enforces ordered expected sequence IDs, at-most-eight-episode blocks, parseable durable spec/record/PASS audit before commit, block completeness before the block gate, and durable PASS evidence before later phase transitions.

## Resolution on 국희 Block03

The quarantined overrun was not silently promoted. EP17–EP20 were source-reread/revalidated and committed through the block-atomic path. Block03 closed at 30/30 and the whole work reached 148/148 with strict semantic-independence and exact/provenance checks passing. The next phase is `WHOLE_WORK_GATE`; the 25-work canonical authority remains unchanged until later promotion phases pass.
