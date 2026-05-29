# Codex / Web Hub Stage Development Operating Report

Status: operating report for local Codex and web-hub cooperative development
Created: 2026-05-29
Applies to: V1700 Page08~Page17 roadmap and all future stages after Page08
Current active branch: stage186-page08-branchpoint-map
Current active page: Page08 — Lineage / Hub / Formula Authority

## 1. Executive summary

The intended operating model is correct:

```text
The web project continues the repository-side development.
Local Codex runs GitNexus, stage preflight, and environment-specific checks.
Local Codex commits the resulting evidence back to the hub.
The web project reads those pushed results and uses them to design and implement the next stage.
```

This process is necessary because local Codex usage limits can slow full implementation, while the web project can still create and maintain repository documents, manifests, reports, PRs, and hub-side workflows. Local Codex should therefore be used for the parts that the web project cannot reliably execute directly, especially GitNexus indexing and local preflight evidence.

## 2. Core principle

Before every new stage, local Codex must refresh the repository understanding and push evidence.

```text
No fresh index, no next-stage authority.
No preflight evidence, no stage promotion.
No pushed result, no web-side continuation.
```

This does not mean every stage must be blocked forever if GitNexus is unavailable. It means the absence of GitNexus must be explicitly recorded, and an approved fallback or exception must be documented before the next stage is treated as valid.

## 3. Role separation

### 3.1 Web project role

The web project is responsible for:

```text
1. drafting proposals and blueprints
2. creating or updating manifests
3. creating release/current report seeds
4. creating GitHub branches and PRs
5. adding workflow hooks where possible
6. reading pushed Codex/GitNexus results
7. analyzing the results
8. deciding the next stage design
9. implementing hub-side stage artifacts
10. preserving roadmap and release authority
```

### 3.2 Local Codex role

Local Codex is responsible for:

```text
1. reading the current active stage guide
2. loading dev_protocol_v3.0 if present in the local environment
3. loading workflow/preflight_guide_v1.1 if present in the local environment
4. running mandatory predevelopment checks
5. running GitNexus indexing / analysis
6. running local-only validation that the web project cannot execute
7. updating evidence reports and connectivity manifests
8. committing and pushing those results to the active stage branch
```

### 3.3 Developer role

The developer is responsible for:

```text
1. ensuring local tools exist and are on PATH
2. confirming GitNexus command names for the local environment
3. reviewing any fallback evidence before it is treated as approved
4. refusing next-stage promotion if local evidence contradicts branchpoint or inheritance manifests
```

## 4. Required protocol documents

Local Codex must learn and apply these documents before each stage when they exist locally:

```text
dev_protocol_v3.0
workflow/preflight_guide_v1.1
```

At the time this report was written, the exact filenames were not found in the hub code search. Therefore:

```text
1. If these files exist only in the local environment, local Codex must read them first.
2. If they are approved as canonical, they should be copied or linked into the repository.
3. Recommended repository targets are:
   docs/development/dev_protocol_v3.0.md
   docs/workflow/preflight_guide_v1.1.md
```

Until those canonical copies exist, every local Codex report must state whether it loaded them from local-only sources or could not find them.

## 5. Standard per-stage loop

Every future stage should follow this loop.

### Step 1 — Web creates or updates stage branch

Example:

```bash
git fetch --all --tags --prune
git checkout <active-stage-branch>
git pull --ff-only origin <active-stage-branch>
```

### Step 2 — Local Codex reads required documents

For Page08 this currently means:

```text
docs/roadmaps/page08_page17_commercial_absorption_writer_studio_roadmap.md
docs/roadmaps/page08_page17_codex_ide_absorption_addendum.md
docs/roadmaps/page08_page17_page_blueprint_drafts.md
docs/proposals/page08_lineage_hub_formula_authority_proposal.md
docs/architecture/page08_lineage_hub_formula_authority_blueprint.md
docs/development/page08_codex_local_execution_guide.md
docs/development/page08_pre_page09_local_execution_guide.md
```

For later stages, the corresponding page/stage guide must be read in the same way.

### Step 3 — Local Codex applies protocol documents

Local Codex must load:

```text
dev_protocol_v3.0
workflow/preflight_guide_v1.1
```

If unavailable:

```text
record: PROTOCOL_FILE_NOT_FOUND
record where it searched
record whether developer approved continuation
```

### Step 4 — Local Codex runs baseline checks

The baseline command set should include:

```bash
python tools/session_start.py
python tools/run_mandatory_predevelopment_check.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_stage184_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

If a command is missing, local Codex must report it rather than hiding it.

### Step 5 — Local Codex runs GitNexus

Preferred commands:

```bash
gitnexus.cmd analyze --force
gitnexus.cmd status
```

Alternative commands:

```bash
gitnexus analyze --force
gitnexus status
```

If GitNexus is unavailable, local Codex must not mark GitNexus evidence as passed. It must record one of:

```text
GITNEXUS_NOT_AVAILABLE
GITNEXUS_FAILED
APPROVED_FALLBACK_USED
```

### Step 6 — Local Codex updates evidence artifacts

For Page08, the required files are:

```text
release/current/stage186_gitnexus_lineage_connectivity_report.json
manifests/stage186_symbol_to_branchpoint_connectivity.json
manifests/stage186_orphan_legacy_symbol_report.json
manifests/stage186_successor_trace_matrix.json
release/current/stage186_branchpoint_map_report.json
release/current/stage190_page08_release_seal_report.json
release/current/page08_release_gate_report.json
```

For later stages, the stage-specific guide must define equivalent evidence files.

### Step 7 — Local Codex commits and pushes

Example:

```bash
git add <updated-evidence-files>
git commit -m "Apply local preflight and GitNexus evidence for <StageXXX>"
git push origin <active-stage-branch>
```

### Step 8 — Web project reads pushed results

After local push, the web project must:

```text
1. inspect changed evidence files
2. verify whether reports are PASS / PASS_WITH_WARNINGS / FAIL
3. verify whether any orphan or disconnected lineage exists
4. update the current stage report if needed
5. decide whether the next stage may begin
```

## 6. Stage promotion rules

A stage may advance only when:

```text
1. stage proposal or blueprint exists
2. stage manifest exists
3. stage report exists
4. required local preflight has been run or explicitly waived
5. GitNexus or approved fallback evidence has been applied when required
6. hub Actions are checked
7. next-stage blockers are resolved or explicitly carried forward
```

A stage must not advance when:

```text
1. local evidence contradicts the manifest
2. GitNexus finds orphan lineage with no successor trace
3. Stage185 local-known evidence is promoted to hub-official without closure
4. Page09 starts before Page08 release gate allows it
5. advisory literary scores are treated as hard quality gates without later promotion record
6. StoryPatch or runtime write behavior appears before approval contracts exist
```

## 7. Page08-specific state

Current Page08 range:

```text
Stage186 — Branchpoint Map Builder
Stage187 — Inheritance Contract Gate
Stage188 — Hub Authority Reconciliation
Stage189 — Formula / Logic Ledger v2
Stage190 — Page08 Release Seal
```

Current PR:

```text
PR #57 — Implement Stage186 Page08 Branchpoint Map Builder
branch: stage186-page08-branchpoint-map
```

Current Page08 condition:

```text
Stage186~Stage189 seed implementation exists.
Stage190 report exists.
Page08 release gate is intentionally blocked until local GitNexus or approved fallback evidence is pushed.
Page09 entry is not allowed yet.
```

## 8. Local Codex instruction for Page08

Use this exact task instruction for local Codex before Page09:

```text
Continue V1700 Page08 from branch stage186-page08-branchpoint-map. Read docs/development/codex_web_hub_stage_development_operating_report.md, docs/development/page08_pre_page09_local_execution_guide.md, and all Page08 proposal/blueprint documents. Load dev_protocol_v3.0 and workflow/preflight_guide_v1.1 if available in the local environment. Run the mandatory predevelopment checks. Run GitNexus indexing and status. Update Stage186 connectivity, orphan legacy symbol, successor trace, Stage186 report, Stage190 report, and Page08 release gate report. Push the updated evidence to the hub. Do not start Page09. Do not implement Story Patch, EAT8D extraction, Narrative PR, Narrative IDE, MultiWork, plugin, or learning. The only goal is to convert Page08 from BLOCKED_PENDING_LOCAL_GITNEXUS_OR_APPROVED_FALLBACK to PASS or PASS_WITH_WARNINGS if the evidence supports it.
```

## 9. Web project instruction after local push

After local Codex pushes evidence, the web project must perform this review:

```text
1. Read the updated Stage186 GitNexus report.
2. Read symbol-to-branchpoint connectivity.
3. Read orphan legacy symbol report.
4. Read successor trace matrix.
5. Check whether Stage190 and Page08 release gate changed to PASS or PASS_WITH_WARNINGS.
6. If PASS, begin Page09 design/development.
7. If WARNINGS, decide whether warnings can be carried forward.
8. If FAIL, stop and repair Page08 before continuing.
```

## 10. Why this solves the Codex limit problem

This workflow reduces local Codex usage by narrowing its job:

```text
Local Codex does not need to design every page from scratch.
Local Codex does not need to create all hub documents.
Local Codex does not need to manage the entire long-range roadmap.
Local Codex only performs local indexing, preflight, evidence extraction, and evidence commit.
```

The web project can then continue with:

```text
stage design
manifest expansion
report analysis
workflow updates
PR updates
next-stage development
```

This split keeps development moving even when local Codex limits are low.

## 11. Final operating rule

For every future stage:

```text
Web builds the stage structure.
Local Codex supplies fresh local evidence.
Web reads the evidence and builds the next stage.
```

This is the standard operating model for Page08~Page17.
