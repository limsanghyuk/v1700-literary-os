# Stage125 — Gate25/28/29 Governor

Stage125 keeps Gate25 as the primary NIE v1.0 release authority and admits Gate28 and Gate29 only as secondary gates.

- Gate25: primary release authority
- Gate28: secondary ASD quality/debt gate
- Gate29: secondary PNE predictive debt gate

Blocked in Stage125:

- Gate28 primary authority
- Gate29 primary authority
- release-gate runtime training
- auto-repair mutation during release
- live provider calls in governor
- direct V545/V555 package merge

The governor emits a deterministic decision and release evidence under `release/current/`.
