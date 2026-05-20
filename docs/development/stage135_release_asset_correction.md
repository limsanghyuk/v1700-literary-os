# Stage135 Release Asset Correction

## Status

The `v1700-stage135` GitHub Release points at commit `9051c36a9007f0b10d5fb0740722304b8b57ba9b`.

The current Release page is closer to correct than the original Stage133 mispublish, but it still does not match the official Stage135 handoff archive:

- the visible assets are workflow-generated generic tag assets
- the release body still describes Stage133

## Current assets to replace

```text
SHA256SUMS_v1700-stage135.txt
V1700_v1700-stage135_integrated_repository.zip
V1700_v1700-stage135_integrated_repository.zip.sha256
```

## Official Stage135 assets to upload

```text
V1700_stage135_learning_quality_gate_release_integrated_repository_with_artifacts.zip
V1700_stage135_learning_quality_gate_release_integrated_repository_with_artifacts.zip.sha256
```

## Expected SHA256

```text
1a19105099454a59b39cb04e919dddd455393fed6058760d9b8aae3273891335
```

## Verified before release

```text
ci-core / gitnexus-and-ci-preflight: success
ci-core / pytest-and-gates Python 3.11: success
ci-core / pytest-and-gates Python 3.12: success
cd-dry-run / build-release-archive-dry-run: success
```

## Note

The repository now records the correct Stage135 release notes and asset metadata, but GitHub Release asset upload still requires the GitHub Release edit page, GitHub CLI, or authenticated API access.
