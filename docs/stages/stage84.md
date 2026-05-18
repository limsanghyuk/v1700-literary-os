# Stage84 — Claude V370 Runtime Absorption into V1700 Korean Drama OS

Stage84 absorbs Claude V370 runtime muscle into the V1700 Korean Drama OS skeleton.

## Absorbed runtime capabilities

- ClosedLoopRenderer
- KoreanAntiLLMFilter
- StyleDNA
- SensoryAnchorInjector
- EmotionToBehaviorRenderer
- KoreanRhythmRewriter
- ReaderSurfaceScorer
- LocalJudgmentValidator
- LLMNodeRouter with provider defaults locked to zero
- SelfLearningCollector local trace dataset

## Non-negotiable boundaries

- V370 is not copied wholesale.
- V1700 hierarchy is preserved: Series Story → Macro Plot → Broadcast Episode → Micro Plot → Sequence → Scene.
- Node2 raw reveal access remains zero.
- Provider default calls remain zero.
- GitNexus remains an optional sidecar.

## Gate

```bash
python tools/run_stage84_release_gate.py
```

Expected result: `status = pass`.
