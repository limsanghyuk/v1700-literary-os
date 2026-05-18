# Stage117 — NarrativeTensionCurve

Stage117 adds the Narrative Intelligence Engine's deterministic four-act tension objective on top of Stage116 Domain-Specific RAG Fusion.

## Purpose

Stage117 converts pacing into a measurable release-gate signal:

```text
T_ideal(t) = 0.60 + 0.40·sin(2πt - 0.50) + 0.20·sin(6πt)
L_final = L_tension + λ·L_coverage
```

The stage is deterministic and uses no live provider calls. It prepares Stage118 NIL Orchestrator by producing tension, coverage, and final loss evidence.

## Added components

- `src/v1700/nie/arc/narrative_tension_curve.py`
- `src/v1700/nie/arc/contracts.py`
- `src/v1700/nie/arc/coverage_loss.py`
- `src/v1700/nie/arc/tension_curve_report.py`
- `src/v1700/stage117/orchestrator.py`
- `src/v1700/gates/stage117_release_gate.py`

## Invariants

- provider default calls = 0
- live provider call count in release gate = 0
- Node2 raw reveal access = 0
- raw manuscript provider leakage = 0
- credential leakage = 0
- branchpoint lineage preserved
