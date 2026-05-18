from __future__ import annotations
from .contracts import AttentionHeatPoint

def build_attention_heatmap() -> dict:
    points = []
    for ep in range(1, 33):
        fatigue = round(0.18 + (ep % 6) * 0.055, 3)
        curiosity = round(0.86 - fatigue * 0.25 + (0.04 if ep in {8,16,24,32} else 0), 3)
        action = 'payoff pulse' if ep in {8,16,24,32} else 'pressure relief' if fatigue > 0.43 else 'sustain tension'
        points.append(AttentionHeatPoint(f'episode_{ep:02d}', curiosity, fatigue, action))
    return {'stage':'107.4b','title':'Reader Attention Heatmap','status':'pass','heat_point_count':len(points),'max_fatigue_score':max(p.fatigue_score for p in points),'points':[p.to_dict() for p in points],'provider_call_count':0}
