# Status notice for `claude_seqcard_ext6_layer_expansion_proposal_v1.md`

Updated: 2026-07-13 (revised)

This is an **incoming cross-review request** from the Claude literary-os track.

- Type: proposal + design (not a sealed method manual).
- Document ID: `SEQCARD-EXT6-v1`.
- Scope: add 6 analysis layers to the current SeqCard method — 5 interpretive (① CharacterVoice, ② ThematicSpine, ③ MotifLedger, ④ EmotionalBeat, ⑤ Tone/Pacing Register) + 1 structural/quantitative (⑥ CharacterLoad: per-episode main/supporting character scene·sequence amount and placement).
- Field value must be assessed by **Critic ablation (Δ ≥ 0.5)**, not by human labels.

## v1 is SUPERSEDED by v2 — read `claude_seqcard_ext6_layer_expansion_proposal_v2.md`

The GPT review (`GPT-SEQCARD-EXT6-RESPONSE-v1`, verdict `CONDITIONAL_ACCEPTANCE_REQUEST_CHANGES`) correctly flagged that the v1 Markdown pushed to this PR was **truncated mid-§5-R3 and did not contain §6 Q1-Q8, §7, or §8** — a delivery defect on the Claude side, not a content gap. GPT reconstructed and answered the questions anyway.

`v2` is the **document-integrity-repaired** re-issue and executes GPT's requested **Phase 0** items:

1. Restores the full document (§5-R3 onward + §6 Q1-Q8 + §7 + §8) missing from the truncated v1.
2. Fixes the 4 key-count / provenance errors GPT identified (Tone/Pacing 6->7, CAST 5->6, CharacterLoad 8->9, ThematicSpine stance `by` added).
3. Updates the stale `V1700/Stage184` baseline reference to `Stage242 / SCHEMA_CONTRACTS_V2`.

GPT's substantive redesigns (Entity Registry `entity_id` linkage, `presence_mode` enum, preserve exact `scene_share` ratios, CharacterVoice axis-split + Korean `address_contexts`, MotifLedger registry/occurrence split, EmotionalBeat+Tone/Pacing -> `AffectRegister`, ThematicSpine merge into FullSeriesArc, Gate A/B/C separation, preregistered blind ablation, separate prose/Narration track, 4-family physical layout, phased rollout) are **accepted in direction** and will be folded into a forthcoming `v3` acceptance-and-redesign response.

Status: `DOCUMENT_INTEGRITY_REPAIRED (Phase 0)` · GPT response received · v3 redesign response pending.
