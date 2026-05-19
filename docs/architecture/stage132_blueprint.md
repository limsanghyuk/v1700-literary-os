# Stage132 Blueprint: Contradiction Classifier + Mystery Exemption

## Purpose

Stage132 turns Stage131's advisory categories into evidence-based classification.

## Architecture

```text
Stage131 GIG Advisory
  -> contradiction_classifier.classifier
  -> contradiction_classifier.mystery_exemption
  -> contradiction_classifier.preflight
  -> stage132.runner
  -> stage132_release_gate
  -> main release gate
```

## Runtime Modules

```text
src/v1700/contradiction_classifier/
  contracts.py
  classifier.py
  mystery_exemption.py
  preflight.py
  report.py

src/v1700/stage132/
  stage132_runner.py

src/v1700/gates/
  stage132_release_gate.py
```

## Classification Matrix

| Class | Evidence Rule | Action |
| --- | --- | --- |
| true_contradiction | same canon scope and two high-confidence incompatible facts | REVIEW_REQUIRED |
| intentional_mystery | reveal lock plus payoff budget plus mystery intent | ALLOW_WITH_LOCK |
| character_misunderstanding | conflict belongs to POV boundary | ALLOW_WITH_POV_TAG |
| reveal_delay | scheduled reveal plus payoff budget | ALLOW_WITH_REVEAL_BUDGET |
| no_conflict | no surface conflict | PASS |

## Invariants

```text
provider_default_calls = 0
live_provider_call_count_in_release_gate = 0
node2_raw_reveal_access = 0
raw_manuscript_provider_leakage = 0
raw_manuscript_cross_project_leakage = 0
credential_leakage = 0
cross_project_write_allowed = false
gate26_hard_block_enabled = false
canon_auto_resolution_count = 0
auto_repair_mutation_count = 0
```

## Release Evidence

```text
release/current/stage132_contradiction_classifier_report.json
release/current/stage132_release_gate_report.json
release/current/stage132_contradiction_classifier_pack/
  classifier_matrix_report.json
  mystery_exemption_report.json
  gitnexus_preflight_report.json
  stage132_summary.json
```
