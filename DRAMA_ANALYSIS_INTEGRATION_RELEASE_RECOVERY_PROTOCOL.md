# Drama Analysis — Integration / Release Recovery Protocol

This protocol extends the existing atomic semantic checkpoint rules to whole-database integration, authority promotion, validation, packaging, and fresh-extraction work. It does not replace the active Stage01–04 authority or semantic authoring protocol.

## Why this exists

A previous 24-work integration run completed the semantic payload copy and strong validation but stopped before authority promotion and release sealing. The durable tree contained the new work while current pointers and final manifests still declared the predecessor authority. This is a revision-skew failure, not a semantic-authoring failure.

## Required phase separation

Never execute all of the following as one long command or one opaque tool call:

1. BASELINE_RECONCILE
2. TARGET_PAYLOAD_INTEGRATE
3. NON_TARGET_IMMUTABILITY_CHECK
4. AUTHORITY_PROMOTE
5. STRONG_VALIDATE
6. FULL_PARSE_AND_AUTHORITY_CLOSURE
7. CHECKSUM_BUILD
8. ZIP_BUILD
9. FRESH_EXTRACT
10. POSTZIP_VALIDATE
11. HUB_PROMOTE

Each phase must leave a durable report before the next phase starts.

## Durable state is stronger than chat state

At restart, inspect the filesystem and validator reports before doing any new work. Do not infer progress from the last assistant message. Completed phase reports are reusable. If a later phase times out, resume from the first phase without a durable PASS report; do not rerun earlier PASS phases by default.

## Integration invariant

For an existing Stage01–04 work being promoted to CANONICAL THICK, preserve existing Stage01–04 payloads unless a demonstrated defect requires repair. Add only the validated THICK / PlannerInput / Runtime / checkpoint / manifest payloads required for the target work. Before pointer promotion, hash-compare every predecessor file against the candidate tree.

`missing_existing == 0` and `changed_existing == 0` are required unless an explicit, enumerated migration has been approved.

## Authority-promotion invariant

Do not package a tree where physical payload coverage and current authority pointers disagree. Promotion order is:

`new authority manifest → target work manifest lineage → current THICK pointer → current Planner/Runtime pointer → nested alias pointers → integrated root pointer → bootstrap summary → release manifest`.

Then run authority-closure validation. A stale nested pointer is blocking.

## Validation invariant

Semantic generation and validation remain separate. Python may validate but must not author narrative meaning. Required promotion gates are:

- strict semantic-independence V3
- exact schema + provenance + source reference validation
- PlannerInput R5 future-leak/debt checks
- Runtime R8 parity and scene coverage
- quality-homogenization gate for a newly promoted work
- non-target immutability
- full JSON/JSONL parse
- pointer/manifest/work-manifest authority closure

## Packaging invariant

Packaging is a separate phase after prezip validation PASS. Generate checksums, build exactly one final ZIP root, run ZIP integrity test, extract into a new directory, and rerun the strong validators there. Do not update the packaged tree after the final ZIP is built; otherwise the postzip validation no longer applies to the delivered artifact.

The final postzip report is external evidence tied to the final ZIP SHA256. It must include ZIP SHA256, entry count, checksum mismatches, semantic status, exact/provenance status, and Planner/Runtime status.

## Timeout / interruption recovery

If a tool call times out:

1. Check for a still-running writer/validator process.
2. Inspect output files already written.
3. Accept a phase as complete only when its durable report parses and says PASS.
4. Resume only the missing phase.
5. Never delete or recreate the already validated working tree merely because the assistant response stopped.

For long read-only validators, run them as independent commands rather than chaining several validators plus extraction plus checksums under one timeout budget.

## Hub promotion

The hub is promoted last. Main-branch protection must be respected: branch → PR → required checks → merge. Hub metadata must record the exact final package SHA256 and fresh-extraction result. A hub pointer must never be advanced before the delivered package has postzip PASS evidence.

## Current recovery evidence — 2026-08-14

For the 그저바라보다가 24-work promotion:

- predecessor CLEAN V5 files checked: 26,494
- missing predecessor files: 0
- changed predecessor files before authority metadata promotion: 0
- CANONICAL THICK: 24 works / 3,573 records
- exact SOURCE refs: 62,905
- exact hash checks: 17,865
- PlannerInput: 24 works / 434 episode files
- Runtime: 24 works / 434 episode files / 27,438 scenes
- final ZIP entries: 26,559
- final ZIP SHA256: `b25ba041d21ab6299e92ac52b7e45dc099708019af6dcc12b97f82aa7974a9cd`
- final fresh extraction: PASS

This protocol should be read together with `DRAMA_ANALYSIS_ATOMIC_CHECKPOINT_AND_RESUME_PROTOCOL.md` and `DRAMA_ANALYSIS_NEW_WORK_EXECUTION_RUNBOOK.md`.
