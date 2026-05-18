from v1700.ir.scene_intent import SceneIntentIR, EmotionalDelta

class Node1Architect:
    def make_scene(self, prompt: str) -> SceneIntentIR:
        return SceneIntentIR(
            scene_id="example_scene_001",
            scene_goal=prompt or "주인공이 조력자의 침묵을 처음 의심한다",
            conflict="신뢰와 의심의 충돌",
            emotional_delta=EmotionalDelta("안도", "미세한 불신"),
            must_keep_facts=("조력자는 대답하지 않았다",),
            forbidden_reveals=("조력자가 범인",),
            timeline_position="D3_NIGHT",
            dialogue_seed="아직 말하지 않은 게 있지.",
            setting_seed="비가 그친 창문 아래, 컵 하나가 식어 있었다",
        )
