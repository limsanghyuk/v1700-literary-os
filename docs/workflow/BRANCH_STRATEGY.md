# V1700 Branch Strategy

- Start every Stage from `main` or an explicitly sealed integrated package.
- Use `stageNNN-topic` branch names.
- Keep web-generated Stage branches as staging pointers when connector limits block full payload pushes.
- Local Codex or Antigravity must mirror the verified ZIP into the branch before PR closure.
- Merge before tag. Tag and release assets are official only after main is green.
