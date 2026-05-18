from __future__ import annotations

from v1700.ir.scene_intent import EmotionalDelta, SceneIntentIR
from .contracts import EpisodePlan, LongformPlan, SequencePlan


class MacroStructurePlanner:
    def plan(self, prompt: str) -> tuple[str, tuple[str, str, str]]:
        subject = prompt.strip() or "침묵한 조력자와 늦게 밝혀지는 진실"
        arc = f"{subject}를 인물의 신뢰 붕괴와 회복 불가능한 선택으로 밀어붙이는 시즌 아크"
        proof = (
            "1막: 관계의 균열을 작은 행동과 누락된 대답으로 증명한다.",
            "2막: 과거 사건의 잔향이 현재 선택을 압박한다.",
            "3막: reveal은 폭로가 아니라 돌이킬 수 없는 행동의 결과로 도착한다.",
        )
        return arc, proof


class TrilogyEpisodePlanner:
    def plan(self, prompt: str, season_arc: str) -> tuple[EpisodePlan, ...]:
        templates = (
            ("EP01", "균열의 첫 장면", "주인공은 조력자의 침묵이 우연이 아님을 감지한다."),
            ("EP02", "잔향의 역류", "과거 사건의 흔적이 현재의 동선을 바꾼다."),
            ("EP03", "선택의 비용", "관계는 회복이 아니라 비용 지불로 종결된다."),
        )
        return tuple(
            EpisodePlan(
                episode_id=eid,
                title=title,
                major_turn=turn,
                sequences=(
                    SequencePlan(f"{eid}_SQ01", "표면 목표를 세운다", "말하지 않은 사실과 현재 행동의 충돌", "안도→의심", "핵심 reveal 금지"),
                    SequencePlan(f"{eid}_SQ02", "관계 압력을 높인다", "보호하려는 말과 추적하려는 행동의 충돌", "의심→불신", "복선은 사물로만 남김"),
                    SequencePlan(f"{eid}_SQ03", "행동 결과를 남긴다", "선택과 회피의 충돌", "불신→결심", "정답 공개 금지"),
                ),
            )
            for eid, title, turn in templates
        )


class LongformPlanBuilder:
    def build(self, prompt: str) -> LongformPlan:
        season_arc, proof = MacroStructurePlanner().plan(prompt)
        episodes = TrilogyEpisodePlanner().plan(prompt, season_arc)
        return LongformPlan(prompt=prompt, season_arc=season_arc, trilogy_proof=proof, episodes=episodes)


class SceneExpansionEngine:
    def expand_first_scenes(self, plan: LongformPlan) -> tuple[SceneIntentIR, ...]:
        scenes: list[SceneIntentIR] = []
        for episode in plan.episodes:
            sequence = episode.sequences[0]
            scenes.append(
                SceneIntentIR(
                    scene_id=f"{episode.episode_id}_SC01",
                    scene_goal=f"{episode.major_turn} {sequence.objective}",
                    conflict=sequence.conflict,
                    emotional_delta=EmotionalDelta("안도", "불신"),
                    must_keep_facts=("조력자는 결정적인 질문에 대답하지 않았다", episode.major_turn),
                    forbidden_reveals=("조력자가 범인", "최종 비밀의 이름"),
                    timeline_position=f"{episode.episode_id}_NIGHT",
                    character_state_refs=("protagonist:trust_fracture", "ally:withheld_answer"),
                    dialogue_seed="아직 말하지 않은 게 있지.",
                    setting_seed="비가 그친 창문 아래, 컵 하나가 식어 있었다",
                )
            )
        return tuple(scenes)
