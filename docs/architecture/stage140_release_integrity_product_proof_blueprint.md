# Stage140 Blueprint — Release Integrity & Product Proof Gate

## 1. Baseline

Stage140 starts from `v1700-literary-os` main after Stage139.

```text
Current active baseline: Stage139 Corpus Governance Pipeline
Main commit observed: 43c76a7b6aeed433f69bb283f45a1b85b48490a2
Next proposed stage: Stage140 Release Integrity & Product Proof Gate
```

## 2. Design Principle

Stage140 is a trust layer, not a generation layer. It blocks releases when repository metadata and GitHub release assets disagree. It also creates the contract for Stage141 prose-generation E2E.

## 3. Architecture

```text
Stage139 Corpus Governance Pipeline
        |
        v
Stage140 Release Integrity & Product Proof Gate
        |
        +-- metadata consistency checker
        +-- release asset integrity checker
        +-- package manifest validator
        +-- release notes / changelog validator
        +-- sample project contract validator
        +-- benchmark contract validator
        v
Stage141 Prose Generation E2E Harness
```

## 4. New Modules

```text
src/v1700/release_integrity/
  __init__.py
  contracts.py
  metadata_checker.py
  asset_checker.py
  report.py

src/v1700/product_proof/
  __init__.py
  contracts.py
  sample_project_contract.py
  benchmark_contract.py

src/v1700/stage140/
  __init__.py
  stage140_runner.py

src/v1700/gates/
  stage140_release_gate.py
```

## 5. Tools

```text
tools/check_stage_metadata_consistency.py
tools/check_release_asset_integrity.py
tools/run_stage140_release_integrity.py
tools/run_stage140_release_gate.py
```

## 6. Tests

```text
tests/test_stage140_release_integrity.py
```

Required assertions:

```text
README current stage == live_core_manifest active_version
package_manifest active_version == live_core_manifest active_version
pyproject description contains current stage
pyproject version maps to current stage
current stage release report exists
current stage release gate report exists
release asset manifest exists
CHANGELOG or RELEASE_NOTES exists for current stage
sample project contract files exist
benchmark contract files exist
release gate status == pass
```

## 7. Metadata Consistency Contract

The checker should produce:

```json
{
  "stage": "140",
  "baseline_stage": "139",
  "status": "pass",
  "current_stage": "stage139",
  "metadata": {
    "readme_stage": "stage139",
    "live_manifest_stage": "stage139",
    "package_manifest_stage": "stage139",
    "pyproject_stage": "stage139"
  },
  "issues": []
}
```

Any mismatch must create a blocking issue.

## 8. Release Asset Integrity Contract

The checker should compare:

```text
package_manifest.canonical_package
package_manifest.sha256_sidecar
release/current/stageXXX_release_asset_manifest.json
GitHub Release tag and asset names if available
```

The GitHub API check may be optional in local mode, but CI should at least validate repository-side manifests and expected asset names.

## 9. Product Proof Contract

Stage140 should add minimal sample and benchmark skeletons:

```text
samples/korean_drama_family_secret/project.json
samples/korean_drama_family_secret/characters.json
samples/korean_drama_family_secret/world.json
samples/korean_drama_family_secret/plot_outline.md
samples/korean_drama_family_secret/scene_requests/scene_001.json

benchmarks/longform_output/README.md
benchmarks/longform_output/expected_metrics.json
benchmarks/longform_output/results/.gitkeep
```

Stage141 will use these to run real prose-generation E2E.

## 10. CI Split Plan

```text
ci-fast:
  compileall
  metadata consistency
  current stage targeted tests
  current stage gate

ci-core:
  full pytest
  active lineage release gate
  repo doctor

ci-release:
  full pytest
  full Stage134~current gates
  package ZIP/SHA256
  release asset validation
```

## 11. Release Gate Criteria

Stage140 release gate passes only if:

- Stage139 baseline gate passes
- metadata consistency passes
- release asset manifest consistency passes
- package manifest consistency passes
- changelog/release note presence passes
- sample project contract passes
- benchmark contract passes
- provider calls remain zero
- migration execution remains blocked
- LOSDB writes remain blocked
- runtime training remains disabled
- branchpoint lineage remains preserved

## 12. Deliverables

```text
docs/proposals/stage140_release_integrity_product_proof_proposal.md
docs/architecture/stage140_release_integrity_product_proof_blueprint.md
docs/development/stage140_next_chat_handoff.md
manifests/stage140_manifest.json
release/current/stage140_release_integrity_report.json
release/current/stage140_release_gate_report.json
```
