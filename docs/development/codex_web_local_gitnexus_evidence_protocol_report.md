# Codex Web-Local GitNexus Evidence Protocol Report

Status: canonical candidate  
Updated: 2026-06-16  
Scope: web planning, local execution, hub evidence promotion

## Purpose

This report defines how work should move between the web ChatGPT project, local Codex execution, and the repository hub when GitNexus or approved fallback analysis is required.

The purpose is to prevent three failures:

1. design decisions that never become recorded evidence
2. local validation that never becomes hub-readable authority
3. premature stage promotion without pushed proof

## Fixed Operating Sentence

The shared operating sentence is:

```text
Web defines.
Local proves.
Hub records.
Only recorded evidence promotes the next Stage.
```

This sentence is the shortest correct interpretation of the workflow.

## Role Separation

### Web ChatGPT project

The web project is the planning and decision surface.

It is responsible for:

- proposal and blueprint drafting
- branch and PR scope definition
- release gate interpretation
- next-stage entry decision
- reviewing pushed evidence from local Codex

The web project should not treat draft reasoning or raw terminal output as final stage authority.

### Local Codex

Local Codex is the execution and proof surface.

It is responsible for:

- checking out the target branch
- running mandatory predevelopment steps
- running GitNexus or approved fallback analysis
- converting results into repository evidence files
- updating manifests, reports, and handoff docs
- pushing the evidence back to the hub

Local Codex should not claim the next stage is promotable until the evidence is committed and pushed.

### Hub repository

The hub is the recorded authority surface.

It is responsible for:

- storing manifests and reports
- preserving lineage and branchpoint evidence
- exposing the pushed result to the next planning session
- carrying the current state across sessions and tools

## What Counts As Evidence

Running a command is not enough by itself.

Evidence exists only when the result becomes a reviewable repository artifact such as:

- `release/current/*.json`
- `release/gitnexus/<stage>/*`
- `manifests/*.json`
- `manifests/gitnexus/*.json`
- `docs/development/*.md`
- `docs/reviews/*.md`

Raw terminal output may help during execution, but it is not stage promotion authority.

## Standard Stage Flow

Every stage that depends on lineage or connectivity analysis should follow this order:

1. the web project defines the design scope, branch, PR, and intended evidence shape
2. local Codex checks out the full target branch state
3. local Codex runs preflight and GitNexus or approved fallback
4. local Codex converts the result into manifests and reports
5. local Codex pushes the evidence
6. the web project reads the pushed evidence and decides whether promotion is allowed

This means the next stage is promoted from recorded evidence, not from conversation confidence.

## GitNexus Rule

GitNexus is not merely a convenience tool.

Within this workflow it functions as lineage evidence infrastructure.

It should answer questions such as:

- which symbols, manifests, tools, and reports belong to the current stage
- whether successor traces are preserved
- whether orphan legacy logic remains
- whether branchpoint connectivity still exists
- whether a page closes without bypassing upstream authority

Expected GitNexus-backed artifacts include:

- symbol connectivity maps
- orphan reports
- successor trace matrices
- branchpoint connectivity reports
- compact stage evidence reports

## Fallback Rule

Fallback is allowed only when GitNexus is unavailable or explicitly blocked.

When fallback is used, the hub must record:

- why GitNexus was not used
- what fallback analyzer was used instead
- whether the result is advisory or promotable
- what warning must remain until fresh GitNexus evidence exists

Fallback does not automatically equal full GitNexus authority.

## Page08 Interpretation

Page08 is the clearest example of this protocol.

The correct reading is:

- the web project may seed Stage186 through Stage190
- local Codex must index the full Page08 branch state
- the resulting lineage and connectivity proof is owned by Stage186
- Stage190 consumes that evidence to decide whether Page08 can be sealed

So the repository is indexed as a whole, but the evidence is recorded under the stage that owns lineage proof.

## Required Local Command Sequence

The standard local sequence is:

```powershell
git fetch --all --tags --prune
git checkout <target-branch>
git pull --ff-only origin <target-branch>
python -m pip install -e ".[dev]"
python tools/session_start.py
python tools/run_mandatory_predevelopment_check.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
gitnexus.cmd analyze --force
gitnexus.cmd status
```

If GitNexus cannot run, the replacement path must be explicitly recorded.

## Source Authority Rule

If a canonical hub document exists, use it as the primary source.

If only a local document exists, mark it as local-only and do not silently treat it as hub authority.

If a hub document later appears, reconcile the local note with the hub source.

## Final Rule

The healthy model is not:

```text
Web builds everything.
Local merely comments.
```

The healthy model is:

```text
Web defines.
Local proves.
Hub records.
Only recorded evidence promotes the next Stage.
```
