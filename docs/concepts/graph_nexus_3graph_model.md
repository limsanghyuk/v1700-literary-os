# GraphNexus Three-Graph Model

GraphNexus is the Stage72.1 graph orchestration layer:

```text
GraphNexus = CodeGraph + NarrativeGraph + StageLineageGraph
```

- `CodeGraph` indexes live source files, definitions, imports, tests, and gates.
- `NarrativeGraph` indexes scene intent, forbidden reveal labels, motifs, and scene flow.
- `StageLineageGraph` preserves stage concepts and survival status.

The model is intentionally lightweight and deterministic so release gates work in local-first environments.
