# Drama Analysis — New Session Bootstrap

This file is the current human-readable entrypoint. Do not begin a new drama-analysis session from an old handoff document.

## Live-hub freshness rule

A downloaded bundle is a snapshot, not permanent authority. At the start of every new session, first re-read live `main` versions of:

- `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json`
- `DRAMA_ANALYSIS_ACTIVE_WORK_CLAIMS.json`
- the live overlay pointer named by the integrated pointer
- `DRAMA_ANALYSIS_METHOD_CURRENT_20260814.md`
- `DRAMA_ANALYSIS_THREAD_CONTINUITY_POLICY_R1_20260815.md`

If bundle and live Hub differ, **live Hub wins**. Never downgrade a newer THICK/Planner/Runtime authority to a bundle snapshot. This is mandatory because other GPT sessions may analyze other dramas concurrently.

## Mandatory authority resolution

1. Read live `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json`.
2. Read `CURRENT_AUTHORITY_POINTER.json` and follow the authority it declares; never hardcode an old V10/V10.1 path.
3. Read `DRAMA_ANALYSIS_EXACT_SCHEMA_REGISTRY_V10_1.json` and the current authority mirror.
4. Follow the live integrated pointer's overlay pointer.
5. Read `DRAMA_ANALYSIS_METHOD_CURRENT_20260814.md`.
6. Read `DRAMA_ANALYSIS_THREAD_CONTINUITY_POLICY_R1_20260815.md` before any new THICK authoring.
7. Before long work, read `DRAMA_ANALYSIS_NEW_WORK_EXECUTION_RUNBOOK.md`, `DRAMA_ANALYSIS_ATOMIC_CHECKPOINT_AND_RESUME_PROTOCOL.md`, `DRAMA_ANALYSIS_THICK_RESPONSE_LEASE_PROTOCOL.md`, `DRAMA_ANALYSIS_REPEAT_INTERRUPTION_INCIDENT_20260814.md`, and `DRAMA_ANALYSIS_INTEGRATION_RELEASE_RECOVERY_PROTOCOL.md`. Use Block-Atomic V2 or an equivalent mechanical guard.
8. Read live `DRAMA_ANALYSIS_ACTIVE_WORK_CLAIMS.json` before selecting a target so concurrent sessions do not claim the same work.
9. After selecting/resuming a work, read SourceLock plus current work_state/checkpoint and execution-guard state before writing.

## Semantic authoring invariant

The drama script itself is primary authority. The model reads the source directly and sequentially and authors new narrative meaning itself. Python may extract, normalize, lock, hash, serialize, validate, compare, assemble, and package; Python must not invent narrative semantics.

One complete episode is the Stage01–04 semantic authoring unit. Q1→Q2→Q3→Q4 are attention/checkpoint units, not dramatic four-act labels. A block of up to eight contiguous episodes is an execution-limit boundary, not a semantic schema.

The canonical order is SourceBoundaryReview → Stage01 → Stage02 → Stage03 → full-series Stage04. LocalEdge is same-episode causal only with `gap_episodes=0`; cross-episode relations belong to Stage04.

For an existing PASS Stage01–04 work that lacks THICK, preserve Stage01–04, use SequenceBlueprint only as sequence boundaries, re-read source, and author THICK independently. Stage02 event copying, Stage01/02 cast-function reuse, generic cast templates, duplicate cast functions, and unresolved evidence are blocking errors.

## Thread Continuity R1 — mandatory for new drama THICK

For each `plant_payoff` entry, decide from source whether it opens a genuinely new dramatic thread or continues an existing one.

- A new semantic `thread_id` is normally created only at a genuinely new `PLANT`/`HOOK`.
- `CONTINUE`, `ESCALATION`, `CALLBACK`, `REACTIVATION`, `REVERSAL`, `PAYOFF`, and related manifestations reuse the established thread ID.
- Use semantic IDs, not per-episode serial IDs.
- Check direct source, prior ID, `existing_refs`, and source-grounded Stage03/04 evidence before issuing another ID.
- Do not merge distinct threads to improve a metric.
- The current 40%/30% continuity lines are provisional diagnostics, not canonical hard gates.
- `resolves_thread` is not part of the current exact schema.

If a THICK thread ID changes, affected R5/R8 must be regenerated.

## Planner / Runtime / EXT6 boundary

Authority order is `Source/SourceLock → Stage01 → Stage02 → Stage03 → Stage04 → CANONICAL THICK → PlannerInput R5 → Runtime R8`.

R5 Episode N may consume only state known through N−1. Thread continuity never permits target/future leakage. R8 is deterministic projection from current THICK plus same-episode R5 and becomes stale if THICK changes.

EXT6 is a `SELECTIVE_APPEND_ONLY` evidence sidecar and does not supersede Stage01–04 or THICK. Base Stage01–04 must remain byte-immutable under EXT6.

## Interruption / release invariant — Block-Atomic V2

Durable disk state outranks chat progress. THICK completion requires `CHECKPOINT_LOCKED`; source reading alone is not progress.

- A THICK execution block is at most 8 contiguous episodes.
- There is **no arbitrary per-response sequence-count cap**. The temporary 3-Sequence hard cap is retired.
- Each sequence is committed atomically in exact `next_seq_id` order before the next begins.
- A completed episode is rebuilt from current atomic records and checkpointed.
- A completed block requires an independent block strong gate.
- Background/late writer continuation is forbidden; overrun output is quarantined.

Durable phases:

`THICK_BLOCK_AUTHORING → BLOCK_GATE → WHOLE_WORK_GATE → R5_BUILD → R8_BUILD → DB_INTEGRATION → CHECKSUM_BUILD → ZIP_BUILD → FRESH_EXTRACTION → HUB_PROMOTION`

Each phase requires durable PASS evidence before transition; do not run the entire chain as one mega-script. Hub promotion is last.

## Current canonical snapshot

At this synchronization point the live Hub remains:

- Stage01–04: `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1`, 98 works / 1,814 episodes / 114,371 SceneCards.
- EXT6: 35-work append-only cohort.
- CANONICAL THICK: `DB98_THICK_26WORK_CANONICAL_AUTHORITY_20260814_V1_GUKHEE_INTEGRATED`, 26 works / 3,883 records.
- Planner/Runtime: 26 works / 470 PlannerInput / 470 Runtime / 29,628 runtime scenes.
- 26th work `국희`: 20 episodes / 148 THICK / 1,287 Runtime scenes.
- Full DB: `DB98_98WORK_STAGE04_26THICK_CLEAN_V8_GUKHEE_INTEGRATED_FINAL_20260814.zip`, SHA256 `39fea427974c212a0e42cf7cc1b63f1ddff875da050443091c77e0522cb4efe7`.

The separate 26-work quality-equalized repair tree and `돌아온일지매` thread-ID pilot are **candidate/pilot evidence only and are not current canonical authority**.

Canonical repository: `limsanghyuk/v1700-literary-os`.
