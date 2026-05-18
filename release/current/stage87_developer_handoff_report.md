# Stage87 Developer Handoff Report

## Status

- Stage87 release gate: `pass`
- Main release gate: `pass`
- Provider default calls: `0`
- Node2 raw reveal access: `0`

## Scale-up Evidence

- 8-episode evidence: `8` episodes / `80` scenes
- 16-episode evidence: `16` episodes / `160` scenes
- 16-episode average quality score: `8.58`
- 16-episode min quality score: `8.39`
- Blocked direct reveal count: `7`
- Knowledge constraint count: `160`

## What Stage87 Proves

- Stage86 `SeriesArcPlanner` scales from contract smoke to 8/16 episode evidence.
- `EpisodeRevealBudget` remains active across long episode maps.
- `CharacterKnowledgeProseBridge` remains active across scene-level contracts.
- Node2 surface-only boundary remains preserved for all scale-up scene contracts.
- GitNexus/GraphNexus traceability remains optional-sidecar safe.

## Developer Commands

```bash
python -m pip install -e .
python tools/run_stage87_release_gate.py
python tools/run_symbol_to_branchpoint_trace_gate.py
python tools/run_release_gate.py
python -m pytest -q tests
```

## Next Direction

`Stage88` should add external human/editor/reader benchmark evidence against the 8-16 episode scale-up pack.

Repository root: `/mnt/data/stage87_work/gpt/active/v1700/literary_generator`

## Verification Summary

- `compileall src tools`: pass
- `pytest` split total: `84 passed`
- `pip editable install`: pass
- `python -m v1700.cli --help`: pass
- `stage87_release_gate`: pass
- `release_gate`: pass

