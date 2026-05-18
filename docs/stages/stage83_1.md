# Stage83.1 — Consistency Audit & Manifest Reconciliation

Stage83.1 is the required reconciliation stage between the Stage83 commercial longform release candidate and Stage84 runtime absorption.

## Purpose

- Rebuild stale Stage75 / Stage81.1 manifests through Stage83.
- Add Stage80~83 branchpoints to the branchpoint model registry.
- Rebuild the organic relation graph from the reconciled survival matrix.
- Remove Stage82/83 commercial-readiness `PENDING` statuses after Stage82/83 evidence exists.
- Add the GitNexus → GraphNexus → BranchpointLogicGraph bridge manifest.
- Prevent relation edges from rendering as `None → None`.

## Gate

```bash
python tools/run_stage83_1_release_gate.py
```

Expected result: `status = pass`, `provider_default_calls = 0`, `node2_raw_reveal_access_count = 0`.
