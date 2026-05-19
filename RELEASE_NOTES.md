# V1700 Stage130 - MultiWork Release

Stage130 seals the Stage127-129 MultiWork line into the first clean MultiWork release authority.

## Release Highlights

- Stage127 MultiWork preflight and isolation evidence remains required.
- Stage128 SharedWorld / SharedCharacter absorption remains read-only.
- Stage129 MultiWorkCIM and Cross-Work Canon Governor remain authoritative.
- Stage130 authorizes only the safe operational MultiWork surface.
- Cross-project writes, raw manuscript sharing, direct V571 trunk merge, canon auto-resolution, Gate26 hard block, active learning, and AutoRepair mutation remain blocked.

## Verification

The release workflow verifies the repository before publishing release assets:

```bash
python -m compileall -q src tools
python -m pytest tests/ -q
python tools/run_stage130_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

## Official Artifacts

Each release publishes:

- Integrated source ZIP
- ZIP SHA256 sidecar
- Current `SHA256SUMS.txt` snapshot
