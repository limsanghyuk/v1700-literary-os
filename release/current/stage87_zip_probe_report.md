# Stage87 ZIP Probe Report

## Status

- ZIP path separator check: pass (`bad_backslash_count = 0`)
- Extraction root: `gpt/active/v1700/literary_generator`
- `compileall src tools`: pass
- `stage87_release_gate`: pass
- `release_gate`: pass
- Split full test suite: `84 passed`

## Split Test Suite Evidence

- Group 1: `12 passed`
- Group 2: `9 passed`
- Group 3: `17 passed`
- Group 4: `18 passed`
- Group 5: `28 passed`

Total: `84 passed`

## Boundary Invariants

- Provider default calls: `0`
- Node2 raw reveal access: `0`
- GitNexus: optional sidecar
- GraphNexus: authoritative internal graph layer
