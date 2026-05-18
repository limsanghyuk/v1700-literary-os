# Organic Impact Review Protocol

## Purpose

Every major V1700 change must describe how it affects inherited concepts before promotion.

This protocol prevents a common failure mode:

```text
new patch fixes the present problem
  -> old concept is bypassed
  -> later stage must rediscover and reconnect it
```

## Required Before Major Changes

Before a major runtime, gate, or Node behavior change, create a change review packet from:

```text
manifests/change_impact_review_template.json
```

The packet must include:

```text
change_intent
related_stage_origins
related_concepts
affected_runtime_modules
affected_tests
affected_gates
node_authority_risks
reveal_leakage_risks
provider_cost_risks
graphnexus_context
graphnexus_impact
rollback_plan
promotion_decision
```

## Required Commands

```powershell
python tools/run_pre_stage40_survival_gate.py
python tools/run_stage72_3_release_gate.py
python tools/run_release_gate.py
python -m pytest -q tests
```

## Promotion Rule

Promotion is blocked if a high-priority foundation concept becomes:

```text
UNKNOWN_NEEDS_REVIEW
```

or if a LIVE/PARTIAL concept loses all current anchors.

## Node Boundary Reminder

Node2 may receive only surface-safe information.

Raw reveal contents, hidden canon facts, and full graph internals remain forbidden.
