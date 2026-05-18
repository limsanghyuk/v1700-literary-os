# Mandatory Pre-Development Protocol

This protocol must be read and applied before every V1700 proposal, blueprint, roadmap, implementation, release gate change, and release package.

It is derived from the priority guide folder:

- `C:\AI_Codex\codex-work\gpt\docs\00_개발전_필수_가이드\00_GitNexus_Development_Preflight_Guide.docx`
- `C:\AI_Codex\codex-work\gpt\docs\00_개발전_필수_가이드\01_PreDevelopment_Mandatory_Checklist_GitNexus_GraphNexus_Branchpoint.docx`
- `C:\AI_Codex\codex-work\gpt\docs\00_개발전_필수_가이드\PREFLIGHT_PRIORITY_MANIFEST.json`

## Priority

This document has priority over stage-specific proposal documents. A new Stage may not be treated as complete unless its new logic is connected to tests, manifests, release evidence, branchpoint trace, release gate, repo doctor, and clean packaging.

## Required Preflight

Before development:

- Confirm GitNexus index freshness or record that Python fallback is authoritative.
- Check repository list / context / impact for the symbols or Stage being changed.
- Check GraphNexus authority: CodeGraph, NarrativeGraph, StageLineageGraph.
- Check BranchpointLogicGraph survival and symbol-to-branchpoint trace.
- Check concept impact and change review expectations.
- Check that release gate and repo doctor will recognize the new Stage.
- Check clean ZIP packaging policy before final handoff.

## Non-Negotiable Invariants

- `provider_default_calls = 0`
- `live_provider_call_count_in_release_gate = 0`
- `node2_raw_reveal_access = 0`
- `reader_only_leakage = 0`
- `internal_marker_leakage = 0`
- `raw_manuscript_provider_leakage = 0`
- `credential_leakage = 0`
- `branchpoint_lineage_preserved = true`
- `python_fallback_required = true`
- `gitnexus_runtime_dependency_required = false`

## Development Rule

Every future Stage must follow this order:

```text
1. Read mandatory pre-development protocol.
2. Run or refresh GitNexus / fallback preflight.
3. Write proposal and blueprint.
4. Define contracts, manifests, tests, release evidence, and branchpoint trace.
5. Implement in small steps.
6. Run stage-specific gate.
7. Run main release gate.
8. Run repo doctor.
9. Run tests.
10. Re-index GitNexus when code changes materially.
11. Package clean ZIP.
12. Re-extract ZIP and validate again.
```

## Stage101 Application

Stage101 applied this protocol by:

- Keeping Stage100 as the baseline gate.
- Blocking untraced V430 runtime merge.
- Recompiling scenario-room concepts as V1700-owned contracts.
- Adding Stage101 manifests, tests, release evidence, branchpoint trace, and release gate.
- Preserving provider-zero, Node2 boundary, and raw manuscript privacy.
- Refreshing GitNexus as an optional sidecar after implementation.
