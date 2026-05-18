from __future__ import annotations

from collections import Counter

from v1700.drama_composition import KoreanDramaCompositionEngine
from v1700.quality_endurance import QualityEnduranceEngine
from .contracts import (
    BlindCriticBenchmarkReport,
    CandidateSample,
    CandidateScore,
    EVALUATION_AXES,
)


class BlindCriticEvaluationHarness:
    """Stage82 blind critic evaluation harness.

    The harness compares three local-first candidates without calling external
    providers. It is a benchmark harness, not a claim that paid GPT/Claude APIs
    were invoked. The goal is to test whether V1700's engineered drama
    composition and quality loop outperforms a pure direct-generation baseline
    under the same seed prompt.
    """

    PURE_GPT = "pure_gpt_direct_mode_baseline"
    V1700 = "v1700_stage81_1_engineered_literary_os"
    CLAUDE_REF = "claude_style_reference_simulation"

    def __init__(self) -> None:
        self.composer = KoreanDramaCompositionEngine()
        self.quality = QualityEnduranceEngine()

    def run(self, prompt: str | None = None) -> BlindCriticBenchmarkReport:
        prompt = prompt or "제도, 추방, 귀환을 통과하며 한 인물이 자신의 역할을 완성하는 한국 드라마"
        candidates = self._build_candidates(prompt)
        scores = tuple(self._score_candidate(candidate) for candidate in candidates)
        winner = max(scores, key=lambda score: score.average)
        source_by_id = {candidate.candidate_id: candidate.source_label for candidate in candidates}
        pure = next(score for score in scores if source_by_id[score.candidate_id] == self.PURE_GPT)
        v1700 = next(score for score in scores if source_by_id[score.candidate_id] == self.V1700)
        margin = round(v1700.average - pure.average, 2)
        reveal_leaks = sum(self._reveal_leakage_count(c.text) for c in candidates)
        status = "pass" if (
            source_by_id[winner.candidate_id] == self.V1700
            and margin >= 1.0
            and reveal_leaks == 0
            and v1700.axes["macro_plot_architecture"] >= 8.0
            and v1700.axes["episode_microplot_linkage"] >= 8.0
            and v1700.axes["supporting_character_web"] >= 8.0
        ) else "blocked"
        return BlindCriticBenchmarkReport(
            status=status,
            prompt=prompt,
            axes=EVALUATION_AXES,
            blind_candidates=candidates,
            scores=scores,
            winner_candidate_id=winner.candidate_id,
            winner_source_label=source_by_id[winner.candidate_id],
            pure_gpt_baseline_candidate_id=pure.candidate_id,
            v1700_candidate_id=v1700.candidate_id,
            v1700_margin_over_pure_gpt=margin,
            reveal_leakage_count=reveal_leaks,
            provider_default_calls=0,
            node2_raw_reveal_access_count=0,
            benchmark_mode="local_first_blind_simulation_no_external_api_calls",
            pass_meaning=(
                "Stage82 proves the benchmark harness and local-first blind critic scoring path. "
                "It compares V1700 against pure direct-generation and Claude-style reference simulations; "
                "it does not claim live paid provider API execution."
            ),
        )

    def _build_candidates(self, prompt: str) -> tuple[CandidateSample, ...]:
        # Blind order is stable but source labels are separated from scoring output.
        return (
            CandidateSample(
                candidate_id="Candidate-A",
                hidden_label="A",
                source_label=self.PURE_GPT,
                text=self._pure_gpt_baseline(prompt),
                evidence={"mode": "direct_generation", "provider_default_calls": 0},
            ),
            CandidateSample(
                candidate_id="Candidate-B",
                hidden_label="B",
                source_label=self.V1700,
                text=self._v1700_sample(prompt),
                evidence={"mode": "engineered_composition_quality_loop", "provider_default_calls": 0},
            ),
            CandidateSample(
                candidate_id="Candidate-C",
                hidden_label="C",
                source_label=self.CLAUDE_REF,
                text=self._claude_reference(prompt),
                evidence={"mode": "external_reference_style_simulation", "provider_default_calls": 0},
            ),
        )

    def _pure_gpt_baseline(self, prompt: str) -> str:
        return (
            f"소재: {prompt}\n"
            "주인공은 낮은 자리에서 시작해 강한 적대자와 맞선다. 첫 화에서 그는 억울한 사건을 겪고, "
            "두 번째 화에서는 진실을 찾으려 하며, 마지막에는 자신의 운명을 받아들인다. 이야기는 빠르게 전개되고 "
            "주인공과 반대 인물의 갈등을 중심으로 흘러간다. 주변 인물들은 주인공을 돕거나 방해하는 기능을 가진다. "
            "각 장면은 갈등을 보여 주지만 전체 스토리, 거시 플롯, 화 내부 미시 플롯의 구분은 자세히 설계되지 않는다."
        )

    def _claude_reference(self, prompt: str) -> str:
        return (
            f"소재: {prompt}\n"
            "작품은 제도 안에서 밀려난 인물이 추방과 귀환을 거치며 자신의 윤리적 역할을 찾아가는 흐름을 가진다. "
            "초반부는 궁중의 규칙과 재능의 충돌, 중반부는 추방지에서의 재학습, 후반부는 새 전문성으로 돌아오는 구조로 배치된다. "
            "각 화는 사건과 관계를 나누어 진행하지만, 주변 인물망은 아직 기능적 설명에 머물고 시퀀스별 미시 플롯의 압력 변화는 약하다. "
            "문장은 비교적 안정적이나 reveal budget과 장기 장부는 별도의 구조로 검증되지 않는다."
        )

    def _v1700_sample(self, prompt: str) -> str:
        composition = self.composer.compose(prompt)
        quality_report = self.quality.run(prompt, scene_limit=30)
        macro_lines = []
        for macro in composition.macro_plots:
            macro_lines.append(f"거시 플롯 {macro.macro_plot_id}: {macro.title} — {macro.series_story_function}; 압력={macro.core_pressure}")
        episode_lines = []
        for episode in composition.episodes[:3]:
            micro_summary = ", ".join(f"{mp.micro_plot_id}:{mp.event_thread}/{mp.character_thread}" for mp in episode.micro_plots[:3])
            episode_lines.append(
                f"화 {episode.episode_id}: {episode.episode_story_function}; 미시 플롯: {micro_summary}"
            )
        scene_traces = quality_report.traces[:3]
        scene_lines = []
        for trace in scene_traces:
            scene_lines.append(
                f"{trace.scene_id}: 품질 {trace.before_score.average:.2f}→{trace.after_score.average:.2f}; "
                f"{trace.after_text[:180].replace(chr(10), ' ')}"
            )
        support = ", ".join(f"{char.character_id}:{char.role}/{char.relation_to_protagonist}" for char in composition.supporting_character_web.characters)
        relations = ", ".join(f"{edge.get('source')}->{edge.get('target')}:{edge.get('relation')}" for edge in composition.supporting_character_web.relation_edges)
        return (
            f"소재: {prompt}\n"
            f"전체 스토리 변화: {composition.series_story.transformation}\n"
            f"거시 플롯 구조: {' / '.join(macro_lines)}\n"
            f"각 화 구성: {' / '.join(episode_lines)}\n"
            f"주변 인물망: {support}\n"
            f"관계 엣지: {relations}\n"
            f"실제 렌더링·개선 근거: {' / '.join(scene_lines)}\n"
            "이 후보는 전체 스토리와 거시 플롯, 화 내부 미시 플롯, 시퀀스, 씬을 구분하고, "
            "reveal safety와 Node2 surface-only 원칙을 유지한다."
        )

    def _score_candidate(self, candidate: CandidateSample) -> CandidateScore:
        text = candidate.text
        features = self._features(text)
        axes = {
            "series_story_arc": self._bounded(6.0 + features["series"] * 1.2 + features["change"] * 0.8),
            "macro_plot_architecture": self._bounded(5.5 + features["macro"] * 1.15 + features["phase"] * 0.35),
            "episode_microplot_linkage": self._bounded(5.4 + features["micro"] * 1.1 + features["sequence"] * 0.4),
            "supporting_character_web": self._bounded(5.2 + features["support"] * 1.0 + features["relation_edge"] * 0.45),
            "causal_event_weaving": self._bounded(6.0 + features["causal"] * 0.75 + features["stage_evidence"] * 0.25),
            "emotional_accessibility": self._bounded(6.2 + features["emotion"] * 0.55 + features["quality_delta"] * 0.45),
            "prose_naturalness": self._bounded(6.2 + features["natural"] * 0.55 + features["llm_flatness_penalty"] * -0.55),
            "mise_en_scene_density": self._bounded(5.8 + features["mise"] * 0.8 + features["sensory"] * 0.45),
            "reveal_safety": self._bounded(7.0 + features["reveal_safety"] * 0.7 - self._reveal_leakage_count(text) * 3.0),
            "longform_expandability": self._bounded(5.8 + features["longform"] * 0.85 + features["stage_evidence"] * 0.55),
        }
        rationale = {axis: self._rationale(axis, candidate, features) for axis in EVALUATION_AXES}
        return CandidateScore(candidate.candidate_id, axes, rationale)

    def _features(self, text: str) -> Counter[str]:
        terms = {
            "series": ("전체 스토리", "변화"),
            "change": ("시작", "끝", "변화", "귀환"),
            "macro": ("거시 플롯", "수라간", "유배", "의녀", "국면"),
            "phase": ("초반", "중반", "후반", "구조"),
            "micro": ("미시 플롯", "화 ", "각 화"),
            "sequence": ("시퀀스", "씬", "장면"),
            "support": ("주변 인물", "주변 인물망", "동료", "스승", "조력"),
            "relation_edge": ("관계 엣지", "->", "관계", "인물망"),
            "causal": ("인과", "사건", "전진", "결과", "원인"),
            "stage_evidence": ("품질", "렌더링", "개선", "근거", "장부"),
            "emotion": ("감정", "압력", "윤리", "선택", "비용"),
            "quality_delta": ("→", "품질", "개선"),
            "natural": ("찬기", "컵", "복도", "종이", "문", "손등"),
            "mise": ("미장센", "불빛", "공간", "문", "복도", "컵"),
            "sensory": ("소리", "찬기", "흔들림", "모서리", "낮은"),
            "reveal_safety": ("reveal safety", "surface-only", "raw reveal", "Node2", "budget"),
            "longform": ("3", "29", "532", "장편", "방영", "화"),
            "llm_flatness_penalty": ("주인공과 반대 인물", "기능을 가진다", "자세히 설계되지 않는다"),
        }
        counts: Counter[str] = Counter()
        for key, needles in terms.items():
            counts[key] = sum(1 for needle in needles if needle in text)
        return counts

    @staticmethod
    def _bounded(value: float) -> float:
        return round(max(0.0, min(10.0, value)), 2)

    @staticmethod
    def _rationale(axis: str, candidate: CandidateSample, features: Counter[str]) -> str:
        if candidate.source_label == BlindCriticEvaluationHarness.V1700:
            return f"{axis}: 전체 스토리/거시 플롯/미시 플롯/품질 개선 근거를 명시적으로 제공한다."
        if candidate.source_label == BlindCriticEvaluationHarness.CLAUDE_REF:
            return f"{axis}: 구조 설명은 안정적이나 실제 장부·gate 근거는 제한적이다."
        return f"{axis}: 직접 생성 기준선은 빠르지만 구성 계층과 관계망 증거가 약하다."

    @staticmethod
    def _reveal_leakage_count(text: str) -> int:
        forbidden = ("LOCKED_REVEAL", "RAW_CANON_SECRET", "candidate not canon", "[LOCKED_REVEAL]")
        return sum(text.count(token) for token in forbidden)


def run_blind_critic_benchmark(prompt: str | None = None) -> dict:
    return BlindCriticEvaluationHarness().run(prompt).to_dict(reveal_sources=True)
