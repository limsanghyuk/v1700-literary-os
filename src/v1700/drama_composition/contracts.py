from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class SeriesStory:
    """전체 스토리: 작품 처음과 끝의 총체적 변화 궤적."""
    premise: str
    initial_state: str
    final_state: str
    transformation: str
    story_question: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class MacroPlot:
    """거시 플롯: 전체 스토리를 구성하는 장기 국면/세계/제도/관계장."""
    macro_plot_id: str
    title: str
    world_or_institution: str
    entry_condition: str
    core_pressure: str
    identity_function: str
    exit_condition: str
    series_story_function: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class SupportingCharacter:
    character_id: str
    role: str
    relation_to_protagonist: str
    pressure_function: str
    macro_plot_ids: tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "character_id": self.character_id,
            "role": self.role,
            "relation_to_protagonist": self.relation_to_protagonist,
            "pressure_function": self.pressure_function,
            "macro_plot_ids": list(self.macro_plot_ids),
        }


@dataclass(frozen=True)
class SupportingCharacterWeb:
    characters: tuple[SupportingCharacter, ...]
    relation_edges: tuple[dict, ...]

    def to_dict(self) -> dict:
        return {
            "characters": [item.to_dict() for item in self.characters],
            "relation_edges": list(self.relation_edges),
        }


@dataclass(frozen=True)
class MicroPlot:
    """한 화 내부에서 작동하는 미시적 사건/감정/관계 플롯."""
    micro_plot_id: str
    macro_plot_id: str
    function_in_episode: str
    event_thread: str
    character_thread: str
    emotional_pressure: str
    reveal_policy: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class DramaScene:
    scene_id: str
    sequence_id: str
    scene_function: str
    dramatic_action: str
    character_relation_focus: str
    setting_pressure: str
    reveal_boundary: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class DramaSequence:
    sequence_id: str
    micro_plot_id: str
    sequence_function: str
    conflict_turn: str
    emotional_turn: str
    scenes: tuple[DramaScene, ...]

    def to_dict(self) -> dict:
        return {
            "sequence_id": self.sequence_id,
            "micro_plot_id": self.micro_plot_id,
            "sequence_function": self.sequence_function,
            "conflict_turn": self.conflict_turn,
            "emotional_turn": self.emotional_turn,
            "scenes": [scene.to_dict() for scene in self.scenes],
        }


@dataclass(frozen=True)
class DramaEpisodeComposition:
    """방영 화/장 단위. 전체 스토리의 일부를 특정 거시 플롯 안에서 전진시킨다."""
    episode_id: str
    macro_plot_id: str
    episode_story_function: str
    whole_story_progress: str
    micro_plots: tuple[MicroPlot, ...]
    sequences: tuple[DramaSequence, ...]

    def to_dict(self) -> dict:
        return {
            "episode_id": self.episode_id,
            "macro_plot_id": self.macro_plot_id,
            "episode_story_function": self.episode_story_function,
            "whole_story_progress": self.whole_story_progress,
            "micro_plots": [plot.to_dict() for plot in self.micro_plots],
            "sequences": [sequence.to_dict() for sequence in self.sequences],
        }


@dataclass(frozen=True)
class KoreanDramaComposition:
    prompt: str
    series_story: SeriesStory
    macro_plots: tuple[MacroPlot, ...]
    supporting_character_web: SupportingCharacterWeb
    episodes: tuple[DramaEpisodeComposition, ...]
    hierarchy_claim: str = "SeriesStory != MacroPlot != BroadcastEpisode != MicroPlot != Sequence != Scene"

    def to_dict(self) -> dict:
        return {
            "prompt": self.prompt,
            "hierarchy_claim": self.hierarchy_claim,
            "series_story": self.series_story.to_dict(),
            "macro_plots": [plot.to_dict() for plot in self.macro_plots],
            "supporting_character_web": self.supporting_character_web.to_dict(),
            "episodes": [episode.to_dict() for episode in self.episodes],
        }
