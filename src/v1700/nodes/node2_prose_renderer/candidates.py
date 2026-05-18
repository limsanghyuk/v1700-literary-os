from v1700.ir.scene_intent import SceneIntentIR
from v1700.ir.style_profile import StyleProfileIR

class ProseCandidateGenerator:
    def generate(self, scene: SceneIntentIR, style: StyleProfileIR, count: int = 3) -> list[str]:
        facts = " ".join(scene.must_keep_facts)
        base = (
            f"{scene.timeline_position}의 장면은 {scene.scene_goal}을 향해 움직인다. "
            f"갈등은 {scene.conflict}에 걸려 있었다. "
            f"{scene.emotional_delta.from_state}에서 {scene.emotional_delta.to_state}로 기울어지는 동안, "
            f"인물은 대답보다 늦은 숨으로 먼저 반응했다. {facts}"
        ).strip()
        variant_a = base
        variant_b = (
            f"{scene.timeline_position}. {scene.scene_goal}. "
            f"{scene.conflict}은 말보다 먼저 방 안의 정적에 걸렸다. "
            f"{scene.emotional_delta.from_state}은 아직 남아 있었고, {scene.emotional_delta.to_state}는 컵의 그림자처럼 천천히 번졌다. {facts}"
        ).strip()
        variant_c = (
            f"그들은 {scene.timeline_position}에 같은 자리에 있었지만 같은 쪽을 보지 않았다. "
            f"{scene.scene_goal}이라는 목적은 드러나지 않은 채, {scene.conflict}만 식탁 위에 남았다. {facts}"
        ).strip()
        return [variant_a, variant_b, variant_c][:count]
