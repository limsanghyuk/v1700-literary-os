from __future__ import annotations
from .multi_season_arc import build_multi_season_arc
from .production_calendar import build_production_calendar
from .character_memory_evolution import build_character_memory_evolution
from .payoff_calendar import build_payoff_calendar
from .attention_heatmap import build_attention_heatmap
from .production_scene_mapping import build_production_scene_mapping
from .release_policy import build_longform_production_release_policy

def run_longform_production_suite() -> dict:
    arc = build_multi_season_arc()
    calendar = build_production_calendar()
    memory = build_character_memory_evolution()
    payoff = build_payoff_calendar()
    attention = build_attention_heatmap()
    scene_map = build_production_scene_mapping()
    policy = build_longform_production_release_policy()
    reports = {'multi_season_arc':arc,'production_calendar':calendar,'character_memory_evolution':memory,'payoff_calendar':payoff,'attention_heatmap':attention,'production_scene_mapping':scene_map,'release_policy':policy}
    issues = [name for name, report in reports.items() if report.get('status') != 'pass']
    return {'stage':'107','baseline_stage':'106','title':'Longform Production Suite','status':'pass' if not issues else 'blocked','issues':issues, **reports, 'provider_default_calls':0,'live_provider_call_count_in_release_gate':0,'raw_manuscript_provider_leakage':0,'node2_raw_reveal_access':0,'credential_leakage':0,'full_text_export_default':False}
