# Stage147 Blueprint - Project Manifest Body

## Intent

Stage147 turns sample project files into canonical manifest-body packets that match the Stage146 narrative contracts.

## Flow

```text
sample project files
  -> project manifest catalog
  -> canonical manifest bundle
  -> manifest-state bindings
  -> policy boundary checks
  -> manifest load order
  -> Stage148 entry signals
```

## Inputs

- `samples/korean_drama_family_secret/project.json`
- `samples/korean_drama_family_secret/characters.json`
- `samples/korean_drama_family_secret/world.json`
- `samples/korean_drama_family_secret/plot_outline.md`
- `samples/korean_drama_family_secret/scene_requests/scene_001.json`

## Outputs

- `canonical_manifest_bundle.json`
- `project_manifest_catalog.json`
- `manifest_state_bindings.json`
- `manifest_policy_boundary.json`
- `manifest_load_order.json`
- `stage148_entry_signals.json`

## Authority Rules

- Stage146 remains the baseline authority for state shapes.
- Stage147 may derive packet fields, but it may not enable writes or hidden-state exposure.
- Reveal packets must remain hidden to Node2 and only expose a surface-safe projection.
- All manifest packets remain local-only synthetic placeholders.
