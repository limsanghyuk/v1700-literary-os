# Drama Analysis — New Work Execution Runbook

This runbook is execution guidance under the current authority pointers. It does not replace them.

## 0. Resolve live authority first

Read, in order:
1. `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json`
2. `CURRENT_AUTHORITY_POINTER.json`
3. the authority and exact-schema registry named by that pointer
4. the current THICK/Planner/Runtime overlay pointer
5. `DRAMA_ANALYSIS_METHOD_CURRENT_20260814.md`
6. `DRAMA_ANALYSIS_THREAD_CONTINUITY_POLICY_R1_20260815.md`
7. `DRAMA_ANALYSIS_ATOMIC_CHECKPOINT_AND_RESUME_PROTOCOL.md`
8. live `DRAMA_ANALYSIS_ACTIVE_WORK_CLAIMS.json`
9. the target work SourceLock, work_state, and last durable checkpoint

Never hardcode a historical authority version or downgrade a newer live Hub authority to a downloaded bundle snapshot.

## 1. Mandatory recovery preflight

Before new writing, reconcile durable disk state. Previous chat prose is not progress authority.

- Refuse to write if another writer owns the work lock.
- Compare semantic specs, atomic records, audits, episode assemblies, and work_state.
- Reassemble a completed episode if its atomic sequence records are complete but episode JSONL is missing.
- Quarantine late/overrun output and do not accept it merely because a file exists.
- Resume only from the recomputed durable `next_seq_id`.

## 2. Determine target state

### Work has no Stage01–04
Follow the active Stage01–04 authority from direct source reading through Stage04 and validation before THICK.

### Work already has PASS Stage01–04 but no THICK
Do not blanket reauthor Stage01–04. Verify SourceLock/current work state, use SequenceBlueprint only as sequence boundaries, re-read source directly, and author THICK independently under the current strict profile.

## 3. Stage01–04 invariant

One complete episode is the Stage01–04 semantic authoring unit. Q1–Q4 and blocks of at most eight contiguous episodes are attention/checkpoint/audit units only. LocalEdge is same-episode only; cross-episode relations belong to Stage04.

Python may extract, normalize, lock, hash, serialize, validate, compare, assemble, and package. Python must not generate narrative meaning.

## 4. THICK strict new-work profile

For each sequence, directly read its member-scene source ranges. Author sequence-specific cast desire/function, causal event chain, real information-state changes, source-supported plant/payoff, and one scene-note record per member scene.

Blocking patterns include Stage02-exact event reuse, Stage01/02-exact cast-function reuse, cast functions composed only of copied Stage01 sentences, generic cast templates, duplicate cast functions inside a sequence, and unresolved SOURCE/evidence for newly authored meaning.

Do not paraphrase merely to lower overlap metrics.

## 5. Mandatory thread continuity — R1

For every plant/payoff entry, determine whether it opens a genuinely new dramatic thread or continues an existing one.

- Issue a new semantic `thread_id` only for a genuinely new `PLANT` or `HOOK`.
- Reuse that ID for later `CONTINUE`, `ESCALATION`, `CALLBACK`, `REACTIVATION`, `REVERSAL`, `PAYOFF`, and related manifestations of the same thread.
- Use durable semantic IDs, not episode/sequence serial IDs.
- Check direct source, prior thread identity, `existing_refs`, Stage03/04 evidence, and prior unresolved state before creating a new ID.
- Do not merge related-but-distinct threads merely to raise a continuity metric.
- The currently discussed 40% multi-episode and 30% R5-coupling values are diagnostics, not canonical hard gates.
- `resolves_thread` is not in the current exact schema and must not be added without explicit schema promotion.

If THICK thread IDs change, regenerate affected R5 and R8.

## 6. Interruption-safe execution — Block-Atomic V2

For THICK/new overlay authoring: `1 sequence = 1 atomic transaction`.

`SOURCE_READ -> SEMANTIC_AUTHORED -> spec atomic write -> exact/source/thread audit -> THICK record atomic write -> episode assemble if closed -> CHECKPOINT_LOCKED`

Only `CHECKPOINT_LOCKED` counts as completion.

Execution boundary:

- A THICK execution block may contain at most 8 contiguous episodes.
- There is **no fixed per-response sequence-count cap**. The temporary 3-Sequence hard cap is retired.
- Read source in bounded current-sequence/member-scene chunks rather than dumping an entire multi-episode block into one undifferentiated prompt.
- Lock each sequence before beginning the next.
- Close each episode by rebuilding episode JSONL from current atomic records and writing an episode checkpoint.
- Close each block with an independent strong gate.
- Background/late semantic continuation after the response boundary is forbidden.

If interrupted, reconcile the valid contiguous prefix and continue from `next_seq_id`; do not repeat already locked work.

## 7. PlannerInput R5

Episode N may use only state available through N-1. EP01 has no previous exit state, prior character/relationship state, unresolved threads, or debt. Future/target source and analysis are holdout and must be blocked from generator input.

Thread continuity does not override future-blindness: R5 may carry only unresolved threads known before the target episode.

## 8. Runtime R8

R8 is deterministic projection from current CANONICAL THICK plus same-episode R5. It is not an independent semantic-authoring layer. If THICK changes, affected Runtime is stale and must be regenerated.

## 9. Durable phase separation

Use separate durable phases:

`THICK_BLOCK_AUTHORING -> BLOCK_GATE -> WHOLE_WORK_GATE -> R5_BUILD -> R8_BUILD -> DB_INTEGRATION -> CHECKSUM_BUILD -> ZIP_BUILD -> FRESH_EXTRACTION -> HUB_PROMOTION`

Each phase requires durable PASS evidence before transition. Do not combine the entire chain into one mega-script or background process.

## 10. Promotion gate

Run exact schema, source/evidence, semantic-independence, thread-continuity diagnostics, R5/R8 parity, manifest/work_state, non-target immutability, package integrity, fresh extraction, and packaged validator checks. Promote only when blocking errors are zero.

Thread-continuity diagnostics must never be gamed by false merging. Preserve prior authority and artifacts through lineage/supersession; do not silently overwrite history.
