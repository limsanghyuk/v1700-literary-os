from __future__ import annotations

def build_cost_latency_ledger(benchmark: dict) -> dict:
    rows = []
    for item in benchmark.get('results', []):
        result = item.get('result', {})
        rows.append({'provider_id': item.get('provider_id'), 'mode': item.get('mode'), 'latency_ms': result.get('latency_ms', 0), 'estimated_cost': result.get('estimated_cost'), 'live_call_performed': result.get('live_call_performed', False)})
    return {'status':'pass','rows':rows,'live_call_count':sum(1 for r in rows if r['live_call_performed']),'estimated_total_cost':0.0}
