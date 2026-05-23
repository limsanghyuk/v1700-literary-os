# Stage149 Integrity Repair

This note records the pre-Stage150 integrity patch.

Changed before Stage150:

- `manifests/live_core_manifest.json` restores `core_invariants`.
- `manifests/live_core_manifest.json` restores the historical `stage112` integration entry.

Follow-up for local release packaging:

- refresh generated stage lineage documentation through Stage149;
- regenerate `SHA256SUMS.txt` from `FILELIST.txt`;
- rerun metadata, asset integrity, release gate, repo doctor, and full tests.
