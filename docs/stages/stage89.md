# Stage89 — Writer Studio UI + Export Pipeline

Stage89 adds a writer-facing Studio data contract and deterministic export pipeline around the Stage88 AI-agent benchmark protected engine.

## Purpose

Stage89 turns the branchpoint-governed V1700 engine into a portable writer workspace that can be exported without external provider calls.

## Core Claim

```text
Stage89 = Writer Studio UI + Export Pipeline
```

The Studio is implemented as local data panels and static export artifacts rather than a cloud-hosted UI.

## Required Panels

- Story Bible
- Episode Board
- Scene Card Board
- Character Knowledge Board
- Reveal Budget Board
- AI Agent Benchmark Panel
- Branchpoint Impact Panel
- Export Pipeline Panel

## Export Targets

- JSON Studio state
- Markdown writer handoff
- Static HTML Studio preview
- Platform serialization pack
- Scene CSV review sheet

## Blocking Conditions

- Missing required Studio panel
- Fewer than 5 export artifacts
- Missing JSON/Markdown/HTML/platform-pack/CSV export format
- Provider default calls above 0
- Node2 raw reveal access above 0
- Stage88 release gate blocked
- Symbol-to-branchpoint trace gate blocked

## Inherited Lineage

Stage89 must inherit:

- Stage88 AI-agent editor/reader benchmark
- Stage87 8/16 episode scale-up evidence
- Stage86 Arc-Reveal-Knowledge absorption
- Stage85 GitNexus/GraphNexus symbol-to-branchpoint traceability
- Stage84 V370 runtime absorption
- Stage83.1 manifest reconciliation

## Developer Commands

```bash
python -m pip install -e .
python tools/run_stage89_writer_studio.py
python tools/run_stage89_export_pipeline.py
python tools/run_stage89_release_gate.py
python tools/run_release_gate.py
python -m pytest -q tests
```
