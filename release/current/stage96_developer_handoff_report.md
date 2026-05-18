# Stage96 Developer Handoff

Stage96 integrates Narrative Physics Optimization, Manuscript Learning, and Provider Ensemble Arbitration.

## Runtime Boundary

- Release gates use dry-run fixture candidates only.
- Raw manuscript text remains local and is reduced to feature summaries.
- Provider candidates are inputs; V1700 Narrative Physics remains the authority.
- Merge output is directive-level, never provider text concatenation.

## Evidence

- Stage96 gate: `pass`
- Provider calls: `0`
- Node2 raw reveal access: `0`

## Commands

```bash
python tools/run_stage96_narrative_optimization.py
python tools/run_stage96_manuscript_learning.py
python tools/run_stage96_provider_ensemble.py
python tools/run_stage96_release_gate.py
python tools/run_release_gate.py
```
