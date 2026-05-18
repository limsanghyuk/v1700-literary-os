# Stage82 — Blind Critic Evaluation & Benchmark Harness

Stage82 adds a local-first blind critic benchmark to the V1700 literary OS.

## Purpose

Stage82 verifies that V1700's engineered Korean-drama composition, quality endurance, and reabsorption stack can be evaluated against baseline generation modes without relying on external provider calls.

## Blind candidates

```text
Candidate A = pure GPT direct-mode baseline simulation
Candidate B = V1700 engineered literary OS output
Candidate C = Claude-style reference simulation
```

The harness keeps candidate IDs blind during scoring, then reveals the source label in the release report.

## Evaluation axes

```text
series_story_arc
macro_plot_architecture
episode_microplot_linkage
supporting_character_web
causal_event_weaving
emotional_accessibility
prose_naturalness
mise_en_scene_density
reveal_safety
longform_expandability
```

## Important limitation

Stage82 is a benchmark harness and local-first evaluation gate. It does not claim live paid GPT/Claude API execution. External provider benchmarking remains a later commercial-readiness task.

## Acceptance

```text
python tools/run_blind_critic_benchmark.py
python tools/run_stage82_release_gate.py
python tools/run_release_gate.py
```

Pass means V1700 wins the local blind benchmark by at least +1.0 over pure GPT direct-mode simulation, with reveal leakage 0 and provider default calls 0.
