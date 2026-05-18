# Stage90 — Studio Round-trip Editing + Export Fidelity Hardening

Stage90 keeps the Stage89 Writer Studio UI/export contract and adds a deterministic interaction loop:

```text
Stage89 Studio state
  -> writer edit patch
  -> patched Studio state
  -> re-export JSON/Markdown/HTML/platform pack/scene CSV
  -> checksum and fidelity audit
  -> Stage90 release gate
```

## Purpose

Stage89 proved that the engine can create writer-facing Studio panels and export artifacts. Stage90 proves that writer-facing edits can be applied and round-tripped back into the export pipeline without breaking V1700's branchpoint invariants.

## Protected invariants

- provider default calls: `0`
- Node2 raw reveal access: `0`
- Stage89 Writer Studio contract preserved
- Stage88 AI-agent benchmark preserved
- Stage87 8/16 episode scale-up evidence preserved
- Stage86 Arc-Reveal-Knowledge preserved
- Stage85 GitNexus/GraphNexus traceability preserved

## Acceptance criteria

- At least four deterministic Studio edit operations are applied.
- JSON, Markdown, HTML, platform pack, and scene CSV artifacts are re-exported.
- Before/after artifact checksums are compared.
- Fidelity score is `10.0`.
- No forbidden raw reveal or internal markers appear in exported content.
- Stage90 release gate and main release gate pass.
