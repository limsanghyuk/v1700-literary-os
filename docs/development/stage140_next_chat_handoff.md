# Stage140 Next Chat Handoff — Continue Development From Here

## 1. Purpose

This document is a handoff for continuing development in a new chat session.

The previous session investigated both repositories:

```text
https://github.com/limsanghyuk/literary-os
https://github.com/limsanghyuk/v1700-literary-os
```

The agreed next direction is Stage140 for `v1700-literary-os`.

## 2. Current Repository State

### v1700-literary-os

```text
Current main baseline: Stage139 Corpus Governance Pipeline
Observed main merge commit: 43c76a7b6aeed433f69bb283f45a1b85b48490a2
README: Stage139
live_core_manifest: Stage139
package_manifest: Stage139
release_gate.py: Stage135~Stage139 registered
CI/CD: Stage134~Stage139 gates included
Known mismatch: pyproject.toml still says Stage135 / version 1.35.0
```

### literary-os

```text
Current main baseline: V586 / 9.1.0
Focus: LOSDBClient Facade + cross_query + Gate G45
README / pyproject / CHANGELOG_V586 mostly aligned
CI exists with version consistency and release gate checks
Known minor issue: CI comments/step labels still mention older V582 / 39 Gates wording
```

## 3. Why Stage140 Is Next

The next stage must not simply add another internal gate. The top problem is external trust and product proof:

1. GitHub Releases must match latest main.
2. pyproject, README, MANIFEST, package manifest, release notes, and release assets must be checked by CI.
3. The project needs real prose-generation E2E tests.
4. The project needs a sample longform benchmark pack.
5. The project needs minimum user CLI/API documentation.
6. Release gates should be split into fast/core/release layers to keep CI sustainable.

## 4. Final Expert Consensus

```text
Stage140: Release Integrity & Product Proof Gate
Stage141: Prose Generation E2E Harness
Stage142: Longform Benchmark Pack
Stage143: User CLI/API Minimum Docs
Stage144: Split CI Runtime Strategy
```

## 5. Stage140 Implementation Target

Implement:

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

src/v1700/gates/stage140_release_gate.py

tools/check_stage_metadata_consistency.py
tools/check_release_asset_integrity.py
tools/run_stage140_release_integrity.py
tools/run_stage140_release_gate.py

tests/test_stage140_release_integrity.py
```

## 6. First Fix Required

Before or during Stage140, align `pyproject.toml` with Stage139 or Stage140 policy.

Current mismatch:

```text
README: Stage139
live_core_manifest: Stage139
package_manifest: Stage139
pyproject.toml: Stage135 / 1.35.0
```

Recommended patch:

```toml
version = "1.39.0"
description = "V1700 Stage139 - Corpus Governance Pipeline"
```

If Stage140 implementation begins immediately, use:

```toml
version = "1.40.0"
description = "V1700 Stage140 - Release Integrity & Product Proof Gate"
```

## 7. Stage140 Gate Must Fail On

```text
README current stage != live_core_manifest active_version
package_manifest active_version != live_core_manifest active_version
pyproject description missing current stage
current stage release report missing
current stage release gate report missing
release asset manifest missing
CHANGELOG or RELEASE_NOTES missing for current stage
sample project contract missing
benchmark contract missing
```

## 8. Product Proof Skeleton To Add

```text
samples/korean_drama_family_secret/
  project.json
  characters.json
  world.json
  plot_outline.md
  scene_requests/scene_001.json

benchmarks/longform_output/
  README.md
  expected_metrics.json
  results/.gitkeep
```

No private manuscript or copyrighted story material should be placed in these samples. Use synthetic public-safe placeholder content.

## 9. CI/CD Target

Add metadata consistency check to CI.

Eventually split:

```text
ci-fast
ci-core
ci-release
```

But for Stage140, at minimum add:

```bash
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_stage140_release_integrity.py
python tools/run_stage140_release_gate.py
```

## 10. Files Added In This Handoff PR

```text
docs/proposals/stage140_release_integrity_product_proof_proposal.md
docs/architecture/stage140_release_integrity_product_proof_blueprint.md
docs/development/stage140_next_chat_handoff.md
```

## 11. Suggested New Chat Opening Prompt

Use this prompt in the next chat:

```text
Continue the V1700 Literary OS project from the Stage140 handoff. Use GitHub repo limsanghyuk/v1700-literary-os. Read docs/development/stage140_next_chat_handoff.md, docs/proposals/stage140_release_integrity_product_proof_proposal.md, and docs/architecture/stage140_release_integrity_product_proof_blueprint.md. Implement Stage140 Release Integrity & Product Proof Gate using the same GitHub branch/PR/CI/release workflow used for Stage135~139. Do not ask for repeated confirmations; use available GitHub tools. Start by fixing pyproject metadata mismatch and adding metadata consistency checks.
```
