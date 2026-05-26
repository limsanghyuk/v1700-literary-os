# Stage168.1 — Local Evaluation Packet Store Byte-Integrity Hotfix Final Report

## Baseline

- Input package: `V1700_stage168_local_evaluation_packet_store_release_integrated_repository_with_artifacts.zip`
- Active version: `stage168`
- Hotfix target: Stage168 local evaluation packet store release package

## Problems found

1. `check_release_asset_integrity.py` blocked because `SHA256SUMS.txt` had stale digests for `AGENTS.md` and `CLAUDE.md`.
2. Standard `sha256sum -c SHA256SUMS.txt` failed for thousands of files because the ledger was not raw-byte aligned.
3. `src/v1700/gates/release_gate.py` still contained process-level release gate caching, reintroducing stale PASS risk after the Stage166.1 fix.

## Fixes applied

1. Removed main release gate process cache.
2. Updated release asset integrity checking to compare raw file bytes.
3. Regenerated `FILELIST.txt` and `SHA256SUMS.txt` after final validation and cache cleanup.
4. Updated package, live, asset, and checker canonical package names to the Stage168.1 hotfix package.
5. Added a lightweight release gate regression test proving same-process recheck behavior without expensive full-gate execution.

## Validation

```text
compileall: pass
Stage167 runner: pass
Stage167 release gate: pass
Stage168 runner: pass
Stage168 release gate: pass
main release gate: pass
metadata consistency: pass
release asset integrity: pass
Stage167+168 pytest: 12 passed
sha256sum -c SHA256SUMS.txt: pass
ZIP forbidden cache entries: 0
```

## Final decision

Stage168.1 hotfix closes the raw-byte integrity and main gate stale-cache regression for the Stage168 package.
