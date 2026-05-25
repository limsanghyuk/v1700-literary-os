# Stage166 Regression Hardening Report

## Target

- Stage: Stage166 — Page04 Release Seal
- Baseline: uploaded integrated Stage166 repository ZIP
- Purpose: execute regression, identify Page04 seal logic weaknesses, harden the implementation, and re-run validation.

## Findings

### 1. Page04 invariant freeze was too narrow

The previous `Page04 Invariant Freeze` checked Stage165 gate/report evidence only. Because Stage166 is a page-level release seal for Stage161~Stage166, it must detect invariant drift in any upstream Page04 stage, including Stage161, Stage162, Stage163, and Stage164.

Confirmed adversarial failure before patch:

```text
stage164_release_gate_report.provider_generation_enabled = true
run_stage166_page04_release_seal(...) -> status: pass
```

### 2. Stage166 release gate cached stale PASS results

The previous `run_stage166_release_gate` cached results by repository root path. In the same Python process, if evidence changed after a first PASS, the gate could return the stale cached PASS.

Confirmed adversarial failure before patch:

```text
first run_stage166_release_gate(...) -> pass
mutate stage165_render_quality_boundary_preflight_report.provider_generation_enabled = true
second run_stage166_release_gate(...) -> pass
```

## Fixes

### 1. Cross-stage Page04 invariant matrix

`src/v1700/page04_release_seal/report.py` now checks invariant evidence across all upstream Stage161~Stage165 reports and release gates.

- Strict core invariants must be present and exact in all upstream reports/gates.
- Optional invariants are checked when present, without blocking older evidence that did not define that field.
- The generated `page04_invariant_freeze.json` now includes an evidence matrix with 10 sources and 190 checks.

### 2. No stale release-gate cache

`src/v1700/gates/stage166_release_gate.py` no longer caches results. Each call recomputes Stage166 evidence and re-reads current files.

### 3. Added adversarial regression tests

`tests/test_stage166_page04_release_seal.py` adds:

- upstream gate invariant drift block test
- upstream report invariant drift block test
- release gate stale-cache prevention test

The test sandbox copy was also narrowed to ignore old bulky historical reports and ZIPs, so adversarial regression remains fast without changing product behavior.

## Validation summary

```text
compileall: pass
mandatory predevelopment: pass
metadata consistency: pass
release asset integrity: pass
Stage165 release gate: pass
Stage166 page04 release seal: pass
Stage166 release gate: pass
main release gate: pass
repo doctor: pass
Page04 Stage161~166 pytest: 39 passed
```

## Preserved invariants

```text
provider_default_calls = 0
live_provider_call_count_in_release_gate = 0
provider_generation_count = 0
runtime_execution_count = 0
write_operation_count = 0
node2_raw_reveal_access = 0
boundary_violation_count = 0
raw_manuscript_provider_leakage = 0
raw_manuscript_cross_project_leakage = 0
credential_leakage = 0
rendering_runtime_enabled = false
generation_runtime_enabled = false
provider_generation_enabled = false
runtime_execution_enabled = false
render_write_enabled = false
memory_write_enabled = false
canon_mutation_enabled = false
runtime_training_enabled = false
```
