# GitNexus Optional Sidecar

GitNexus is treated as a developer-side CodeGraph sidecar. It may be installed once in a developer environment, but the V1700 runtime and release gate must pass without it.

Required behavior:

- GitNexus installed: probe can report the available command.
- GitNexus missing: Python fallback remains available.
- Provider calls: `0`.
- Runtime dependency: `false`.
- `.gitnexus/` should not be committed.

On Windows PowerShell, prefer `npm.cmd` and `npx.cmd` when script execution policy blocks `npm.ps1`.
