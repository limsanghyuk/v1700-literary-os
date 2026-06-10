# Page08 Local Codex Execution Guide

Status: execution guide for local Codex / developer environment
Created: 2026-05-28
Page: Page08 — Lineage / Hub / Formula Authority
Stage range: Stage186~Stage190
Recommended branch: stage186-page08-branchpoint-map

## 1. Purpose

This guide tells a local Codex or developer environment how to investigate, learn, and execute the Page08 detailed proposal and blueprint.

Page08 must be implemented before Page09~Page17 work. Do not start EAT8D Feature Schema, Story Patch, Narrative PR, Narrative IDE, MultiWork, plugin, or learning implementation before Page08 is sealed.

## 2. Repository

```text
limsanghyuk/v1700-literary-os
```

## 3. Required first-read documents

Read these first, in order:

```text
docs/roadmaps/page08_page17_commercial_absorption_writer_studio_roadmap.md
docs/roadmaps/page08_page17_codex_ide_absorption_addendum.md
docs/roadmaps/page08_page17_page_blueprint_drafts.md
docs/proposals/page08_lineage_hub_formula_authority_proposal.md
docs/architecture/page08_lineage_hub_formula_authority_blueprint.md
manifests/page08_page17_roadmap_manifest.json
```

Then inspect workflow authority:

```text
docs/workflow/SESSION_PROTOCOL.md
docs/workflow/WORKFLOW.md
docs/workflow/BRANCH_STRATEGY.md
MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md
```

If present locally, inspect Stage185 evidence as local-known authority only. Do not treat Stage185 as hub-official unless hub closure evidence exists.

## 4. Required startup commands

From a clean local environment:

```bash
git fetch --all --tags --prune
git checkout main
git pull --ff-only origin main
python -m pip install -e ".[dev]"
python tools/session_start.py
python tools/run_mandatory_predevelopment_check.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_stage184_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

Then create the implementation branch:

```bash
git checkout -b stage186-page08-branchpoint-map
```

## 5. Stage186 implementation target

Start only with:

```text
Stage186 — Branchpoint Map Builder
```

Primary outputs:

```text
docs/lineage/v1700_branchpoint_map.md
manifests/stage186_branchpoint_manifest.json
release/current/stage186_branchpoint_map_report.json
tools/run_stage186_branchpoint_map_builder.py
tests/test_stage186_branchpoint_map_builder.py
```

## 6. Stage186 expected branchpoints

The first implementation should include at minimum:

```text
stage24_1_roadmap_metadata_hardening
v1632_selective_legacy_restoration
stage95_native_narrative_physics_engine
stage97_1_adversarial_longform_validation_hardening
stage120_126_gate_governor_cross_lineage_release
stage127_140_multiwork_gig_formula_learning_planning
page01_stage145_149_constitution_chain
page02_stage150_154_memory_body
page03_stage155_160_execution_body
page04_stage161_166_rendering_body
page05_stage167_172_evaluation_body
page06_stage173_178_governance_body
page07_stage179_184_evolution_body
stage185_8d_advisory_absorption_local_known
page08_page17_commercial_absorption_roadmap
uploaded_codex_ide_absorption_addendum
```

## 7. Stage186 manifest shape

Use this shape as the minimum schema:

```json
{
  "stage": 186,
  "branchpoints": [
    {
      "branchpoint_id": "page05_stage167_172_evaluation_body",
      "source_stage_or_page": "Page05 / Stage167~172",
      "status": "CORE",
      "authority_scope": "hub_official_or_documented_lineage",
      "core_invariants": [
        "evaluation outputs must preserve advisory vs blocking separation where applicable"
      ],
      "successor_requirements": [
        "Page12 must not promote literary advisory values into hard gates without evidence and policy"
      ],
      "forbidden_regressions": [
        "hard-block literary outcome solely from 8D value"
      ],
      "evidence_files": [],
      "successor_trace_required": true
    }
  ]
}
```

## 8. Stage186 report shape

`release/current/stage186_branchpoint_map_report.json` should include:

```json
{
  "stage": 186,
  "status": "PASS",
  "branchpoint_count": 0,
  "core_count": 0,
  "gated_count": 0,
  "advisory_count": 0,
  "legacy_count": 0,
  "deprecated_count": 0,
  "replaced_with_trace_count": 0,
  "failures": [],
  "warnings": []
}
```

## 9. Stage186 validation rules

Stage186 must fail if:

```text
branchpoint_id is missing
status is missing
CORE branchpoint has no invariant
successor requirement is missing
Stage185 is marked hub-official without closure evidence
uploaded proposal Stage186~195 numbering is used as active numbering
8D advisory principle is absent
Page09 is allowed to start without Page08 inheritance authority
```

## 10. After Stage186

Proceed in order:

```text
Stage187 — Inheritance Contract Gate
Stage188 — Hub Authority Reconciliation
Stage189 — Formula / Logic Ledger v2
Stage190 — Page08 Release Seal
```

Do not skip directly to Stage189 or Stage190.

## 11. Local Codex prompt

Use this prompt to start the local Codex implementation:

```text
You are continuing V1700 Page08 — Lineage / Hub / Formula Authority. Read docs/roadmaps/page08_page17_commercial_absorption_writer_studio_roadmap.md, docs/roadmaps/page08_page17_codex_ide_absorption_addendum.md, docs/roadmaps/page08_page17_page_blueprint_drafts.md, docs/proposals/page08_lineage_hub_formula_authority_proposal.md, docs/architecture/page08_lineage_hub_formula_authority_blueprint.md, docs/development/page08_codex_local_execution_guide.md, and manifests/page08_page17_roadmap_manifest.json. Implement Stage186 Branchpoint Map Builder only. Create docs/lineage/v1700_branchpoint_map.md, manifests/stage186_branchpoint_manifest.json, release/current/stage186_branchpoint_map_report.json, tools/run_stage186_branchpoint_map_builder.py, and tests/test_stage186_branchpoint_map_builder.py. Preserve Provider-Zero default, Node2 surface safety, Stage185 8D advisory principle, non-mutating ASD, audit-first learning, project isolation before MultiWork sharing, and license boundary before cross-project access. Do not implement Page09 or Codex Story Patch features yet.
```

## 12. PR expectation

The Stage186 PR should say:

```text
This PR implements Stage186 Branchpoint Map Builder as the first stage of Page08. It does not implement Page09 commercial absorption, Page12 EAT8D extractor, Page13 Story Patch, or Stage185 hub closure.
```

## 13. Stop conditions

Stop and request review if any of these occur:

```text
Stage185 files appear newer than hub Stage184 but no hub closure evidence exists.
Existing manifests already define conflicting Stage186 semantics.
A previous branch already implemented Page08.
Release asset integrity fails before Page08 work begins.
Mandatory predevelopment check fails.
```
