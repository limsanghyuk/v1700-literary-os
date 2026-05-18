from __future__ import annotations

from dataclasses import dataclass

from .drse import DRSEContext
from .emotional_momentum import EmotionalMomentumVector


@dataclass(frozen=True)
class MiseEnSceneDirective:
    scene_id: str
    sensory_directives: tuple[str, ...]
    spatial_pressure: str
    emotional_temperature: str
    drse_surface_directives: tuple[str, ...]

    def to_surface_packet_hints(self) -> tuple[str, ...]:
        return tuple((*self.sensory_directives, self.spatial_pressure, self.emotional_temperature, *self.drse_surface_directives))

    def to_dict(self) -> dict:
        return {
            "scene_id": self.scene_id,
            "sensory_directives": list(self.sensory_directives),
            "spatial_pressure": self.spatial_pressure,
            "emotional_temperature": self.emotional_temperature,
            "drse_surface_directives": list(self.drse_surface_directives),
        }


class MiseEnSceneCompiler:
    def compile(self, scene_id: str, drse: DRSEContext, momentum: EmotionalMomentumVector) -> MiseEnSceneDirective:
        intensity = momentum.intensity()
        spatial = "인물 사이의 거리를 한 박자 늦게 드러낸다." if intensity >= 0.45 else "공간은 낮게 고정하고 사물의 위치로 긴장을 유지한다."
        temperature = "찬기와 건조한 표면으로 감정을 간접화한다." if momentum.dread >= momentum.sympathy else "빛과 손의 지연된 움직임으로 감정을 간접화한다."
        sensory = (
            "손끝·컵·문틈 같은 작은 물체를 감정의 앵커로 사용한다.",
            "대사보다 침묵과 시선의 방향을 먼저 배치한다.",
        )
        return MiseEnSceneDirective(
            scene_id=scene_id,
            sensory_directives=sensory,
            spatial_pressure=spatial,
            emotional_temperature=temperature,
            drse_surface_directives=drse.to_surface_directives(),
        )
