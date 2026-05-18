# Stage123 — ASD / Gate28 Absorption

Stage123 absorbs the V545 Autonomous Story Doctor concepts conservatively over the Stage122 trunk.

## Absorbed

- NarrativeDebtDetector
- ArcConsistencyChecker
- StoryDoctorOrchestrator
- AutoRepairExecutor in dry-run mode only
- Gate28 as a secondary StoryQualityGate

## Gate28 thresholds

- G28-1: debt_score <= 0.50
- G28-2: arc_score <= 0.40
- G28-3: high_priority_cnt <= 5
- G28-4: combined_quality <= 0.45
- combined_quality = min(debt_score * 0.55 + arc_score * 0.45, 1.0)

## Explicitly blocked

- Gate28 primary release authority
- graph mutation auto-repair
- LLM repair generation
- direct V545 package merge
- Gate29 predictive authority

Provider calls remain zero in release gate mode.
