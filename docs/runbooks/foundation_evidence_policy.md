# Foundation Evidence Policy

## Purpose

Stage72.3 separates two questions that were previously easy to blur:

```text
How strong is the historical evidence?
How alive is the concept in the current runtime?
```

## Evidence Levels

```text
E1_DOCUMENT
The concept exists only in design text.

E2_ARTIFACT
The concept has a manifest, report, fixture, or sample output.

E3_EXECUTABLE
The concept has an executable script or module.

E4_TESTED
The concept has test or harness evidence.

E5_LIVE_CURRENT
The concept has current V1700 runtime, test, or gate anchors.
```

## Survival Statuses

```text
LIVE_RUNTIME
The concept is active in runtime code and has a current anchor.

LIVE_GATE_ONLY
The concept is enforced by a gate but not directly in runtime behavior.

PARTIAL
Part of the concept survives, but runtime work remains.

DOCUMENTED_ONLY
The concept is preserved for future restoration but not active.

DEFERRED
The concept is valid but deliberately delayed.

REJECTED_WITH_REASON
The concept should not be restored without a new decision.

UNKNOWN_NEEDS_REVIEW
The concept has not been classified enough for promotion.
```

## Policy

Do not promote a major change if it downgrades a high-priority concept without a written review decision.

Do not mark a concept `LIVE_RUNTIME` unless it has a current runtime anchor.

Do not mark a concept `PARTIAL` unless at least one current anchor exists.
