# Stage115 — CharacterInfluenceMatrix + Structural Balance

Stage115 adds the NIE character graph layer. It converts pairwise character pressure into an asymmetric influence matrix `W[n×n]`, computes directed structural-balance triangle tension, and assigns janggi-style role tiers from PageRank and betweenness centrality.

## Invariants

- `W[i][j]` and `W[j][i]` may differ.
- Influence weights are bounded to `[-1, +1]`.
- At least one high-tension triangle is detected in the fixture pack.
- Every fixture character receives a role tier: `jang`, `cha`, `po`, `ma_sang`, or `jol`.
- Provider calls remain zero in release gates.
- Stage115 is visible to release gate and repo doctor.

## Evidence

- `release/current/stage115_character_influence_matrix_report.json`
- `release/current/stage115_release_gate_report.json`
