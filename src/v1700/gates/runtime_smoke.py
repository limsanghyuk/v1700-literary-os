from v1700.runtime.profile import RuntimeProfile
from v1700.nodes.node1_architect import Node1Architect
from v1700.nodes.node2_prose_renderer import Node2ProseCompiler
from v1700.nodes.node3_critic_gate import Node3CriticGate
from v1700.ir.style_profile import StyleProfileIR

def run_runtime_smoke() -> dict:
    RuntimeProfile().assert_local_first()
    scene = Node1Architect().make_scene("주인공이 조력자의 침묵을 처음 의심한다")
    rendered = Node2ProseCompiler().compile(scene, StyleProfileIR()).rendered
    ok, issues = Node3CriticGate().validate(rendered)
    return {"status": "pass" if ok else "blocked", "issues": issues, "scene_id": rendered.scene_id, "external_provider_calls": 0}
