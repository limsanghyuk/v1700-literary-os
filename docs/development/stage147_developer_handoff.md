# Stage147 Developer Handoff

## Stage

- Stage147 - Project Manifest Body
- Baseline: Stage146 Narrative State Contract
- Next: Stage148 Node Boundary Constitution

## Main Files

- `src/v1700/project_manifest_body/contracts.py`
- `src/v1700/project_manifest_body/loader.py`
- `src/v1700/project_manifest_body/report.py`
- `src/v1700/stage147/stage147_runner.py`
- `src/v1700/gates/stage147_release_gate.py`
- `tools/run_stage147_project_manifest_body.py`
- `tools/run_stage147_release_gate.py`

## Evidence Pack

- `release/current/stage147_project_manifest_body_pack/canonical_manifest_bundle.json`
- `release/current/stage147_project_manifest_body_pack/project_manifest_catalog.json`
- `release/current/stage147_project_manifest_body_pack/manifest_state_bindings.json`
- `release/current/stage147_project_manifest_body_pack/manifest_policy_boundary.json`
- `release/current/stage147_project_manifest_body_pack/manifest_load_order.json`
- `release/current/stage147_project_manifest_body_pack/stage148_entry_signals.json`

## Validation Order

```text
1. mandatory predevelopment check
2. stage metadata consistency
3. release asset integrity
4. Stage147 project manifest body report
5. Stage147 release gate
6. main release gate
7. repo doctor
8. active-lineage pytest pack
9. GitNexus refresh
10. clean ZIP packaging
```

## Important Constraints

- sample files remain synthetic only
- provider calls remain zero
- raw manuscript inclusion remains false
- Node2 raw reveal access remains zero
- Stage148 must enforce boundaries on top of these packets rather than replacing them
