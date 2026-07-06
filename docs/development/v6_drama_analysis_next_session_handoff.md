# V6 Drama Analysis Next Session Handoff

Date: 2026-07-06

## Start instruction

Continue the V1700 drama source analysis workflow from the V6 handoff. Read:

```text
docs/development/v6_drama_analysis_methodology.md
docs/development/v6_drama_analysis_next_session_handoff.md
```

## Current rule

Use V6 calibrated close-reading plus V1700 extension.

Do not return to earlier scaffold-only methods.

## Required process

```text
1. Read the source archive.
2. Resolve episodes using file names and archive paths before body markers.
3. Build scene boundaries from story-function changes.
4. Preserve source scene markers when available.
5. Split long source scenes only when the dramatic function changes.
6. Generate Claude-style base files.
7. Add V1700 extension folders.
8. Run parse and structure checks.
9. Compare with same-work reference when available.
10. If a reference exposes a systematic defect, repair the policy and rerun.
11. Apply the repaired policy to the target work.
12. Package the developer ZIP with reports.
```

## Required output folders

```text
authored/
authored_seq/
authored_arc/
agent_votes/
agent_votes_v1700/
arbiter/
boundary_decisions/
sequence_boundary_decisions/
eat8d/
evaluation_packets/
graph_advisory/
ledgers/
renderer_packet_bindings/
validation/
quality/
original_extracted/
```

## Calibration note

Dokkaebi is the reference calibration work. The prior defect was excessive rule-type labeling and incomplete episode handling. V6 repairs this with file-name-first episode authority and dominant-function classification.

## Transfer note

After Dokkaebi calibration, apply the repaired policy to My Girlfriend Is a Gumiho or any new drama source archive. Do not copy Dokkaebi distribution blindly.

## Integrity note

No full source text should be included in the final developer ZIP. Include extraction notes and analysis evidence only.

## Decision language

Use candidate language unless strict comparison and manual spot-check are complete.

Recommended label:

```text
DEVELOPER_READY_CANDIDATE
```
