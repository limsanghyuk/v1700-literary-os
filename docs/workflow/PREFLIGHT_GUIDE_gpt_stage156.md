# GPT-Native GitNexus Preflight Guide — Stage156 Supplement

This supplement adapts the Claude-Native `PREFLIGHT_GUIDE_v1.1.md` / v2.0 direction into the GPT execution environment used for V1700 Stage156.

## Source influence

The referenced guide keeps the original GitNexus objective but reinterprets it for Claude tools. Its most important upgrade is that Step 15 becomes a combined hygiene, survival, and connectivity gate. Stage156 adopts that principle in GPT form.

## GPT-specific application

1. Use hub search and file fetch to confirm current branch, PR, and docs state.
2. Use local package inspection when direct clone is unavailable.
3. Convert every new stage into five linked surfaces: code, tests, tools, manifests, and release/current evidence.
4. Treat orphan modules as release blockers. A new module must be referenced by a runner, gate, test, manifest, and stage doc.
5. Treat clean packaging as a gate. `.pytest_cache`, `__pycache__`, and transient artifacts must not enter the release ZIP.
6. Keep provider-zero, write-zero, Node2 surface-only, and no runtime training as non-negotiable invariants.

## Stage156 mandatory preflight extension

Before Stage156 development, verify:

- Stage155 release gate exists and passes.
- Page03 Execution Contract artifacts exist.
- Local execution packet store path is read-only JSONL.
- Packet checksums are deterministic and reproducible.
- Store loader performs validation without writing.
- Stage156 gate is registered in main release gate and live manifest.
- Metadata checker and asset checker know Stage156.
- Full package contains no cache files.

## Decision rule

Stage156 can pass only if the local packet store is deterministic, read-only, checksum-indexed, Node2-safe, and fully connected to gates and manifests.
