# Kill Me Heal Me vs Stove League Quality Comparison Handoff

Date: 2026-07-15  
Status: LOCAL VERIFIED / HUB EVIDENCE HANDOFF  
Scope: Stage01-04 package quality comparison

## Task

The local Codex environment compared the `킬미힐미` and `스토브리그` analysis packages in the supplied SeqCard archive. The comparison applied the current Stage01-04 schema, causality, validation, lineage, and release rules in this repository.

## Method

1. Verified the source ZIP by SHA256, entry count, and CRC.
2. Parsed every relevant JSON and JSONL file for both works: 301 files, zero parse errors.
3. Measured Stage01-04 coverage, ID integrity, edge validity, candidate disposition, field diversity, and provenance evidence.
4. Reviewed early, middle, and late episodes across SceneCard, SequenceBlueprint, CharacterArc, RelationshipArc, LocalEdge, PayoffCandidate, CrossEpisodeEdge, and FullSeriesArc layers.
5. Checked the supplied method-review DOCX and the current authority documents in the hub.
6. Exported aggregate metadata only. No script, dialogue, authored row, vector, key, or model artifact was loaded into GitHub.

## Result

`킬미힐미` is the preferred current reference package. It satisfies the current structural contracts, has episode-qualified Stage03 IDs, contains no invalid local/cross edge references, disposes all 60 Stage04 payoff candidates, and includes SourceLock plus work-level strong-validation lineage with zero reported errors and warnings.

`스토브리그` remains semantically useful, particularly for ensemble breadth, but is blocked under the current contract. Required repairs are 964 episode-qualified Stage03 work IDs, 16 cross-episode bridges incorrectly stored as local edges, disposition of 83 payoff candidates, SourceLock creation, current strong validation, and lineage/supersession recording.

This comparison does not grant canonical status, promotion, or provider/model superiority.

## Hub Artifacts To Load

- `docs/drama_analysis/results/KILLME_VS_STOVE_QUALITY_COMPARISON_2026-07-15.md`
- `docs/drama_analysis/results/KILLME_VS_STOVE_QUALITY_METRICS_2026-07-15.json`
- `docs/drama_analysis/results/KILLME_VS_STOVE_QUALITY_GATE_RESULT_2026-07-15.json`
- `docs/drama_analysis/results/KILLME_VS_STOVE_EVIDENCE_MANIFEST_2026-07-15.json`
- `tools/compare_seqcard_works.py`

## ChatGPT Design Use

- Treat `킬미힐미` as the stronger current Stage01-04 reference example.
- Place `스토브리그` in the rework queue; do not treat file-presence completion as current-contract readiness.
- Preserve its ensemble and relationship breadth while rebuilding its Stage03/04 compliance evidence.
- Do not change the current schemas solely because this older package uses different identifiers or local-edge conventions.
- Do not advance promotion or canonical claims from this comparison.

## Local And Hub Boundary

The source ZIP, extracted database rows, raw scripts, dialogue, and DOCX were inspected locally and remain local. GitHub receives only the comparison report, aggregate metrics, gate result, evidence manifest, and metadata-only reproduction tool.
