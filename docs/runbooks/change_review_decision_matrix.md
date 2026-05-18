# Change Review Decision Matrix

## Decisions

```text
APPROVE
All required gates pass and no high-priority lineage risk is introduced.

APPROVE_WITH_CONDITIONS
The change is acceptable, but a follow-up concept restoration or test is required.

RESTORE_FIRST
The change touches a high-priority pre-Stage40 concept that is only partial or documented.

DEFER
The concept is valid, but the current stage should not absorb it yet.

REJECT
The change violates node authority, reveal safety, provider cost boundaries, or release invariants.
```

## Required Evidence

Every decision must cite:

```text
related concept_id
related stage origins
affected runtime files
affected tests or gates
rollback plan
```

## Default Rule

If a change affects Node2 prose rendering, longform scene/sequence planning, provider routing, or graph retrieval, the default decision is not `APPROVE`.

The default decision is:

```text
APPROVE_WITH_CONDITIONS
```

unless the pre-Stage40 survival gate and release gate both pass without new warnings.
