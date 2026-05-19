# V1700 Stage133 - NarrativeStateTensor 8D Measurement Layer

Stage133 measures Stage132 contradiction classifications through a deterministic, local-only 8D NarrativeStateTensor.

## Release Highlights

- Stage127 MultiWork preflight and isolation evidence remains required.
- Stage128 SharedWorld / SharedCharacter absorption remains read-only.
- Stage129 MultiWorkCIM and Cross-Work Canon Governor remain authoritative.
- Stage130 authorizes only the safe operational MultiWork surface.
- Stage131 distinguishes true contradiction, intentional mystery, character misunderstanding, and reveal delay.
- Stage132 adds evidence-based classification for true contradiction, intentional mystery, POV misunderstanding, reveal delay, and no-conflict cases.
- Stage133 measures the classified cases across causality, temporal continuity, reveal budget, character agency, emotional momentum, voice stability, attention economy, and canon isolation.
- Mystery exemption requires a reveal lock and payoff budget.
- True contradictions are measured as review-required states instead of being auto-fixed.
- Gate26 hard block, canon auto-resolution, AutoRepair mutation, and cross-project writes remain disabled.
- Cross-project writes, raw manuscript sharing, direct V571 trunk merge, canon auto-resolution, Gate26 hard block, active learning, and AutoRepair mutation remain blocked.

## Verification

The release workflow verifies the repository before publishing release assets:

```bash
python -m compileall -q src tools
python -m pytest tests/ -q
python tools/run_stage133_narrative_state_tensor.py
python tools/run_stage133_release_gate.py
python tools/run_stage130_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

## Official Artifacts

Each release publishes:

- Integrated source ZIP
- ZIP SHA256 sidecar
- Current `SHA256SUMS.txt` snapshot
