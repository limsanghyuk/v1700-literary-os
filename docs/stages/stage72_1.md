# STAGE72.1: GraphNexus Restoration Patch

## Problem

Stage72 canonicalized the repository and preserved Stage61-66 graph intelligence as concise lineage knowledge, but the live core did not yet expose a working optional graph architecture.

## Implemented

- `CodeGraph`, `NarrativeGraph`, and `StageLineageGraph` under `src/v1700/graph_nexus`.
- GitNexus optional sidecar probe under `src/v1700/sidecars/gitnexus`.
- Python fallback graph construction that passes without GitNexus installed.
- Lineage, impact, legacy survival, node projection, and GraphNexus release gates.
- Node2 graph projection limited to `Node2GraphSurfacePacket`.
- Stage72 release gate integration and release evidence script.

## Runtime Policy

GitNexus is not vendored into this repository. It is an external CLI/MCP sidecar and should be installed on the developer machine, not copied into `src`.

If GitNexus is not installed, Stage72.1 uses deterministic Python fallback graph analysis. This keeps the release gate runnable on clean machines, while still allowing GitNexus to provide deeper graph indexing when installed.

See `docs/runbooks/gitnexus_installation_policy.md`.

## Verification

Run:

```bash
python -m pytest -q tests
python tools/run_graph_nexus_release_gate.py
python tools/run_release_gate.py
```
