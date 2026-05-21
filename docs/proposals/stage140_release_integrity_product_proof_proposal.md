# Stage140 Proposal — Release Integrity & Product Proof Gate

## 1. Executive Summary

Stage140 should become the next evolution point after Stage139 Corpus Governance Pipeline.

The immediate priority is not another internal model layer. The current risk is external trust: release assets, metadata, package descriptors, README, manifests, and CI/CD evidence must all point to the same active stage. After that, the project must prove product value through actual prose-generation E2E and longform benchmark artifacts.

## 2. Expert Consensus

### Chief Architect

The architecture is strong through Stage139, but the external release surface is still fragile. Stage140 must create one authoritative release integrity layer that binds the following:

- README current stage
- pyproject version and description
- live_core_manifest active_version
- package_manifest active_version and canonical package
- release/current stage reports
- GitHub Release tag and assets
- CHANGELOG or release notes

The architect recommends Stage140 as a release-integrity gate before Stage141 prose E2E.

### Chief Compiler

The compiler view found a clear mismatch: `v1700-literary-os` main is Stage139, but `pyproject.toml` still records Stage135. This must become a CI-blocking failure. The compiler recommends a deterministic metadata consistency checker under `tools/` and a test file that fails if README, pyproject, manifests, package manifest, and release evidence diverge.

### Chief System Principal Engineer

The principal engineer agrees that release trust comes first. However, the next strategic risk is that the system remains gate-heavy but product-light. Stage140 should therefore include product-proof preparation: define the sample project layout, E2E prose-generation contract, benchmark output directory, and release asset verification. Actual prose-generation execution can become Stage141, but Stage140 must make the proof path unavoidable.

## 3. Current Repository Findings

### v1700-literary-os

Current main is Stage139.

- README: Stage139
- live_core_manifest: Stage139
- package_manifest: Stage139
- pyproject: still Stage135
- CI: Stage134~139 gates are executed
- release.yml: builds ZIP/SHA256 on version tags
- missing: strict metadata consistency CI
- missing: visible prose-generation E2E product proof
- missing: public longform benchmark pack

### literary-os

Current main is V586 / 9.1.0.

- README, pyproject, CHANGELOG_V586 are mostly aligned
- release workflow exists
- CI contains version consistency and release gate checks
- some CI comments/step names still reference older V582 / 39 gates wording
- missing: public prose-generation E2E and longform benchmark proof

## 4. Stage140 Goals

Stage140 must provide:

1. Release asset integrity check
2. Metadata consistency check
3. Package and manifest alignment check
4. CHANGELOG / release notes requirement
5. CI blocking for mismatched stage/version metadata
6. Product proof path definition for Stage141
7. Release gate splitting plan for long-term CI sustainability

## 5. Non-Goals

Stage140 should not activate real training, active learning, LOSDB writes, migration execution, provider calls, or canon mutation. It should not attempt full prose benchmark scoring yet. Those belong after metadata and release integrity are stable.

## 6. Proposed New Components

```text
src/v1700/release_integrity/
  contracts.py
  checker.py
  report.py

src/v1700/product_proof/
  contracts.py
  sample_project_contract.py

tools/check_stage_metadata_consistency.py
tools/check_release_asset_integrity.py
tools/run_stage140_release_integrity.py
tools/run_stage140_release_gate.py

tests/test_stage140_release_integrity.py
```

## 7. Required CI Rules

CI should fail if:

- README current stage differs from live_core_manifest active_version
- pyproject description differs from current stage
- package_manifest active_version differs from live_core_manifest active_version
- current stage release report is missing
- current stage release gate report is missing
- release asset manifest is missing
- CHANGELOG or RELEASE_NOTES for current stage is missing
- GitHub Release asset names do not match package_manifest canonical package

## 8. Product Proof Path

Stage140 should define, but not yet fully score, the following structure:

```text
samples/korean_drama_family_secret/
  project.json
  characters.json
  world.json
  plot_outline.md
  scene_requests/scene_001.json

benchmarks/longform_output/
  README.md
  run_benchmark.py
  expected_metrics.json
  results/.gitkeep
```

Stage141 should then implement actual prose generation E2E using this structure.

## 9. Final Recommendation

Proceed with Stage140 as `Release Integrity & Product Proof Gate`, then Stage141 as `Prose Generation E2E Harness`, Stage142 as `Longform Benchmark Pack`, Stage143 as `User CLI/API Minimum Docs`, and Stage144 as `Split CI Runtime Strategy`.
