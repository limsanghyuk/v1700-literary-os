# Stage135 Release Asset Correction

## Status

The `v1700-stage135` GitHub Release exists and points at commit `9051c36a9007f0b10d5fb0740722304b8b57ba9b`.

The visible Release assets must be corrected because the current asset list still shows Stage133 files.

## Remove these assets

```text
SHA256SUMS_v1.33.0-stage133.txt
V1700_v1.33.0-stage133_integrated_repository.zip
V1700_v1.33.0-stage133_integrated_repository.zip.sha256
```

## Upload these Stage135 assets

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

The ChatGPT GitHub connector can create branches, commits, PRs, and merge PRs, but it does not expose a GitHub Release asset upload endpoint. Therefore the asset upload must be done from the GitHub Release edit page or GitHub CLI.
