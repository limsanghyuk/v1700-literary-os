# V1700 Stage Development Preflight Guide V1.1

Document ID: V1700-PREFLIGHT-001  
Updated: 2026-05-25  
Applies to: all V1700 Stage development, integrity repair, release closure, and workflow upgrades

## Philosophy

Passing tests alone is not enough. New logic must preserve lineage, remain visible to release gates and repo doctor, keep provider-zero and privacy-zero invariants intact, and produce clean release evidence and release assets.

## Fixed Sequence

1. Confirm repository state, latest main, active stage, and latest tag.
2. Confirm working context by reading the mandatory protocol, proposal, blueprint, and relevant session notes.
3. Run `python tools/run_mandatory_predevelopment_check.py`.
4. Refresh GitNexus or record Python fallback.
5. Inspect target scope, symbols, process, manifest, and release evidence.
6. Review invariant impact.
7. Confirm design artifacts first.
8. Confirm implementation surfaces: source, tests, manifests, release reports, release gate, repo doctor, package manifest, checksums.
9. Implement in small steps.
10. Run the stage-specific gate.
11. Run repository-wide gates.
12. Run the relevant pytest pack.
13. Re-index after material changes.
14. Build release authority artifacts: canonical ZIP, `.sha256`, and `SHA256SUMS.txt`.
15. Re-verify extracted release state.

## Blocking Conditions

Development stops if stage gate, main release gate, repo doctor, CI, docs/manifests, ZIP/sidecar, or release assets disagree.
