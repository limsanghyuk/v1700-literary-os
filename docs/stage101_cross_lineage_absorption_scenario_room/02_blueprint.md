# Stage101 Blueprint

## Architecture

```text
Stage100 RC baseline
  -> Stage101.0 Cross-lineage preflight
  -> V430 source probe
  -> Absorption candidate matrix
  -> Scenario Room contracts
  -> Scene beat / action / dialogue-silence / prop reveal cue integration
  -> Dual-mode regression
  -> Stage101 release gate
  -> Main release gate / repo doctor / clean package
```

## Package Layout

```text
src/v1700/cross_lineage/
  v430_candidate_probe.py
  absorption_decision.py
  lineage_trace.py

src/v1700/scenario_room/
  contracts.py
  scene_beat_board.py
  investigation_action.py
  dialogue_silence_cue.py
  prop_reveal.py
  planner.py
  scenario_room_orchestrator.py
  scenario_room_report.py

src/v1700/stage101/
  contracts.py
  source_probe.py
  absorption_matrix.py
  orchestrator.py
  report.py

src/v1700/gates/
  stage101_release_gate.py
```

## Data Contracts

Stage101 introduces these core contracts:

- `SceneBeat`
- `InvestigationActionBeat`
- `DialogueSilenceCue`
- `PropRevealCue`
- `ScenarioRoomPlan`
- `Stage101AbsorptionCandidate`
- `Stage101Preflight`

## Stage Steps

### Stage101.0

Locks the Stage100 baseline, probes V430 source availability, builds the absorption candidate matrix, and blocks untraced runtime merge.

### Stage101.1

Builds the Scenario Room contract layer and validates scenario mode without changing prose-mode authority.

### Stage101.2

Integrates scene beats, investigation/action beats, dialogue/silence cues, and prop-led reveal cues. Every cue must remain bound to scene necessity, agency, reveal budget, and Node2 surface-only boundaries.

### Stage101.3

Runs dual-mode regression to prove Stage101 does not conflate prose and scenario evaluation.

## Release Gate Checks

The Stage101 gate checks:

- Stage100 baseline gate
- GitNexus cross-lineage preflight
- V430 source probe
- absorption candidate matrix
- V430 untraced merge block
- scenario room contract
- scene beat board
- investigation/action beats
- dialogue/silence cues
- prop reveal cues
- dual-mode regression
- provider zero
- Node2 boundary
- raw manuscript leakage
- branchpoint survival
- symbol-to-branchpoint trace
- README active stage consistency
- package manifest canonical reference
- repo doctor
- main release gate
- clean ZIP packaging
- secret scan

## Release Evidence

```text
release/current/stage101_0_cross_lineage_preflight_report.json
release/current/stage101_v430_source_probe_report.json
release/current/stage101_absorption_candidate_matrix.json
release/current/stage101_scenario_room_contract_report.json
release/current/stage101_scenario_cue_integration_report.json
release/current/stage101_dual_mode_regression_report.json
release/current/stage101_cross_lineage_scenario_room_report.json
release/current/stage101_release_gate_report.json
release/current/stage101_developer_handoff_report.md
```

## Packaging

The final Stage101 package must exclude:

- `.git`
- `.gitnexus`
- `.venv`
- `__pycache__`
- `.pytest_cache`
- `*.pyc`
- temporary logs and scratch files

The package must be re-extracted and validated before handoff.
