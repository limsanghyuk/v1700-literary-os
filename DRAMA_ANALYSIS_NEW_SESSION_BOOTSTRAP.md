# Drama Analysis — New Session Bootstrap

This file is the current human-readable entrypoint. Do not begin a new drama-analysis session from an old handoff document.

## Mandatory authority resolution

1. Read `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json`.
2. Read `CURRENT_AUTHORITY_POINTER.json` and follow the authority it declares. Never hardcode a historical V10/V10.1 path. The current pointer resolves to `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1`.
3. Read `DRAMA_ANALYSIS_EXACT_SCHEMA_REGISTRY_V10_1.json` and the current authority mirror.
4. Read `DRAMA_ANALYSIS_CURRENT_OVERLAY_POINTERS_20260814_25WORK.json` for current CANONICAL THICK and Planner/Runtime authority IDs.
5. Read `DRAMA_ANALYSIS_METHOD_CURRENT_20260814.md`.
6. Before long THICK work, also read `DRAMA_ANALYSIS_NEW_WORK_EXECUTION_RUNBOOK.md`, `DRAMA_ANALYSIS_ATOMIC_CHECKPOINT_AND_RESUME_PROTOCOL.md`, `DRAMA_ANALYSIS_THICK_RESPONSE_LEASE_PROTOCOL.md`, `DRAMA_ANALYSIS_REPEAT_INTERRUPTION_INCIDENT_20260814.md`, and `DRAMA_ANALYSIS_INTEGRATION_RELEASE_RECOVERY_PROTOCOL.md`. Use `tools/drama_analysis_phase_guard.py` or an equivalent mechanical guard; documentation-only compliance is not sufficient.
7. Read `DRAMA_ANALYSIS_ACTIVE_WORK_CLAIMS.json` before selecting a new target so concurrent sessions do not claim the same work. This coordination file never overrides semantic/release authority.
8. After selecting or resuming a work, read SourceLock plus current work_state/checkpoint and execution-guard state before writing.

## Semantic authoring invariant

The drama script itself is primary authority. The model reads the source directly and sequentially and authors new narrative meaning itself. Python may extract, normalize, lock, hash, serialize, validate, compare, and package; Python must not invent narrative semantics.

One complete episode is the semantic authoring unit. Q1→Q2→Q3→Q4 are attention/checkpoint units, not dramatic four-act labels. A block of up to eight episodes is an execution-limit boundary, not a semantic schema.

The canonical order is SourceBoundaryReview → Stage01 → Stage02 → Stage03 → full-series Stage04. LocalEdge is same-episode causal only with `gap_episodes=0`; cross-episode relations belong to Stage04.

For an existing PASS Stage01–04 work that lacks THICK, preserve Stage01–04, use SequenceBlueprint only as sequence boundaries, re-read the source, and author THICK independently. Stage02 event copying, Stage01/02 cast-function reuse, generic cast templates, duplicate strict cast functions, and unresolved evidence are blocking errors.

## Planner / Runtime / EXT6 boundary

Authority order is `Source/SourceLock → Stage01 → Stage02 → Stage03 → Stage04 → CANONICAL THICK → PlannerInput R5 → Runtime R8`.

R5 Episode N may consume only state known through N−1. R8 is deterministic projection from current THICK plus the same-episode R5; it does not independently author meaning and becomes stale if THICK changes.

EXT6 is a `SELECTIVE_APPEND_ONLY` evidence sidecar. It does not supersede Stage01–04 or THICK. Current exact records are EntityRegistry, EntityBridge, CastPresence, CharacterLoad, CastCoverageLedger, SourceHeadingRegistry, and SourceSceneAlignment. Base Stage01–04 must remain byte-immutable under EXT6.

## Interruption / release invariant

Durable disk state outranks chat progress. THICK completion requires `CHECKPOINT_LOCKED`. Source reading alone is not progress. New THICK semantic authoring uses one atomic sequence transaction and a mechanically enforced response lease; at most three newly authored sequences are accepted per assistant response. At response end, close the lease, fsync the checkpoint, release the writer lock, freeze semantic write surfaces, record `next_seq_id`, and stop.

A response that authors THICK semantics must not also begin whole-work validation, R5, R8, database promotion, checksums, ZIP creation, fresh extraction, or hub promotion. Those are later phases, each requiring its own durable PASS evidence before transition.

Whole-database integration/release is phase-separated: baseline reconcile → target payload integrate → non-target immutability → authority promote → strong validate → full parse/authority closure → checksums → ZIP → fresh extract → postzip validate → hub promote. The hub is promoted last.

## Current overlay closure — 2026-08-14

- Stage01–04: `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1`, 98 works / 1,814 episodes / 114,371 SceneCards; unchanged.
- EXT6: 35-work append-only cohort; unchanged.
- CANONICAL THICK: `DB98_THICK_25WORK_CANONICAL_AUTHORITY_20260814_V1_GHJ_INTEGRATED`, 25 works / 3,735 records.
- THICK strict semantic-independence V3: PASS, blocking errors 0.
- Exact/provenance/source: PASS, 65,915 SOURCE refs / 18,675 hash checks / errors 0.
- Planner/Runtime V1.1: `DB98_PLANNER_RUNTIME_25WORK_CANONICAL_PROFILE_V1_1_AUTHORITY_20260814_V1_GHJ_INTEGRATED`, 25 works / 450 PlannerInput files / 450 Runtime files / 28,341 runtime scene records; errors 0.
- 25th work `구해줘`: 16 episodes / 162 THICK records / 903 Runtime scene records; semantic, exact/provenance, quality, R5/R8 all PASS.
- Predecessor 24-work immutability: 26,559 predecessor files checked before metadata promotion; missing 0 / changed 0.
- Full database ZIP: `DB98_98WORK_STAGE04_25THICK_CLEAN_V7_GHJ_INTEGRATED_FINAL_20260814.zip`.
- Full database SHA256: `87bf39e78fce21943e52ce799688bbf9e71ffcb52b3d5dce211ba7b1b1836f37`.
- Final fresh extraction: PASS.
- Updated new-session bundle: `DRAMA_ANALYSIS_NEW_SESSION_COMPLETE_BUNDLE_20260814_25WORK.zip`, SHA256 `af924167546064b100bba0144e02b9a7eb4587b88ed39e1ec6b865678c114152`.
- Active coordination claim: `국희` THICK authoring is in progress on the ㄱ track; consult `DRAMA_ANALYSIS_ACTIVE_WORK_CLAIMS.json` for the current claimed work and resume point.

Canonical repository: `limsanghyuk/v1700-literary-os`.
