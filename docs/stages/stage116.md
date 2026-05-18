# Stage116 — Domain-Specific RAG Fusion

Stage116 adds the NIE domain-specific retrieval policy layer on top of Stage115. It classifies Korean drama queries without LLM calls, applies DramaLexicon BM25 boosts, and returns adaptive BM25/Dense/k settings for CHARACTER, EMOTIONAL, and PLOT_EVENT queries.

## Invariants

- QueryIntentClassifier LLM calls = 0
- embedding provider calls in release gate = 0
- provider default calls = 0
- Node2 raw reveal access = 0
- raw manuscript provider leakage = 0
- release gate and repo doctor must recognize Stage116

## Next

Stage117 — NarrativeTensionCurve.
