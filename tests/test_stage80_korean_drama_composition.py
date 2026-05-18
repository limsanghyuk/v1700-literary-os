from v1700.drama_composition import KoreanDramaCompositionEngine, DramaCompositionGate
from v1700.gates.stage80_release_gate import run_stage80_release_gate


def test_stage80_separates_story_macro_plot_episode_micro_plot_sequence_scene():
    composition = KoreanDramaCompositionEngine().compose("한 인물이 세 세계를 통과하며 자기 역할을 완성하는 한국 드라마")
    assert "SeriesStory != MacroPlot" in composition.hierarchy_claim
    assert len(composition.macro_plots) >= 3
    assert len(composition.episodes) >= 6
    assert composition.episodes[0].macro_plot_id == composition.macro_plots[0].macro_plot_id
    assert len(composition.episodes[0].micro_plots) >= 3
    assert len(composition.episodes[0].sequences) >= len(composition.episodes[0].micro_plots)
    assert len(composition.episodes[0].sequences[0].scenes) >= 3


def test_stage80_supporting_character_web_is_not_flat_protagonist_antagonist_only():
    composition = KoreanDramaCompositionEngine().compose("주변 인물 관계망이 중요한 한국 드라마")
    web = composition.supporting_character_web
    assert len(web.characters) >= 5
    roles = {c.role for c in web.characters}
    assert "스승" in roles
    assert "경쟁자" in roles
    assert "권력 장치" in roles
    assert len(web.relation_edges) >= 4


def test_stage80_composition_gate_passes():
    composition = KoreanDramaCompositionEngine().compose("거시 플롯과 미시 플롯을 분리하는 한국 드라마")
    result = DramaCompositionGate().validate(composition)
    assert result["status"] == "pass"
    assert result["macro_plot_count"] >= 3
    assert result["broadcast_episode_count"] >= 6
    assert result["scene_count"] >= 54


def test_stage80_release_gate_passes():
    result = run_stage80_release_gate()
    assert result["status"] == "pass"
    assert result["korean_drama_composition_gate"]["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access_count"] == 0
