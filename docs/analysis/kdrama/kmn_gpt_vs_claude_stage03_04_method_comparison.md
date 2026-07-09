# Stage03~04 Method Comparison — GPT Clean Direct-Reading Rebuild vs Claude Expanded Analysis

## Scope

This report is included as a separate layer because the user requested the difference between Claude's expanded analysis method and this GPT direct-reading-derived method.

## Shared target schema

Both methods converge on the same Stage03~04 target objects:

- SeriesArc
- CharacterArc
- RelationshipArc
- LocalEdge
- CrossEpisodeEdge
- PayoffCandidate
- season_wiring_graph
- payoff_setup_closure_matrix
- episode_role_map
- tension_role_curve
- character_relation_closure_report

## Claude expanded method — comparative reference

Claude's expanded mode is stronger as a corpus-expansion and schema-expansion pattern. It emphasizes:

1. explicit EdgeLayer / CharacterArc / RelationshipArc schema expansion;
2. reusable ID namespace discipline;
3. anti-gaming validation for new layer labels and FK consistency;
4. cross-work comparability from Secret Forest / My Name Is Kim Sam Soon style outputs;
5. direct support for broader corpus pipelines.

Its risk is that it can look structurally complete even when lower-layer scene semantics are shallow unless the Stage01/02 input is audited first.

## GPT clean direct-reading-derived method — applied here

This package applies a stricter input-authorship gate before creating Stage03~04:

1. Stage03 is derived only from Stage01 SceneCard and Stage02 SequenceBlueprint metadata;
2. EP14~EP16 contaminated inputs were rejected and replaced with clean rewrite canonical ZIPs;
3. raw script export is blocked;
4. provider generation count is fixed at zero;
5. Stage03 references scene/sequence IDs, not raw text;
6. Stage04 cannot claim closure unless the payoff candidate has setup and closure references;
7. method comparison is separated from canonical outputs so it does not pollute schema data.

## Practical difference

| Area | Claude expanded method | GPT method in this package |
|---|---|---|
| Primary strength | broad schema/corpus expansion | strict direct-reading provenance and contamination rejection |
| Stage03 creation | expansion-first edge/arc modeling | Stage01/02 evidence-first edge/arc modeling |
| Failure prevention | anti-gaming schema checks | input contamination scan + schema checks |
| Best use | many-work comparative corpus | canonical single-work season wiring |
| Risk | structure may outrun semantic depth | slower, more conservative, less aggressively expansive |

## Integration decision

The final recommended standard is hybrid:

```text
Claude-style expanded schema discipline
+ GPT-style direct-reading provenance and fail-closed input audit
= canonical Stage03~04 operating protocol
```

For this package, the canonical outputs follow the GPT clean direct-reading-derived method while preserving the Claude-compatible object families and ID discipline.
