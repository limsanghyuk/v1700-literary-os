from v1700.nodes.node1_architect import Node1Architect
from v1700.nodes.node2_prose_renderer import Node2ProseCompiler
from v1700.nodes.node3_critic_gate import Node3CriticGate
from v1700.ir.style_profile import StyleProfileIR


def test_node1_node2_node3_pipeline_passes():
    scene = Node1Architect().make_scene("주인공이 조력자의 침묵을 처음 의심한다")
    rendered = Node2ProseCompiler().compile(scene, StyleProfileIR()).rendered
    ok, issues = Node3CriticGate().validate(rendered)
    assert ok, issues
