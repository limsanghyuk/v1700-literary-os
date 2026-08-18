# Drama Close-Reading Protocol — Current Authority Index

Status: CURRENT CANDIDATE AUTHORITY
Version: 2.0
Date: 2026-07-10
Repository: limsanghyuk/v1700-literary-os

## Purpose

This index tells a new session exactly which documents define the current drama-analysis method and in what order they must be read. It supplements, and does not silently replace, the Claude Stage01~04 manual already stored in the hub.

## Mandatory reading order

1. `docs/external/claude_drama_analysis_method_manual_stage01_04_v1.md`
2. `docs/development/drama_close_reading_continuous_analysis_protocol_v2.md`
3. `docs/contracts/drama_analysis_stage01_04_release_contract_v2.md`
4. `docs/runbooks/drama_analysis_failure_recovery_and_quality_gate_v2.md`
5. `docs/development/drama_analysis_new_chat_bootstrap_v2.md`

For an existing work, also read its latest audit and manifest before opening source material.

## Authority rules

- Source text is the semantic authority for Stage01.
- Stage01 is the SSOT for Stage02.
- Stage01+02 are the evidence base for Stage03.
- Stage04 may be finalized only after all episodes are complete.
- A human-readable report never overrides machine validation or source evidence.
- A prior PASS is superseded when a stronger gate discovers a defect.
- `candidate`, `quarantine`, `pass_candidate`, and `canonical` are distinct states.
- User-facing delivery is normally a two-episode batch; internal reading remains one episode split into four quarters.

## Current reference audit

- `docs/analysis/kdrama/p101_claude_method_quality_audit_v2.md`
- The P101 audit is a negative-positive reference: Stage01/03 are strong, while Stage02 deterministic mapping and Stage04 evidence calibration demonstrate how a plausible PASS can fail a stronger gate.

## Non-negotiable boundaries

- Python may extract, hash, validate, serialize unchanged authored records, and package.
- Python may not read for meaning, derive semantic fields, expand a scene summary into other fields, or generate Stage01~04 interpretation.
- Raw scripts and dialogue are not committed to the hub.
- Every release claim must be reproducible from embedded or release-linked evidence.
