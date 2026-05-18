from __future__ import annotations

def score_results(benchmark: dict) -> dict:
    scores = []
    for item in benchmark.get('results', []):
        mode = item.get('mode')
        provider = item.get('provider_id')
        base = 82.0 if mode == 'PROSE' else 80.0
        delta = {'openai': 3.5, 'anthropic': 3.0, 'gemini': 2.5, 'ollama': 1.5}.get(provider, 0.0)
        v1700_delta = 4.0 if mode == 'SCENARIO' else 3.0
        scores.append({'seed_id': item.get('seed_id'), 'provider_id': provider, 'mode': mode, 'score_total': round(base + delta + v1700_delta, 2), 'v1700_improvement_delta': v1700_delta, 'score_breakdown': {'structure': 8.6, 'style': 8.3, 'safety': 10.0, 'longform_fit': 8.8}, 'reviewer_notes': ['fixture-level scoring for sandbox contract validation']})
    return {'stage':'107.5.4','title':'V1700 Arbitration Comparison','status':'pass','score_count':len(scores),'scores':scores,'comparison_claim':'contract_level_fixture_scoring_not_human_benchmark'}
