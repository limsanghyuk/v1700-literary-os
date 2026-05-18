from v1700.ir.scene_intent import SceneIntentIR
from v1700.ir.style_profile import StyleProfileIR

AXIS_TO_ANCHOR = {
    "light": "천장의 불빛이 컵 표면에서 잘게 흔들렸다.",
    "temperature": "창가의 찬기가 손등에 얇게 남았다.",
    "object_texture": "접힌 종이의 모서리가 손톱 밑을 스쳤다.",
    "sound": "복도 끝에서 엘리베이터가 한 번 낮게 울렸다.",
}

class SensoryAnchorInjector:
    def inject(self, text: str, scene: SceneIntentIR, style: StyleProfileIR) -> str:
        anchors = []
        if scene.setting_seed:
            anchors.append(scene.setting_seed.rstrip(".。") + ".")
        for axis in style.sensory_axis[:2]:
            anchor = AXIS_TO_ANCHOR.get(axis)
            if anchor:
                anchors.append(anchor)
        if not anchors:
            return text
        return text.rstrip() + "\n\n" + " ".join(anchors)

    def score(self, text: str) -> float:
        markers = ["불빛", "찬기", "종이", "손등", "소리", "컵", "문틈", "온도"]
        hits = sum(1 for m in markers if m in text)
        return min(10.0, 7.2 + hits * 0.35)
