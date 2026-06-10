# V1700 Page08 Blueprint — Lineage / Hub / Formula Authority

Status: detailed blueprint draft
Created: 2026-05-28
Proposal: docs/proposals/page08_lineage_hub_formula_authority_proposal.md
Stage range: Stage186~Stage190

## 0. Blueprint summary

Page08 creates the authority layer required before the Page09~Page17 roadmap can safely continue. It turns lineage, hub state, formulas, gates, runners, fixtures, and release evidence into traceable contracts.

Page08 does not implement commercial features. It prepares the branchpoint and inheritance authority that future commercial absorption must obey.

## 1. Implementation objectives

```text
1. Build a branchpoint map.
2. Build a branchpoint manifest.
3. Build an inheritance contract gate.
4. Reconcile hub official authority vs local known evidence.
5. Build Formula / Logic Ledger v2.
6. Seal Page08 and hand off to Page09.
```

## 2. Directory plan

Page08 should add or update the following paths:

```text
docs/lineage/v1700_branchpoint_map.md
docs/proposals/page08_lineage_hub_formula_authority_proposal.md
docs/architecture/page08_lineage_hub_formula_authority_blueprint.md
docs/development/page08_codex_local_execution_guide.md
docs/development/page08_next_chat_handoff.md
manifests/stage186_branchpoint_manifest.json
manifests/stage187_inheritance_contract.json
manifests/stage188_hub_authority_reconciliation.json
manifests/stage189_formula_logic_ledger_v2.json
manifests/stage189_formula_status_matrix.json
release/current/stage186_branchpoint_map_report.json
release/current/stage187_inheritance_contract_gate_report.json
release/current/stage188_hub_authority_reconciliation_report.json
release/current/stage189_formula_logic_ledger_report.json
release/current/stage190_page08_release_seal_report.json
release/current/page08_release_gate_report.json
tools/run_stage186_branchpoint_map_builder.py
tools/run_stage187_inheritance_contract_gate.py
tools/run_stage188_hub_authority_reconciliation.py
tools/run_stage189_formula_logic_ledger_v2.py
tools/run_stage190_page08_release_seal.py
tools/run_page08_release_gate.py
tests/test_stage186_branchpoint_map_builder.py
tests/test_stage187_inheritance_contract_gate.py
tests/test_stage188_hub_authority_reconciliation.py
tests/test_stage189_formula_logic_ledger_v2.py
tests/test_stage190_page08_release_seal.py
```

This blueprint is a draft. The actual Stage186 implementation may split or rename some files if the release gate records the successor mapping.

## 3. Stage186 — Branchpoint Map Builder

### Purpose

Stage186 identifies the branchpoints that must be inherited by future pages.

### Input sources

The implementation should inspect at least:

```text
docs/stages/STAGE_INDEX.md
docs/roadmaps/page08_page17_commercial_absorption_writer_studio_roadmap.md
docs/roadmaps/page08_page17_codex_ide_absorption_addendum.md
docs/roadmaps/page08_page17_page_blueprint_drafts.md
manifests/page08_page17_roadmap_manifest.json
release/current/*stage184*
```

If Stage185 local files are present in the local environment, they should be referenced as local-known evidence, not hub-official authority unless hub closure exists.

### Minimum branchpoints

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

### Manifest schema

```json
{
  "stage": 186,
  "branchpoints": [
    {
      "branchpoint_id": "stage97_1_adversarial_longform_validation_hardening",
      "source_stage": "Stage97.1",
      "status": "CORE",
      "authority_scope": "hub_or_legacy_documented",
      "core_invariants": [
        "branchpoint survival must be checked before studio progression",
        "adversarial broken-proof evidence must not be skipped"
      ],
      "successor_requirements": [
        "future writer-studio pages must not bypass adversarial validation lineage"
      ],
      "forbidden_regressions": [
        "remove negative corpus requirement without successor trace"
      ],
      "evidence_files": [],
      "successor_trace_required": true
    }
  ]
}
```

### Runner behavior

`tools/run_stage186_branchpoint_map_builder.py` should:

```text
1. load the known branchpoint seed list
2. validate required fields
3. write or validate manifests/stage186_branchpoint_manifest.json
4. write release/current/stage186_branchpoint_map_report.json
5. fail if any CORE branchpoint has no invariant
```

### Failure conditions

```text
missing branchpoint_id
missing status
CORE branchpoint without core_invariants
branchpoint without successor policy
Stage185 marked hub-official without hub evidence
uploaded proposal Stage186~195 accepted as active numbering without remap
```

## 4. Stage187 — Inheritance Contract Gate

### Purpose

Stage187 defines the inheritance declaration that future pages and stages must provide.

### Contract schema

```json
{
  "contract_id": "stage187_inheritance_contract",
  "applies_to": "Page09~Page17 and future stage work",
  "required_declaration_fields": [
    "must_inherit",
    "may_extend",
    "must_not_override",
    "may_deprecate_only_with_successor_trace"
  ],
  "global_must_inherit": [
    "Provider-Zero default",
    "Node2 surface safety",
    "8D advisory principle",
    "non-mutating ASD until author-approved repair path",
    "audit-first learning",
    "project isolation before sharing",
    "license boundary before cross-project access"
  ]
}
```

### Runner behavior

`tools/run_stage187_inheritance_contract_gate.py` should:

```text
1. load manifests/stage186_branchpoint_manifest.json
2. load manifests/stage187_inheritance_contract.json
3. validate all required declaration fields
4. validate global inherited rules
5. validate uploaded Codex / Narrative IDE concepts are marked as remapped, not direct Stage186~195
6. write release/current/stage187_inheritance_contract_gate_report.json
```

### Failure conditions

```text
required declaration field missing
global inherited rule missing
future page allowed to omit inheritance declaration
8D advisory principle absent
StoryPatch approval invariant absent
learning audit invariant absent
MultiWork isolation invariant absent
```

## 5. Stage188 — Hub Authority Reconciliation

### Purpose

Stage188 records the difference between hub-official authority and local-known authority.

### Authority categories

```text
HUB_OFFICIAL
LOCAL_KNOWN
PLANNED
SUPERSEDED_WITH_TRACE
DEPRECATED_WITH_REASON
```

### Manifest schema

```json
{
  "stage": 188,
  "hub_authority": {
    "latest_confirmed_hub_stage": "Stage184",
    "latest_confirmed_hub_page": "Page07",
    "evidence": [
      "PR #54 officialized Stage184 Page07 Release Seal",
      "PR #55 upgraded GPT preflight workflow authority"
    ]
  },
  "local_known_authority": {
    "stage185": {
      "name": "NarrativeStateTensor 8D Advisory Absorption",
      "status": "LOCAL_KNOWN",
      "hub_closure": false
    }
  },
  "roadmap_authority": {
    "page08_page17": "PLANNED"
  }
}
```

### Runner behavior

`tools/run_stage188_hub_authority_reconciliation.py` should:

```text
1. read hub authority manifest if present
2. read roadmap manifest
3. record Stage184 as hub official unless newer hub evidence is present
4. record Stage185 as local-known unless hub closure files are present
5. record Page08~Page17 roadmap as planned authority
6. write release/current/stage188_hub_authority_reconciliation_report.json
```

### Failure conditions

```text
local-known evidence marked hub-official without closure
roadmap marked release seal
missing authority category
missing evidence note for authority promotion
```

## 6. Stage189 — Formula / Logic Ledger v2

### Purpose

Stage189 creates a ledger that tracks formulas and logic units together. It is not only a formula list.

### Ledger entry schema

```json
{
  "entry_id": "eat8d_advisory_tensor",
  "kind": "formula_or_logic",
  "status": "ADVISORY_WITH_GATED_EVIDENCE",
  "introduced_by": "Stage185 local-known evidence",
  "inherits_from": ["Page05 Evaluation Body"],
  "must_not_be_used_as": ["hard literary quality gate"],
  "allowed_successors": ["Page12 EAT8D Feature Extraction"],
  "related_contracts": [],
  "related_gates": [],
  "related_fixtures": [],
  "release_evidence": []
}
```

### Required first ledger families

```text
Provider-Zero / provider sandbox policy
Node2 surface safety
Memory Body read-first policy
Execution Body deterministic dry-run policy
Rendering Body surface draft dry-run policy
Page05 evaluation body
Page06 governance body
Page07 evolution body
Stage185 8D advisory tensor
GIG / contradiction advisory policy
ASD non-mutating repair lineage
MultiWork isolation-before-sharing
Author license boundary
Formula / Logic successor trace rule
```

### Runner behavior

`tools/run_stage189_formula_logic_ledger_v2.py` should:

```text
1. load branchpoint manifest
2. load inheritance contract
3. build or validate formula / logic entries
4. validate each CORE or GATED entry has successor policy
5. write stage189_formula_logic_ledger_v2.json and stage189_formula_status_matrix.json
6. write release/current/stage189_formula_logic_ledger_report.json
```

### Failure conditions

```text
ledger entry without status
CORE entry without successor policy
ADVISORY entry used as hard gate without promotion record
logic unit without related stage or branchpoint
Stage185 8D missing advisory status
```

## 7. Stage190 — Page08 Release Seal

### Purpose

Stage190 seals Page08 as the authority base for Page09~Page17.

### Required checks

```text
Stage186 branchpoint map report exists
Stage187 inheritance contract gate report exists
Stage188 hub authority reconciliation report exists
Stage189 formula logic ledger report exists
Page08 local Codex execution guide exists
Page08 next-chat handoff exists
roadmap manifest points to addendum and blueprint drafts
```

### Runner behavior

`tools/run_stage190_page08_release_seal.py` should:

```text
1. verify required Page08 docs
2. verify required manifests
3. verify required reports
4. verify Page09 start is blocked unless Page08 seal passes
5. write release/current/stage190_page08_release_seal_report.json
```

`tools/run_page08_release_gate.py` should aggregate all Page08 stage reports.

### Failure conditions

```text
missing Page08 proposal
missing Page08 blueprint
missing Codex local execution guide
missing branchpoint manifest
missing inheritance contract
missing hub authority reconciliation
missing Formula / Logic Ledger v2
Page09 marked unblocked without Page08 seal
```

## 8. Test strategy

Unit tests should verify:

```text
branchpoint records require invariants
inheritance declarations require four fields
hub/local/planned authority categories are distinct
Formula / Logic Ledger entries require status
ADVISORY entries cannot be hard-gate entries without promotion record
Stage185 8D remains advisory
uploaded proposal stage numbering is remapped
Page08 release seal requires all prior reports
```

## 9. Fixture strategy

Positive fixtures:

```text
valid branchpoint manifest
valid inheritance contract
valid hub/local authority record
valid formula logic ledger
valid page08 seal input set
```

Negative fixtures:

```text
CORE branchpoint without invariant
future page without inheritance declaration
Stage185 marked hub-official without evidence
8D marked hard literary gate
GIG hard blocks mystery without exemption policy
Formula ledger entry without status
Page08 seal missing local execution guide
```

## 10. Local Codex integration

Local Codex should begin from these documents:

```text
docs/roadmaps/page08_page17_commercial_absorption_writer_studio_roadmap.md
docs/roadmaps/page08_page17_codex_ide_absorption_addendum.md
docs/roadmaps/page08_page17_page_blueprint_drafts.md
docs/proposals/page08_lineage_hub_formula_authority_proposal.md
docs/architecture/page08_lineage_hub_formula_authority_blueprint.md
docs/development/page08_codex_local_execution_guide.md
manifests/page08_page17_roadmap_manifest.json
```

After reading, Codex should start with Stage186 only.

## 11. Page08 to Page09 handoff

Page09 may start only after:

```text
Page08 release seal passes
Stage189 ledger exists
Page09 inherits Codex-first policy from the addendum
Page09 references Page08 inheritance contract
Page09 declares that commercial absorption cannot bypass branchpoint survival
```

## 12. Blueprint conclusion

Page08 makes lineage executable. Once complete, every future page can be developed aggressively without silently losing the old system because the inheritance gate and Formula / Logic Ledger define what must survive.
