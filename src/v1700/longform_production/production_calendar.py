from __future__ import annotations
from .contracts import ProductionEpisode

def build_production_calendar() -> dict:
    episodes = []
    for season_idx in (1, 2):
        season_id = f'season_{season_idx:02d}'
        for ep in range(1, 17):
            global_ep = (season_idx - 1) * 16 + ep
            episodes.append(ProductionEpisode(
                episode_id=f'episode_{global_ep:02d}', season_id=season_id, episode_index=global_ep,
                target_scene_count=10, production_window=f'week_{global_ep:02d}',
                narrative_function='setup' if ep <= 4 else 'escalation' if ep <= 12 else 'payoff cascade',
                attention_budget=round(0.74 + (ep % 4) * 0.035, 3), payoff_due_count=1 if ep in {4, 8, 12, 16} else 0,
            ))
    return {'stage':'107.2','title':'Longform Production Calendar','status':'pass','episode_count':len(episodes),'scene_target_total':sum(e.target_scene_count for e in episodes),'episodes':[e.to_dict() for e in episodes],'provider_call_count':0}
