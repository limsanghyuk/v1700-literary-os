# Stage109 — Plugin / Marketplace Architecture

Stage109 adds a local-first plugin and marketplace architecture on top of Stage108 External Review & Editorial Board Mode.

## Scope

- Local plugin catalog
- Plugin manifest validation
- Plugin sandbox policy
- Disabled-by-default extension loading
- Genre / evaluator / export / provider-adapter pack contracts
- Release-gate isolation for all plugins

## Invariants

- Plugins are disabled by default.
- Plugin network access is blocked by default.
- Plugins cannot access raw manuscript text.
- Plugins cannot access credentials.
- Release gates remain provider-zero.
- GitNexus runtime dependency remains optional and Python fallback remains required.
