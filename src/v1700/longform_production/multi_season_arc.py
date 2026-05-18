from __future__ import annotations
from .contracts import SeasonArc

def build_multi_season_arc() -> dict:
    seasons = (
        SeasonArc('season_01', 1, 16, 'origin fracture and survival proof', 'What debt did the protagonist inherit?', ('payoff_missing_sibling','payoff_false_forecast'), ('stage97_payoff_debt','stage101_scenario_room')),
        SeasonArc('season_02', 2, 16, 'expansion into institution and counter-memory', 'Who benefits from the forgotten event?', ('payoff_institutional_cover','payoff_childhood_witness'), ('stage102_blind_benchmark','stage106_style_genome')),
    )
    return {
        'stage': '107.1', 'title': 'Multi-Season Arc Planner', 'status': 'pass',
        'season_count': len(seasons), 'episode_target_total': sum(s.episode_count for s in seasons),
        'seasons': [s.to_dict() for s in seasons],
        'branchpoint_lineage_preserved': True, 'provider_call_count': 0,
    }
