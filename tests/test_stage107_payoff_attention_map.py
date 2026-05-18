from v1700.longform_production.payoff_calendar import build_payoff_calendar
from v1700.longform_production.attention_heatmap import build_attention_heatmap
from v1700.longform_production.production_scene_mapping import build_production_scene_mapping


def test_stage107_payoff_attention_and_mapping_are_feature_only():
    payoff = build_payoff_calendar()
    attention = build_attention_heatmap()
    scene_map = build_production_scene_mapping()
    assert payoff["status"] == "pass"
    assert attention["status"] == "pass"
    assert scene_map["status"] == "pass"
    assert scene_map["raw_manuscript_required"] is False
    assert attention["heat_point_count"] == 32
