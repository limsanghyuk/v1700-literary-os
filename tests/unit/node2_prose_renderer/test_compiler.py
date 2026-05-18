from v1700.ir.scene_intent import SceneIntentIR, EmotionalDelta
from v1700.ir.style_profile import StyleProfileIR
from v1700.nodes.node2_prose_renderer import Node2ProseCompiler


def test_compiler_preserves_required_constraints():
    scene = SceneIntentIR(
        scene_id="t1",
        scene_goal="주인공이 조력자의 침묵을 의심한다",
        conflict="신뢰와 의심의 충돌",
        emotional_delta=EmotionalDelta("안도", "불신"),
        must_keep_facts=("조력자는 대답하지 않았다",),
        forbidden_reveals=("조력자가 범인",),
        timeline_position="D3_NIGHT",
        dialogue_seed="아직 말하지 않은 게 있지.",
        setting_seed="비가 그친 창문 아래, 컵 하나가 식어 있었다",
    )
    rendered = Node2ProseCompiler().compile(scene, StyleProfileIR()).rendered
    assert "조력자는 대답하지 않았다" in rendered.final_text
    assert "조력자가 범인" not in rendered.final_text
    assert not rendered.risk_flags
    assert rendered.surface_score["anti_llm"] >= 8.0
    assert rendered.constraint_score["reveal_preservation"] == 10.0
