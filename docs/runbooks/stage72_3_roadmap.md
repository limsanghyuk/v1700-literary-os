# Stage72.3 Roadmap

## Goal

Recover Stage01-39 foundation lineage and make future changes pass organic impact review.

## Council References

This roadmap is the compact execution summary. The full council package is:

```text
docs/proposals/stage72_3_three_expert_council_proposal.md
docs/architecture/stage72_3_foundation_lineage_recovery_blueprint.md
docs/reviews/stage72_3_principal_engineer_validation.md
docs/runbooks/stage72_3_consensus_roadmap.md
```

## Phase 0: Baseline Lock

```text
python tools/run_stage72_2_release_gate.py
python tools/run_release_gate.py
python -m pytest -q tests
gitnexus list
```

Exit:

```text
Stage72.2 gate pass
release gate pass
pytest green
GitNexus alias v1700_stage72_3_ascii registered
```

## Phase 1: Historical Evidence Scan

Inputs:

```text
C:\AI_Codex\codex-work\gpt\knowledge_base\v1650_stage35_critic_comparison_gate
```

Outputs:

```text
manifests/pre_stage40_raw_evidence_index.json
```

Exit:

```text
Stage01-39 manifests, reports, tests, and design docs are indexed.
```

## Phase 2: Concept Card Normalization

Outputs:

```text
manifests/pre_stage40_lineage_manifest.json
docs/stages/stage_001_039_foundation.md
```

Exit:

```text
At least 20 high-value concepts are classified.
Each concept has source evidence.
```

## Phase 3: Current Anchor Mapping

Outputs:

```text
docs/generated/wiki/foundation_lineage_wiki.md
docs/generated/skills/foundation_lineage_skill.md
```

Exit:

```text
Each LIVE or PARTIAL concept has a current runtime, gate, test, doc, or manifest anchor.
```

## Phase 4: Organic Impact Governance

Outputs:

```text
docs/runbooks/organic_impact_review_protocol.md
manifests/change_impact_review_template.json
src/v1700/gates/pre_stage40_survival_gate.py
tools/run_pre_stage40_survival_gate.py
tests/test_stage72_3_pre_stage40_survival_gate.py
```

Exit:

```text
Future major changes require lineage, context, impact, tests, boundaries, and rollback plan.
```

## Phase 5: Handoff

Outputs:

```text
release/current/stage72_3_developer_handoff_report.md
packages/v1700_stage72_3/*.zip
```

Exit:

```text
Stage72.3 gate pass
Stage72.2 gate still pass
release gate pass
pytest green
provider calls 0
Node2 raw reveal access 0
```
