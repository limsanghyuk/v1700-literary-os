from pathlib import Path
from v1700.stage107.orchestrator import run_stage107

def test_stage107_longform_production_suite_passes():
    report = run_stage107(Path(__file__).resolve().parents[1])
    assert report['status'] == 'pass'
    assert report['stage107_1_multi_season_arc']['season_count'] >= 2
    assert report['stage107_2_production_calendar']['episode_count'] >= 32
    assert report['stage107_4_payoff_attention_map']['production_scene_mapping']['production_scene_total'] >= 320
    assert report['provider_default_calls'] == 0
