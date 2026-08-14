# Drama Analysis — New Session Bootstrap

This file is the current human-readable entrypoint. Do not begin a new drama-analysis session from an old handoff document.

## Mandatory authority resolution

1. Read `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json`.
2. Read `CURRENT_AUTHORITY_POINTER.json` and follow the authority it declares. Never hardcode a historical V10/V10.1 path. The current pointer resolves to `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1`.
3. Read `DRAMA_ANALYSIS_EXACT_SCHEMA_REGISTRY_V10_1.json` and the current authority mirror.
4. Read `DRAMA_ANALYSIS_CURRENT_OVERLAY_POINTERS_20260814_26WORK.json` for current CANONICAL THICK and Planner/Runtime authority IDs.
5. Read `DRAMA_ANALYSIS_METHOD_CURRENT_20260814.md`.
6. Before long THICK work, read `DRAMA_ANALYSIS_NEW_WORK_EXECUTION_RUNBOOK.md`, `DRAMA_ANALYSIS_ATOMIC_CHECKPOINT_AND_RESUME_PROTOCOL.md`, `DRAMA_ANALYSIS_THICK_RESPONSE_LEASE_PROTOCOL.md`, `DRAMA_ANALYSIS_REPEAT_INTERRUPTION_INCIDENT_20260814.md`, and `DRAMA_ANALYSIS_INTEGRATION_RELEASE_RECOVERY_PROTOCOL.md`. Use `tools/drama_analysis_phase_guard.py` or an equivalent Block-Atomic V2 guard.
7. Read `DRAMA_ANALYSIS_ACTIVE_WORK_CLAIMS.json` before selecting a target. This coordination file never overrides semantic/release authority.
8. After selecting or resuming a work, read SourceLock plus current work_state/checkpoint and execution-guard state before writing.

## Semantic authoring invariant

The drama script itself is primary authority. The model reads the source directly and sequentially and authors new narrative meaning itself. Python may extract, normalize, lock, hash, serialize, validate, compare, assemble, and package; Python must not invent narrative semantics.

One complete episode is the Stage01–04 semantic authoring unit. Q1→Q2→Q3→Q4 are attention/checkpoint units, not dramatic four-act labels. A block of up to eight contiguous episodes is an execution-limit boundary, not a semantic schema.

The canonical order is SourceBoundaryReview → Stage01 → Stage02 → Stage03 → full-series Stage04. LocalEdge is same-episode causal only with `gap_episodes=0`; cross-episode relations belong to Stage04.

For an existing PASS Stage01–04 work that lacks THICK, preserve Stage01–04, use SequenceBlueprint only as sequence boundaries, re-read the source, and author THICK independently. Stage02 event copying, Stage01/02 cast-function reuse, generic cast templates, duplicate strict cast functions, and unresolved evidence are blocking errors.

## Planner / Runtime / EXT6 boundary

Authority order is `Source/SourceLock → Stage01 → Stage02 → Stage03 → Stage04 → CANONICAL THICK → PlannerInput R5 → Runtime R8`.

R5 Episode N may consume only state known through N−1. R8 is deterministic projection from current THICK plus same-episode R5; it does not independently author meaning and becomes stale if THICK changes.

EXT6 is a `SELECTIVE_APPEND_ONLY` evidence sidecar. It does not supersede Stage01–04 or THICK. Current exact records are EntityRegistry, EntityBridge, CastPresence, CharacterLoad, CastCoverageLedger, SourceHeadingRegistry, and SourceSceneAlignment. Base Stage01–04 must remain byte-immutable under EXT6.

## Interruption / release invariant — Block Atomic V2

Durable disk state outranks chat progress. THICK completion requires `CHECKPOINT_LOCKED`; source reading alone is not progress.

- A THICK execution block is at most 8 contiguous episodes.
- There is no arbitrary per-response sequence-count cap.
- Each sequence is committed atomically and in exact `next_seq_id` order before the next sequence begins.
- A completed episode is reassembled from current atomic records and checkpointed.
- A completed block requires an independent block strong gate.
- Background or late writer continuation is forbidden; late output is quarantined and must be source-reread/revalidated before any later acceptance.

The durable phases are `THICK_BLOCK_AUTHORING → BLOCK_GATE → WHOLE_WORK_GATE → R5_BUILD → R8_BUILD → DB_INTEGRATION → CHECKSUM_BUILD → ZIP_BUILD → FRESH_EXTRACTION → HUB_PROMOTION`. Each phase requires durable PASS evidence before transition. Do not run the entire chain as one mega-script. The hub is promoted last.

## Current overlay closure — 2026-08-14

- Stage01–04: `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1`, 98 works / 1,814 episodes / 114,371 SceneCards; unchanged.
- EXT6: 35-work append-only cohort; unchanged.
- CANONICAL THICK: `DB98_THICK_26WORK_CANONICAL_AUTHORITY_20260814_V1_GUKHEE_INTEGRATED`, 26 works / 3,883 records.
- THICK strict semantic-independence V3: PASS, blocking errors 0.
- Exact/provenance/source: PASS, 68,659 SOURCE refs / 19,415 hash checks / errors 0.
- Planner/Runtime V1.1: `DB98_PLANNER_RUNTIME_26WORK_CANONICAL_PROFILE_V1_1_AUTHORITY_20260814_V1_GUKHEE_INTEGRATED`, 26 works / 470 PlannerInput files / 470 Runtime files / 29,628 runtime scene records; errors 0.
- 26th work `국희`: 20 episodes / 148 THICK records / 1,287 Runtime scene records; whole-work, semantic, exact/provenance, quality, R5/R8 all PASS.
- Predecessor 25-work immutability: 26,636 pre-existing files checked before authority metadata promotion; missing 0 / changed 0.
- Full database ZIP: `DB98_98WORK_STAGE04_26THICK_CLEAN_V8_GUKHEE_INTEGRATED_FINAL_20260814.zip`, SHA256 `39fea427974c212a0e42cf7cc1b63f1ddff875da050443091c77e0522cb4efe7`; final fresh extraction PASS.

Canonical repository: `limsanghyuk/v1700-literary-os`.
