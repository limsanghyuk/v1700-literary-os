# EXT6 Append-Only Immutability Correction — 2026-07-29

## Independent audit finding

Six existing works — `비밀의숲`, `101번째프로포즈`, `W`, `강남엄마따라잡기`, `개와늑대의시간`, `개인의취향` — received a new EXT6 cast/source evidence layer.

- new EXT6 rows: 26,012
- source lines cross-checked: 19,166
- evidence agreement with original scripts: 100%
- fabricated source evidence: 0

The evidence format includes episode, scene, source line, entity, and quoted source fragment, for example `EP01-S01 L17 달재 (음! 알겠다는!)`.

## Immutability failure

The packages claimed zero modification to existing data, but an independent comparison found 239 modifications to pre-existing records. Therefore all previous claims of Stage01–04 immutability for those packages are invalid.

`개와늑대의시간` included severe violations:

- fixed CharacterArc codes such as `INTRO` and `LOSS` were replaced by prose
- a RelationshipArc meaning changed from `BOND` to `RIVALRY`
- a causal edge direction was reversed
- existing relationship records were deleted

## Binding decision

Accept only newly added EXT6 evidence files. Reject every attempted overwrite, deletion, reorder, schema conversion, enum substitution, edge-direction change, or semantic rewrite of existing Stage01–04 data.

### Required integration gate

1. Freeze hashes of every pre-existing file and record.
2. Permit writes only under new EXT6 namespaces.
3. Require zero modified, deleted, or reordered baseline records.
4. Preserve enum values and causal edge direction byte-for-byte.
5. Fail integration when any baseline hash changes.
6. Treat semantic reinforcement as a separate candidate patch, never as part of evidence-layer adoption.

Previous V1.2/V1.3 complete-package integration candidates for the six works are revoked. Only append-only EXT6 evidence subsets may be adopted.
