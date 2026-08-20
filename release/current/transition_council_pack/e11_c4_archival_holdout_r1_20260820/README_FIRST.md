# E11-C4 Archival Holdout Package

Date: 2026-08-20

## Result

- Source: E10 controller decisions frozen before E10 EP15 target unblinding
- Targets: 6 works, 56 Sequences, no overlap with the original E11 six works
- C2 scope accuracy: 44/56 (78.57%)
- C4 A1-R1 scope accuracy: 45/56 (80.36%)
- Paired change: 3 improved, 2 worsened, exact McNemar p=1.0
- C2 L3 recall: 66.67%
- C4 L3 recall: 0%
- Material interventions: C2 11, C4 11
- Final-Sequence material rewrites: C2 0, C4 0

A1-R1 is rejected for adoption because the small accuracy gain coincided with complete loss of L3 recall. A2 was already implicit in the E10 controller and produced no incremental reduction.

## Directory Order

1. `00_PREUNBLIND`: frozen predictions and hashes created without reading holdout EpisodePlan/Arc.
2. `01_UNBLIND_RESULTS`: row-level gold, paired metrics, report, and output manifest.
3. `02_NEXT_DESIGN`: A1-R2 structural preregistration for a new unused holdout.
4. `03_REPRODUCTION_SCRIPTS`: exact freeze and scoring programs.

## Scientific Boundary

This is an archival holdout validation, not a newly generated prospective experiment and not promotion evidence. A1-R2 has been designed but not tested on another unused set.
