# V1700 Branch Strategy And Release Workflow

> Baseline: Stage160 | Updated: 2026-05-25

## Core Principles

```text
GitHub main = latest stable baseline
CI green    = only merge authority
Stage tag   = official version marker
ZIP + SHA   = official delivery artifact
```

## Branch Structure

```text
main
  |- stageNNN-topic
  |- hotfix-stageNNN-topic
  `- workflow-topic
```

Recommended branch names:

- `stage161-memory-body`
- `stage149-integrity-repair`
- `workflow-v11-stage-preflight-upgrade`

## Development To Release Flow

```text
1. Create a branch from main.
2. Run the mandatory predevelopment protocol.
3. Implement and validate locally.
4. Push the branch and wait for GitHub Actions.
5. Open a PR after CI turns green or when review is needed for the remaining fixes.
6. Merge to main only after required checks pass.
7. Create and push the Stage tag from merged main.
8. Publish the GitHub Release with canonical assets.
9. Verify the release ZIP, .sha256, and SHA256SUMS.txt.
```

## Required CI Checks

The exact workflow names may evolve, but the following categories must stay green:

- fast CI
- core CI
- release dry-run
- tag release workflow when a tag is created

If a branch changes gates, manifests, packaging, or release workflows, merge is blocked until all relevant CI checks pass.

## Release Assets

Every official Stage release must provide:

1. canonical release ZIP
2. canonical `.sha256` sidecar
3. `SHA256SUMS.txt`

The sidecar is the direct authority for the shipped ZIP. `SHA256SUMS.txt` is the repository-wide release ledger.

## Version Alignment

Before merge or release, confirm alignment across:

- `README.md`
- `CHANGELOG.md`
- `package_manifest.json`
- `manifests/live_core_manifest.json`
- stage-specific manifests and release reports
- release tag and release title

## Hotfix Rule

Hotfixes follow the same flow with the smallest safe scope:

```text
1. branch from main
2. run preflight
3. make the minimal repair
4. re-run local and CI validation
5. merge
6. publish the corrective tag and release if needed
```
