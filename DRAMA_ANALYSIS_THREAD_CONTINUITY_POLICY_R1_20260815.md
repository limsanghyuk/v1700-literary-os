# Drama Analysis — Thread Continuity Policy R1

Date: 2026-08-15
Status: ACTIVE_NEW_WORK_METHOD_POLICY
Authority relation: supplements the current drama-analysis method; does not change the exact THICK schema by itself.

## Purpose

A plant/payoff or causal thread is a long-lived narrative identity. If the same dramatic thread receives a different `thread_id` in each episode, humans may understand the continuity but PlannerInput R5 and downstream tools cannot reliably track unresolved debt, continuation, escalation, and payoff.

This policy makes thread identity continuity mandatory for all newly authored THICK work.

## Thread identity issuance

A new semantic `thread_id` is issued only when a genuinely new dramatic thread is first created by `PLANT` or `HOOK`.

Later manifestations of the same thread reuse that ID for `CONTINUE`, `ESCALATION`, `CALLBACK`, `REACTIVATION`, `REVERSAL`, `PAYOFF`, and related `REVEAL` or `LINK` when they are manifestations of the same already-open thread.

Do not create a new ID merely because the episode changes.

## Semantic ID form

Thread IDs express durable semantic identity rather than an episode-local serial.

Good: `가을동화_은서_출생비밀`

Bad: `가을동화_p05002`

Episode number, sequence number, or a per-episode counter must not be the semantic identity of a continuing thread.

## Continuation versus new thread

Before issuing a new ID, directly inspect the source and prior-state evidence. Priority evidence is:

1. direct source reading;
2. an existing prior `thread_id` whose dramatic subject/object/causal question is the same;
3. `existing_refs` into an earlier episode;
4. Stage03 PayoffCandidate / Stage04 CrossEpisodeEdge or other source-grounded prior evidence;
5. prior R5 unresolved payoff / causal debt as retrieval aid only, never as higher authority than source.

Related themes are not automatically the same thread. Do not merge distinct threads merely because they share a character, location, motif, or broad topic.

## No metric gaming

Thread-continuity metrics are diagnostic. They do not authorize semantic merging.

The current diagnostic checker may report multi-episode thread-ID percentage, prior-episode `existing_refs` percentage, and R5 coupling percentage.

The proposed `multi-episode >= 40%` and `R5 coupling >= 30%` lines are provisional cohort diagnostics, not canonical correctness gates. A work must not be altered merely to cross them. Correct identity with a lower diagnostic score is preferable to an incorrect merge with a higher score.

## R5/R8 dependency

If any THICK `thread_id` changes:

1. affected PlannerInput R5 is stale and must be regenerated from corrected THICK under the normal future-blind rule;
2. affected Runtime R8 is stale and must be regenerated from current THICK plus same-episode R5;
3. R5 regeneration must not inspect target/future episode facts to decide which prior threads are carried forward.

A coupling metric may therefore remain below a provisional threshold even when R5 is correctly future-blind.

## Retrospective repair

Existing canonical works must not be repaired by broad automatic similarity merging.

Allowed: high-confidence ID-only rebinding supported by direct source and/or explicit prior refs; before/after ID ledger; semantic-payload invariance check; R5/R8 regeneration; before/after diagnostics.

Forbidden unless separately reauthored and validated: changing `event`, `cast.desire_or_function`, `info_shift`, `plant_payoff.statement`, `scene_notes.functional_propositions`, or evidence/source coordinates merely to raise continuity scores.

## Exact-schema boundary

`resolves_thread: true|false` is a useful schema proposal for distinguishing a payoff occurrence from complete thread closure, but it is NOT part of the current exact THICK schema. It remains experimental until an anchor/ablation test demonstrates value and the exact schema registry is deliberately version-promoted.

## New-work atomic checkpoint

For each newly authored THICK sequence containing plant/payoff entries:

`SOURCE_READ -> identify new versus continuing thread -> reuse or issue semantic thread_id -> write statement/evidence -> atomic THICK audit -> CHECKPOINT_LOCKED`

The audit should flag episode-serial-style IDs for continuing threads, a continuing kind that creates a new ID without source-grounded reason, and a reused ID whose semantic subject is demonstrably a different thread.

## Anchor pilot evidence

The first retrospective anchor pilot used `돌아온일지매` with high-confidence ID-only aliases. It improved multi-episode identity and R5 coupling without changing semantic payload, but did not justify over-merging to satisfy the provisional 30% R5 line.

This supports adopting R1 prospectively on new works while keeping retrospective repair conservative.
