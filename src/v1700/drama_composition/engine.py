from __future__ import annotations
from .contracts import (
    SeriesStory, MacroPlot, SupportingCharacter, SupportingCharacterWeb,
    MicroPlot, DramaScene, DramaSequence, DramaEpisodeComposition, KoreanDramaComposition,
)


class SeriesStoryComposer:
    def compose(self, prompt: str) -> SeriesStory:
        subject = prompt.strip() or "궁중과 민중 세계를 통과하는 주인공의 성장 드라마"
        return SeriesStory(
            premise=subject,
            initial_state="주인공은 세계의 규칙을 온전히 알지 못한 낮은 위치에서 출발한다.",
            final_state="주인공은 여러 제도와 관계장을 통과하며 자신의 윤리와 기능을 사회적 역할로 전환한다.",
            transformation="무력한 생존자에서 관계와 사건의 의미를 읽고 선택의 책임을 감당하는 인물로 변화한다.",
            story_question="한 인물은 시대와 제도의 압력 속에서 자신의 재능을 어떻게 사회적 책임으로 바꾸는가?",
        )


class MacroPlotArchitect:
    def architect(self, story: SeriesStory) -> tuple[MacroPlot, ...]:
        return (
            MacroPlot(
                macro_plot_id="MP01_APPRENTICESHIP_WORLD",
                title="첫 세계 진입과 규율의 학습",
                world_or_institution="닫힌 제도/직능 공동체",
                entry_condition="주인공은 낮은 지위로 들어와 규칙과 권력의 언어를 배운다.",
                core_pressure="재능과 규율, 생존과 윤리, 스승과 경쟁자의 압력이 동시에 작동한다.",
                identity_function="주인공의 원초적 재능이 처음으로 사회적 기술로 변환된다.",
                exit_condition="주인공은 기존 세계에서 밀려나거나 더 큰 세계로 추방된다.",
                series_story_function="전체 스토리의 출발점과 첫 정체성 획득을 담당한다.",
            ),
            MacroPlot(
                macro_plot_id="MP02_EXILE_RECOMPOSITION",
                title="추방과 재구성",
                world_or_institution="변방/민중/자연의 세계",
                entry_condition="주인공은 기존 제도에서 배제되어 생존 조건을 다시 배운다.",
                core_pressure="상실, 생존, 재학습, 다른 계층과의 접촉이 주인공을 다시 만든다.",
                identity_function="주인공은 제도 밖 지식과 감각을 흡수해 다른 기능을 획득한다.",
                exit_condition="새로운 능력이 주인공을 원래 세계와 다른 방식으로 재접속시킨다.",
                series_story_function="전체 스토리의 중간 변형과 반전된 학습을 담당한다.",
            ),
            MacroPlot(
                macro_plot_id="MP03_RETURN_WITH_NEW_FUNCTION",
                title="새 기능으로의 귀환과 최종 책임",
                world_or_institution="권력과 생명/진실이 충돌하는 중심 세계",
                entry_condition="주인공은 이전과 다른 전문성으로 중심 세계에 돌아온다.",
                core_pressure="권력, 생명 윤리, 과거 사건의 잔향, 주변 인물의 선택이 충돌한다.",
                identity_function="주인공은 개인 재능을 공동체적 판단과 책임으로 확장한다.",
                exit_condition="주인공의 변화가 세계의 질서와 관계망에 되돌릴 수 없는 흔적을 남긴다.",
                series_story_function="전체 스토리의 종착점과 처음-끝 변화를 완성한다.",
            ),
        )


class SupportingCharacterWebEngine:
    def build(self, macro_plots: tuple[MacroPlot, ...]) -> SupportingCharacterWeb:
        ids = tuple(plot.macro_plot_id for plot in macro_plots)
        characters = (
            SupportingCharacter("mentor_01", "스승", "재능을 알아보지만 쉽게 인정하지 않는다", "규율과 윤리를 부여", (ids[0],)),
            SupportingCharacter("rival_01", "경쟁자", "주인공의 재능을 위협으로 인식한다", "비교와 압박을 생성", (ids[0], ids[2])),
            SupportingCharacter("exile_witness_01", "변방의 조력자", "주인공을 제도 밖 지식과 연결한다", "재학습의 통로", (ids[1],)),
            SupportingCharacter("institutional_force_01", "권력 장치", "개인이 아닌 제도적 압력으로 대치한다", "거시 갈등 유지", ids),
            SupportingCharacter("hidden_beneficiary_01", "숨은 수혜자", "작은 사건의 결과를 뒤늦게 의미화한다", "미시 플롯과 전체 스토리 연결", (ids[1], ids[2])),
        )
        edges = (
            {"from": "mentor_01", "to": "rival_01", "relation": "shared_rule_conflict", "weight": 0.7},
            {"from": "rival_01", "to": "institutional_force_01", "relation": "instrumental_alignment", "weight": 0.8},
            {"from": "exile_witness_01", "to": "hidden_beneficiary_01", "relation": "delayed_causality", "weight": 0.6},
            {"from": "hidden_beneficiary_01", "to": "institutional_force_01", "relation": "unseen_cost", "weight": 0.5},
        )
        return SupportingCharacterWeb(characters=characters, relation_edges=edges)


class MicroPlotPlanner:
    def plan_for_episode(self, episode_id: str, macro_plot: MacroPlot, ordinal: int) -> tuple[MicroPlot, ...]:
        return (
            MicroPlot(
                micro_plot_id=f"{episode_id}_MPLOT01",
                macro_plot_id=macro_plot.macro_plot_id,
                function_in_episode="전체 스토리 변화가 작은 사건으로 감지되는 축",
                event_thread=f"{macro_plot.world_or_institution}에서 작은 규칙 위반이 발생한다.",
                character_thread="주변 인물이 주인공의 선택을 다르게 해석한다.",
                emotional_pressure="호기심→불안→결심",
                reveal_policy="정답 공개 금지, 사물과 행동으로만 암시",
            ),
            MicroPlot(
                micro_plot_id=f"{episode_id}_MPLOT02",
                macro_plot_id=macro_plot.macro_plot_id,
                function_in_episode="주변 인물 관계망이 주인공의 문제를 확대하는 축",
                event_thread="주변 인물의 사소한 선택이 제도적 압력과 연결된다.",
                character_thread="조력자, 경쟁자, 제도 권력이 각자 다른 목적을 보인다.",
                emotional_pressure="안도→의심→압박",
                reveal_policy="인물의 동기는 분산 제시, 핵심 비밀은 잠금",
            ),
            MicroPlot(
                micro_plot_id=f"{episode_id}_MPLOT03",
                macro_plot_id=macro_plot.macro_plot_id,
                function_in_episode="다음 화 또는 다음 거시 플롯으로 넘어갈 잔향을 남기는 축",
                event_thread="작은 사건의 결과가 당장 풀리지 않고 다음 국면의 빚으로 남는다.",
                character_thread="주인공은 해결보다 비용이 남는 선택을 한다.",
                emotional_pressure="압박→선택→잔향",
                reveal_policy="결과는 제시하되 원인은 유예",
            ),
        )


class SequenceComposer:
    def compose(self, episode_id: str, micro_plots: tuple[MicroPlot, ...]) -> tuple[DramaSequence, ...]:
        sequences: list[DramaSequence] = []
        for index, plot in enumerate(micro_plots, start=1):
            sid = f"{episode_id}_SEQ{index:02d}"
            scenes = (
                DramaScene(
                    scene_id=f"{sid}_SC01",
                    sequence_id=sid,
                    scene_function="미시 플롯의 표면 사건을 제시한다.",
                    dramatic_action=plot.event_thread,
                    character_relation_focus=plot.character_thread,
                    setting_pressure="공간의 규칙이 인물의 말을 제한한다.",
                    reveal_boundary=plot.reveal_policy,
                ),
                DramaScene(
                    scene_id=f"{sid}_SC02",
                    sequence_id=sid,
                    scene_function="관계 충돌과 감정 압력을 증폭한다.",
                    dramatic_action="사소한 선택이 다른 인물에게 비용으로 돌아간다.",
                    character_relation_focus="주인공과 주변 인물의 해석 차이가 드러난다.",
                    setting_pressure="사람들 앞에서 말할 수 없는 정보가 행동으로 새어 나온다.",
                    reveal_boundary="핵심 진실은 말하지 않고 반응만 남긴다.",
                ),
                DramaScene(
                    scene_id=f"{sid}_SC03",
                    sequence_id=sid,
                    scene_function="전체 스토리 또는 다음 시퀀스로 이어지는 잔향을 남긴다.",
                    dramatic_action="해결처럼 보이는 행동이 더 큰 국면의 원인이 된다.",
                    character_relation_focus="주변 인물의 선택이 주인공의 다음 행로를 바꾼다.",
                    setting_pressure="공간이 바뀌지 않아도 권력의 방향이 바뀐다.",
                    reveal_boundary="원인 유예, 결과만 고정",
                ),
            )
            sequences.append(DramaSequence(
                sequence_id=sid,
                micro_plot_id=plot.micro_plot_id,
                sequence_function=plot.function_in_episode,
                conflict_turn="표면 사건 → 관계 압력 → 다음 국면의 빚",
                emotional_turn=plot.emotional_pressure,
                scenes=scenes,
            ))
        return tuple(sequences)


class EpisodeCompositionMapper:
    def __init__(self) -> None:
        self.micro_planner = MicroPlotPlanner()
        self.sequence_composer = SequenceComposer()

    def map(self, story: SeriesStory, macro_plots: tuple[MacroPlot, ...]) -> tuple[DramaEpisodeComposition, ...]:
        episodes: list[DramaEpisodeComposition] = []
        episode_number = 1
        # 3 macro plots x 2 broadcast episodes = 6-episode composition map.
        for macro in macro_plots:
            for local in range(1, 3):
                eid = f"EP{episode_number:02d}"
                micro_plots = self.micro_planner.plan_for_episode(eid, macro, local)
                sequences = self.sequence_composer.compose(eid, micro_plots)
                episodes.append(DramaEpisodeComposition(
                    episode_id=eid,
                    macro_plot_id=macro.macro_plot_id,
                    episode_story_function=(
                        f"{macro.title} 국면에서 전체 스토리의 변화를 "
                        f"{local}번째 단계로 전진시킨다."
                    ),
                    whole_story_progress=(
                        "주인공의 처음-끝 변화 중 "
                        f"'{macro.identity_function}' 요소를 구체적 사건으로 증명한다."
                    ),
                    micro_plots=micro_plots,
                    sequences=sequences,
                ))
                episode_number += 1
        return tuple(episodes)


class KoreanDramaCompositionEngine:
    """Stage80 Korean drama story/macro-plot composition engine.

    This engine explicitly separates:
    Series Story != Macro Plot != Broadcast Episode != Micro Plot != Sequence != Scene.
    """
    def __init__(self) -> None:
        self.story_composer = SeriesStoryComposer()
        self.macro_architect = MacroPlotArchitect()
        self.character_web = SupportingCharacterWebEngine()
        self.episode_mapper = EpisodeCompositionMapper()

    def compose(self, prompt: str) -> KoreanDramaComposition:
        story = self.story_composer.compose(prompt)
        macro_plots = self.macro_architect.architect(story)
        web = self.character_web.build(macro_plots)
        episodes = self.episode_mapper.map(story, macro_plots)
        return KoreanDramaComposition(prompt=prompt, series_story=story, macro_plots=macro_plots, supporting_character_web=web, episodes=episodes)


def run_korean_drama_composition_smoke(prompt: str = "낮은 신분의 인물이 제도와 추방과 귀환을 통과하며 자기 역할을 완성하는 한국 드라마") -> dict:
    composition = KoreanDramaCompositionEngine().compose(prompt)
    return composition.to_dict()
