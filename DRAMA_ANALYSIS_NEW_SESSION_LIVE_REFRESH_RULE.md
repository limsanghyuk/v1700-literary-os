# Drama Analysis — New Session Live Hub Refresh Rule

A new-session bundle is a portable learning/bootstrap snapshot. It is not allowed to freeze authority forever.

## Mandatory live refresh
At the start of every new drama-analysis session, fetch from `main`:

1. `DRAMA_ANALYSIS_CURRENT_INTEGRATED_POINTER.json`
2. `DRAMA_ANALYSIS_ACTIVE_WORK_CLAIMS.json`
3. the `overlay_pointer` named by the current integrated pointer
4. `DRAMA_ANALYSIS_METHOD_CURRENT_20260814.md`
5. `DRAMA_ANALYSIS_NEW_SESSION_BOOTSTRAP.md`

If any live authority ID, work count, database filename, SHA, or active claim differs from the bundle snapshot, the live hub supersedes the bundle snapshot.

## No downgrade
Never replace a newer live THICK/Planner/Runtime authority with an older bundle authority. Historical bundle manifests remain evidence/history only after a newer live promotion.

## Concurrent GPT sessions
Multiple GPT sessions may analyze different dramas. Before selecting a target, read `DRAMA_ANALYSIS_ACTIVE_WORK_CLAIMS.json`; do not start a second writer on an ACTIVE or staging-complete-not-promoted work.

## Authority precedence
`SOURCE_AND_SOURCELOCK > ROOT_CURRENT_STAGE01_04_AUTHORITY > LIVE_CURRENT_CANONICAL_THICK > LIVE_CURRENT_DERIVED_PLANNER_RUNTIME > EXT6_APPEND_ONLY_EVIDENCE > BUNDLE_SNAPSHOT > HISTORICAL_DOCS`

## Execution model
Use Block-Atomic V2: at most 8 contiguous episodes per THICK execution block, one atomic transaction per Sequence, episode checkpoints, block strong gate, no background/late writer, and durable PASS evidence between later phases. There is no fixed per-response 3-Sequence cap.
