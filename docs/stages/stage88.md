# Stage88 — AI-Agent Editor/Reader Blind Benchmark

Stage88 replaces the planned external human editor/reader benchmark with a deterministic local AI-agent benchmark, per user direction.

## Purpose

Stage88 validates Stage87 8/16 episode scale-up evidence through role-separated artificial reviewer agents instead of external human editors/readers.

## Core Claim

```text
Stage88 = Local AI-Agent Blind Benchmark over Stage87 Scale-up Evidence
```

The benchmark remains local-first and does not introduce default provider calls.

## Agent Panel

- Senior Korean drama editor agent
- Commercial serialization platform editor agent
- Continuity and script logic editor agent
- Korean longform genre reader agent
- AI-scent and prose surface detector agent
- Skeptical binge reader agent

## Blocking Conditions

- Agent panel below 6 agents
- Blind sample count below 16 samples
- Consensus score below 8.0
- Minimum agent average below 8.0
- Minimum sample average below 8.0
- Provider default calls above 0
- Node2 raw reveal access above 0

## Inherited Lineage

Stage88 must inherit:

- Stage87 8/16 episode scale-up evidence
- Stage86 Arc-Reveal-Knowledge absorption
- Stage85 GitNexus/GraphNexus symbol-to-branchpoint traceability
- Stage84 V370 runtime absorption
- Stage83.1 manifest reconciliation

## Developer Commands

```bash
python -m pip install -e .
python tools/run_stage88_agent_benchmark.py
python tools/run_stage88_release_gate.py
python tools/run_release_gate.py
python -m pytest -q tests
```
