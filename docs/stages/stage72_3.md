# Stage72.3 - Foundation Lineage Recovery and Organic Impact Governance

Stage72.3 restores the missing formal link between Stage01-39 foundation concepts and the current V1700 active runtime.

## What It Adds

- `manifests/pre_stage40_raw_evidence_index.json`
- `manifests/pre_stage40_lineage_manifest.json`
- `docs/stages/stage_001_039_foundation.md`
- `docs/generated/wiki/foundation_lineage_wiki.md`
- `docs/generated/skills/foundation_lineage_skill.md`
- `src/v1700/gates/pre_stage40_survival_gate.py`
- `src/v1700/gates/stage72_3_release_gate.py`
- organic impact governance runbooks and change review template

## Design Rule

Stage01-39 logic is not blindly copied back into the active repo.

The active repo inherits it by concept:

```text
source evidence -> concept card -> current anchor -> survival status -> gate
```

## Promotion Meaning

Stage72.3 is complete only when the current baseline still passes:

```text
Stage72.2 release gate
Stage72.3 survival gate
main release gate
pytest
provider calls 0
Node2 raw reveal access 0
```
