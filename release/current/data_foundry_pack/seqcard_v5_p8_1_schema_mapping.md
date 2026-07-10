# SeqCard v5 To P8.1 Schema Mapping

Date: 2026-07-05

## New Data Layers

```text
authored/*.seqcard.jsonl: 648 episode files, 41168 scene records
authored_arc/*.episodearc.json: 648 episode arc files
authored_seq/*.seqblueprint.jsonl: 648 episode sequence blueprint files, 6146 sequence records
```

## Purpose

SeqCard v5 is useful for P8.1 because it adds EpisodeArc and SequenceBlueprint layers. These support cross-level integrity checks from season/episode/sequence/scene metadata without exporting raw drama text.

## Boundary

```text
can_strengthen_full_season_validation: true
can_replace_missing_p8_1_candidate_files: false
P8.1 validation still requires the four full_season_* input files from the hub.
P9 Scorecard remains blocked.
Gate A remains not ready.
```
