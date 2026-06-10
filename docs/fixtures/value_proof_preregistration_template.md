# Value Proof Preregistration Template

Status: fixture template draft
Created: 2026-06-07
Scope: post-roadmap value proof planning
Repository: limsanghyuk/v1700-literary-os

## 1. Purpose

This template preregisters a Value Proof experiment before any execution-engine expansion.

The purpose is to prevent post-hoc threshold changes and informal demo claims.

## 2. Core hypothesis

```text
V1700 structured literary OS + controlled LLM assistance produces better literary output than a pure LLM baseline under controlled evaluation.
```

## 3. Experiment ID

```text
value_proof_experiment_id:
created_at:
owner:
review_status:
```

## 4. Experiment arms

### Arm A — Pure LLM baseline

```text
provider:
model:
prompt:
temperature:
max_tokens:
target_length:
structure_guidance: none
```

### Arm B — V1700 structured pipeline

```text
provider:
model:
prompt:
temperature:
max_tokens:
target_length:
allowed_v1700_guidance:
formula_guidance:
critic_guidance:
corpus_reference_policy:
```

### Optional Arm C — Commercial tool baseline

```text
enabled: yes/no
tool_name:
terms_review_status:
configuration:
```

## 5. Controlled variables

Required controls:

- same base prompt
- same target language
- same target length
- same token budget
- same sampling policy unless explicitly justified
- randomized output order
- blinded arm labels
- no evaluator sees provider or arm labels

## 6. Evaluation dimensions

Minimum dimensions:

- story coherence
- scene tension
- character believability
- dialogue subtext
- emotional progression
- originality and cliche avoidance
- reader engagement
- genre fit

Optional dimensions:

- cultural specificity
- production adaptability
- serialized hook strength
- thematic depth

## 7. Evaluator plan

```text
minimum_evaluators:
evaluator_profile:
writer_or_reader_background:
conflict_of_interest_policy:
blindness_policy:
```

Recommended minimum:

```text
MVE: 2~3 evaluators
Full experiment: 5+ evaluators
```

## 8. Sample plan

```text
scene_count:
work_count:
genre_distribution:
randomization_seed:
exclusion_policy:
```

Recommended starting point:

```text
MVE: 10~15 scenes
Full experiment: 40~60 scenes
```

## 9. Threshold

Initial proposed threshold:

```text
Arm B preference >= 60 percent
p < 0.05 if sample size permits
effect size reported
```

If sample size is too small:

- report descriptive preference
- report confidence interval if possible
- report effect size
- do not overclaim statistical proof

## 10. Failure rule

If Arm B does not meet threshold, do not open execution-engine expansion based on the experiment.

Failure routes to:

- critic redesign
- corpus improvement
- formula calibration
- prompt/control redesign
- repeat with smaller corrected fixture

Failure must not route to uncontrolled feature expansion.

## 11. Evidence paths

Future experiment should save:

```text
experiments/value_proof/preregister.json
experiments/value_proof/prompts/
experiments/value_proof/outputs/
experiments/value_proof/blind_packets/
experiments/value_proof/evaluator_results/
experiments/value_proof/aggregate_report.md
release/current/value_proof_gate_report.md
```

## 12. Rights and safety policy

- no unlicensed full-text corpus ingestion
- use metadata and structured analysis where possible
- keep provider keys out of code and documents
- record source class for any corpus-derived prompt material

## 13. Approval status

```text
preregistration_status: draft / approved / rejected
approved_by:
approval_date:
```

## 14. Final rule

Do not run a claimed Value Proof experiment unless this template is completed and approved.
