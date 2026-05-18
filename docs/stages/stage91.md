# Stage91 — Studio Persistence + Review Queue + UI Event Replay

Stage91 turns the Stage90 static round-trip Studio into a deterministic interaction contract.

It adds:

- Writer Studio persistence snapshots with checksums
- Branchpoint-aware review queue state
- Replayable UI event logs
- Stage91 release gate
- Stage91 symbol-to-branchpoint trace entries

Stage91 is intentionally still local and deterministic. It does not add a browser runtime, database server, external provider call, or raw reveal authority.

```text
Stage90 patched Studio workspace
  -> Stage91 persistence snapshot
  -> UI event replay
  -> review queue transitions
  -> edit events
  -> snapshot checksums
  -> release gate
```

## Invariants

- provider default calls: `0`
- Node2 raw reveal access: `0`
- GitNexus remains optional sidecar
- GraphNexus remains internal authority
- Stage90 export fidelity is preserved

## Acceptance

- at least 18 UI events replayed
- at least 3 persistence snapshots
- at least 6 review queue items
- blocking reviews resolved
- deterministic replay checksum
- `stage91_release_gate` pass
