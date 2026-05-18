
from pathlib import Path

from v1700.gates.stage84_release_gate import run_stage84_release_gate
from v1700.runtime_absorption import (
    ClosedLoopRenderer,
    KoreanAntiLLMFilter,
    LLMNodeRouter,
    StyleDNA,
    run_stage84_absorption_smoke,
)


def test_style_dna_and_anti_llm_filter_absorb_v370_surface_muscle():
    dna = StyleDNA()
    assert {"literary", "noir", "romance", "historical"}.issubset(set(dna.available_genres()))
    result = KoreanAntiLLMFilter("literary").filter("그 순간, 모든 것이 달라질 것만 같았다. 복잡한 감정이 밀려왔다.")
    assert result.n_cliches >= 2
    assert "그 순간, 모든 것이 달라질 것만 같았다" not in result.filtered
    assert result.score < 10.0


def test_closed_loop_renderer_preserves_provider_zero_and_node2_reveal_boundary(tmp_path: Path):
    renderer = ClosedLoopRenderer(trace_store=tmp_path)
    result = renderer.render(
        "조력자의 침묵이 우연이 아님을 드러낸다",
        "그 순간, 모든 것이 달라질 것만 같았다. 그는 복잡한 감정이 밀려왔다. 하지만 말하지 않았다.",
        genre_id="literary",
    )
    assert result.status == "pass"
    assert result.provider_default_calls == 0
    assert result.node2_raw_reveal_access_count == 0
    assert result.replacements
    assert len(result.anchors) >= 2
    assert renderer.collector.statistics()["total_records"] == 1
    assert (tmp_path / "stage84_trace_dataset.jsonl").exists()


def test_llm_node_router_uses_mock_by_default_even_when_external_provider_requested():
    router = LLMNodeRouter(allow_provider_calls=False)
    text = router.generate("draft", {}, provider="claude")
    assert text
    assert router.provider_default_calls == 0
    assert router.call_counts()["mock"] == 1


def test_stage84_absorption_smoke_and_release_gate_pass():
    smoke = run_stage84_absorption_smoke()
    assert smoke["status"] == "pass"
    assert smoke["stage80_hierarchy_preserved"] is True
    assert smoke["provider_default_calls"] == 0
    assert smoke["node2_raw_reveal_access_count"] == 0
    gate = run_stage84_release_gate()
    assert gate["status"] == "pass"
