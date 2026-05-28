# V1700 GPT Stage Development Preflight Guide V1.1

Document ID: V1700-PREFLIGHT-GPT-001  
Updated: 2026-05-28  
Applies to: all V1700 Stage development, integrity repair, release closure, workflow upgrades, and pre-design planning

## Philosophy

The `literary-os` workflow treats preflight as a mandatory session-start authority check instead of a loose best practice. V1700 adopts the same idea, but maps it to GPT-native Stage development:

- GitHub `main` is the sealed baseline
- the latest relevant tag is the last official release authority
- `session_start.py` is mandatory before planning or coding
- proposals, blueprints, and roadmaps are first-class GitHub artifacts
- release authority is `commit + tag + ZIP + .sha256 + SHA256SUMS.txt`

Passing tests alone is not enough. New logic must preserve lineage, remain visible to release gates and repo doctor, keep Provider-Zero and Privacy-Zero invariants intact, and produce clean release evidence and release assets.

## GPT Translation Of The External Workflow

The external workflow concept is translated like this inside V1700:

- `git pull + session_start.py` -> `GitHub authority + local branch + session note + mandatory predevelopment check`
- hook-based blocking -> `install_predevelopment_hooks.py` + `run_precommit_guard.py`
- docs committed before or with implementation -> `proposal + blueprint + handoff + manifest + gate evidence`
- session end push -> `session_end.py` + docs/sessions note + push before handoff

## Fixed Sequence

1. Verify latest GitHub `main`, latest Stage tag, and working branch.
2. Read `docs/development/MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md`.
3. Read the target Stage proposal and blueprint, or create them first.
4. Read the latest relevant note in `docs/sessions/`.
5. Run `python tools/session_start.py`.
6. Run `python tools/run_mandatory_predevelopment_check.py`.
7. Run `gitnexus.cmd status`; if needed, run `gitnexus.cmd analyze --force`.
8. Inspect target symbols, impact surface, manifests, and branchpoint lineage.
9. Review invariant impact on provider-zero, write-zero, privacy-zero, and release authority.
10. Implement code, tests, docs, manifests, and release evidence together.
11. Run stage-specific gates.
12. Run repository-wide gates and repo doctor.
13. Run the relevant pytest pack.
14. Re-index GitNexus after material changes.
15. Regenerate `SHA256SUMS.txt`.
16. Rebuild or verify the clean ZIP, sidecar SHA256, and release asset manifest when release authority is touched.
17. Run `python tools/session_end.py` and record the session note before handoff or closure.

## Blocking Conditions

Development stops if any of the following disagree:

- GitHub `main` versus local authority baseline
- active Stage gate versus repository-wide release gate
- repo doctor versus manifests and release evidence
- package manifest versus release asset manifest
- `FILELIST.txt` versus `SHA256SUMS.txt`
- proposal/blueprint scope versus implemented code surface
- Provider-Zero, Write-Zero, Privacy-Zero, or lineage invariants

## Required Commands

```bash
python tools/session_start.py
python tools/run_mandatory_predevelopment_check.py
python tools/run_stage184_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/regenerate_sha256sums.py
python tools/session_end.py
```

## Session-Level Rule

The same preflight applies:

- before a new proposal or blueprint is drafted
- before a new Stage implementation starts
- before an integrity repair begins
- before a release authority repair begins
