# V1700 Branch Strategy

## Core Principles

- `main` is the single stable authority baseline.
- GitHub green on `main` is required before release authority can move.
- Merge happens before tag.
- Tag and release assets are official only after `main` is green.

## Branch Types

- `stageNNN-topic` for stage implementation or integrity repair
- `hotfix-stageNNN-topic` for release-authority repair after a sealed stage
- `docs-workflow-topic` for workflow or protocol upgrades
- temporary web-generated stage branches may exist as handoff pointers, but local Codex must finish authority closure

## Naming Rule

- use `stageNNN-topic`
- use dots only when the stage itself is a dotted hotfix authority line such as `stage172-3`

## Development Flow

1. Start from `main` or an explicitly sealed integrated package mirrored into a fresh branch.
2. Run `session_start.py` before work begins.
3. Push the branch before review.
4. Require green GitHub Actions before merge.
5. Delete the remote working branch after merge when it is no longer needed.

## Web-To-Local Handoff Rule

- keep web-generated Stage branches as staging pointers when connector limits block full payload pushes
- local Codex or Antigravity must mirror the verified ZIP or extracted authority state into the branch before PR closure
- web output is not final authority until local preflight, checksums, gates, and release assets are revalidated
