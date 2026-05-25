# GPT-Native GitNexus Preflight Guide — Stage158 Supplement

This supplement applies the Claude-Native GitNexus Step15 v2.0 principle to the GPT/web development workflow.

## Adopted principle

A stage is not complete merely because its unit tests pass. It must remain connected to modules, tools, tests, manifests, release/current evidence, and the main release gate. Hygiene, survival, and connectivity are a single preflight concern.

## Stage158 mandatory checks

1. Confirm Stage157 release gate passes.
2. Confirm new package, runner, gate, tools, tests, docs, manifests, and release evidence exist.
3. Confirm dependency order preflight produces zero blockers.
4. Confirm conflict matrix produces zero forbidden packet conflicts.
5. Confirm Node2 projection matrix has zero hidden/raw/provider/write token leaks.
6. Confirm blocked operations remain disabled.
7. Confirm clean ZIP has no `.pytest_cache`, `__pycache__`, or `.pyc` artifacts.
8. Confirm Stage150~158 targeted regression passes.

## GPT-specific fallback

When direct GitHub clone or bulk push is blocked, the canonical artifact is the verified integrated repository ZIP plus SHA256 sidecar, and Antigravity mirrors it into the hub.
