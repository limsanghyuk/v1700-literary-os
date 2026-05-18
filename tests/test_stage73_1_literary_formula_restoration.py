from pathlib import Path

from v1700.gates.drse_quality_gate import run_drse_quality_gate
from v1700.gates.literary_formula_survival_gate import run_literary_formula_survival_gate
from v1700.gates.stage73_1_release_gate import run_stage73_1_release_gate
from v1700.graph_nexus.narrative_graph import NarrativeGraph
from v1700.ir.scene_intent import EmotionalDelta, SceneIntentIR
from v1700.literary_formulas import (
    DRSEEngine,
    DRSEInputNode,
    EmotionalMomentumTracker,
    MiseEnSceneCompiler,
    SceneGraphQueryEngine,
)

ROOT = Path(__file__).resolve().parents[1]


def test_drse_scores_causality_emotion_and_residue_without_provider_calls():
    nodes = (
        DRSEInputNode("n1", "causality", "과거 사건의 결과", ("causal",), ("stage39",)),
        DRSEInputNode("n2", "emotion", "불신의 감정선", ("emotion",), ("stage56",)),
        DRSEInputNode("n3", "residue", "복선 잔향", ("residue", "reveal"), ("stage52",)),
    )
    context = DRSEEngine().score("과거 사건과 불신이 현재 선택을 압박한다", nodes)

    assert context.provider_default_calls == 0
    assert len(context.scores) == 3
    assert context.top_scores(1)[0].final_score > 0
    assert context.to_surface_directives()


def test_scene_graph_query_and_mise_en_scene_projection_remain_surface_safe():
    scene = SceneIntentIR(
        scene_id="S74_SCENE",
        scene_goal="조력자의 침묵을 의심한다",
        conflict="신뢰와 불신의 충돌",
        emotional_delta=EmotionalDelta("안도", "불신"),
        forbidden_reveals=("조력자가 범인",),
        setting_seed="식은 컵",
    )
    graph = NarrativeGraph.from_scene_intents([scene])
    focus = SceneGraphQueryEngine().focus(graph, scene.scene_id)
    context = DRSEEngine().score(scene.scene_goal, focus.nodes)
    momentum = EmotionalMomentumTracker().from_scene_terms(scene.conflict, "안도", "불신")
    directive = MiseEnSceneCompiler().compile(scene.scene_id, context, momentum)

    assert focus.relation_count >= 1
    assert momentum.dread >= 0.2
    assert directive.to_surface_packet_hints()
    assert "조력자가 범인" not in " ".join(directive.to_surface_packet_hints())


def test_stage73_1_gates_pass():
    formula = run_literary_formula_survival_gate(ROOT)
    drse = run_drse_quality_gate(ROOT)
    release = run_stage73_1_release_gate(ROOT)

    assert formula["status"] == "pass"
    assert drse["status"] == "pass"
    assert release["status"] == "pass"
    assert release["provider_default_calls"] == 0
    assert release["node2_raw_reveal_access_count"] == 0
