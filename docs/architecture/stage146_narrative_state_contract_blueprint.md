# Stage146 Blueprint - Narrative State Contract

## Contract Surface

```text
SeriesState
  -> EpisodeState
    -> SceneState

SeriesState
  -> CharacterState
  -> WorldState

SceneState
  -> RevealState

EpisodeState
  -> ContinuityState
```

## Canonical Objects

- `SeriesState`: series identity, format, theme, episode order, and timeline anchor
- `EpisodeState`: episode premise, order, scene order, and episode continuity anchor
- `SceneState`: location, participants, objective, and surface constraints
- `CharacterState`: role, goals, relationships, and knowledge boundary
- `WorldState`: era, locations, institutions, rules, and public facts
- `RevealState`: visibility level, holders, unlock condition, and Node2-safe projection
- `ContinuityState`: timeline position, open threads, resolved threads, contradiction watchlist, and repair policy

## Safety Rules

- Node2 receives only surface-safe projections.
- Reveal packets are never handed raw to Node2.
- Continuity rules are advisory and gating authority only.
- All state contracts remain read-only until later approved stages.

## Follow-On Dependency

- Stage147 binds project manifests to these contracts.
- Stage148 binds node authorities to these contracts.
- Stage149 blocks Stage150 unless this contract remains intact.
