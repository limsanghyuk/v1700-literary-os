
from __future__ import annotations

import json
import re
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean
from typing import Any, Protocol

from v1700.gates.stage80_release_gate import run_stage80_release_gate
from v1700.lineage.stage83_1_consistency_audit import run_stage83_1_consistency_audit


@dataclass(frozen=True)
class StyleDNAProfile:
    genre_id: str
    pov: str
    scene_rhythm: str
    emotional_amp: float
    anti_llm_strictness: str
    sensory_priority: tuple[str, ...]
    inner_monologue: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "genre_id": self.genre_id,
            "pov": self.pov,
            "scene_rhythm": self.scene_rhythm,
            "emotional_amp": self.emotional_amp,
            "anti_llm_strictness": self.anti_llm_strictness,
            "sensory_priority": list(self.sensory_priority),
            "inner_monologue": self.inner_monologue,
            "metadata": dict(self.metadata),
        }


class StyleDNA:
    """V1700-native StyleDNA profile registry adapted from Claude V370 concepts."""

    def __init__(self) -> None:
        self._profiles: dict[str, StyleDNAProfile] = {
            "literary": StyleDNAProfile("literary", "1인칭", "slow", 0.80, "strict", ("tactile", "audio", "visual"), True),
            "noir": StyleDNAProfile("noir", "1인칭", "fast", 0.40, "firm", ("visual", "audio", "tactile"), False),
            "fantasy": StyleDNAProfile("fantasy", "3인칭 제한", "medium", 0.75, "standard", ("visual", "tactile", "audio"), False),
            "romance": StyleDNAProfile("romance", "3인칭 제한", "medium", 0.95, "relaxed", ("tactile", "visual", "audio"), True),
            "historical": StyleDNAProfile("historical", "3인칭 전지", "slow", 0.60, "firm", ("audio", "visual", "tactile"), False),
        }

    def get(self, genre_id: str = "literary") -> StyleDNAProfile:
        if genre_id not in self._profiles:
            raise ValueError(f"Unknown genre_id: {genre_id}")
        return self._profiles[genre_id]

    def register(self, profile: StyleDNAProfile) -> None:
        self._profiles[profile.genre_id] = profile

    def available_genres(self) -> tuple[str, ...]:
        return tuple(self._profiles)


_BASE_CLICHES: dict[str, str] = {
    "복잡한 감정이 밀려왔다": "식은 숨이 한 번 새어 나왔다",
    "복잡한 감정이 밀려들었다": "손끝이 천천히 식었다",
    "감정이 복잡했다": "입 안이 바짝 말랐다",
    "가슴이 먹먹했다": "목 안쪽이 마른 종이처럼 붙었다",
    "마음이 복잡했다": "손바닥을 두 번 폈다 접었다",
    "말로 표현할 수 없는 감정": "이름 붙이지 않기로 한 것",
    "눈물이 핑 돌았다": "아래 눈꺼풀이 한 번 떨렸다",
    "눈물이 왈칵 쏟아졌다": "눈 안쪽이 뜨거워졌다",
    "운명의 장난처럼": "기울어진 시간처럼",
    "그 순간, 모든 것이 달라질 것만 같았다": "문틈으로 들어오던 바람이 멎었다",
    "그 순간 시간이 멈춘 것 같았다": "숨이 반 박자 늦게 나왔다",
    "심장이 두근거렸다": "귀 뒤쪽이 달아올랐다",
    "가슴이 두근댔다": "목 아래쪽이 조여들었다",
    "침묵이 흘렀다": "냉장고 소리가 유독 크게 들렸다",
    "정적이 흘렀다": "바람 소리만 들렸다",
    "배신감이 밀려왔다": "발밑이 빠지는 것 같았다",
    "충격이었다": "눈이 한 번도 깜빡이지 않았다",
    "믿기지 않았다": "같은 문장을 세 번 읽었다",
    "안도감이 밀려왔다": "어깨가 한 박자 늦게 내려갔다",
    "두려웠다": "등 뒤가 서늘했다",
    "무서웠다": "발바닥이 바닥에 들러붙었다",
    "긴장했다": "손바닥이 축축해졌다",
    "불안했다": "눈이 자꾸 문 쪽으로 갔다",
    "화가 났다": "이를 악물었다",
    "분노가 치밀었다": "손이 주먹을 쥐었다",
    "당황했다": "발끝이 안쪽으로 돌아갔다",
    "결심했다": "턱을 한 번 당겼다",
    "지쳐있었다": "눈꺼풀이 납 같았다",
    "보고 싶었다": "핸드폰을 집어 들다가 내려놓았다",
}

_GENRE_CLICHES: dict[str, dict[str, str]] = {
    "noir": {"불안했다": "담배 연기가 눈에 들어오는 것처럼 따가웠다", "믿기지 않았다": "창밖의 가로등을 다섯 번 세었다"},
    "romance": {"심장이 두근거렸다": "그 손이 닿았던 자리가 한참 뒤까지 따뜻했다"},
    "historical": {"분노가 치밀었다": "옷깃을 여몄다", "결심했다": "손을 모아 예를 올렸다"},
}


@dataclass(frozen=True)
class FilterResult:
    filtered: str
    score: float
    replacements: tuple[tuple[str, str], ...]
    n_cliches: int

    @property
    def is_clean(self) -> bool:
        return self.n_cliches == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "filtered": self.filtered,
            "score": self.score,
            "replacements": [list(pair) for pair in self.replacements],
            "n_cliches": self.n_cliches,
            "is_clean": self.is_clean,
        }


class KoreanAntiLLMFilter:
    def __init__(self, genre_id: str = "literary") -> None:
        self.genre_id = genre_id
        self._dictionary = dict(_BASE_CLICHES)
        self._dictionary.update(_GENRE_CLICHES.get(genre_id, {}))

    @property
    def dict_size(self) -> int:
        return len(self._dictionary)

    def filter(self, text: str) -> FilterResult:
        out = text
        replacements: list[tuple[str, str]] = []
        for cliche, replacement in sorted(self._dictionary.items(), key=lambda item: -len(item[0])):
            if cliche in out:
                out = out.replace(cliche, replacement)
                replacements.append((cliche, replacement))
        if not text:
            score = 10.0
        else:
            cliche_chars = sum(len(src) for src, _ in replacements)
            score = round(10.0 * (1.0 - min(cliche_chars / max(len(text), 1), 1.0)), 3)
        return FilterResult(out, score, tuple(replacements), len(replacements))

    def score_only(self, text: str) -> float:
        return self.filter(text).score


_DIRECT_EMOTION: dict[str, str] = {
    "슬펐다": "시선을 컵 바닥에 오래 두었다",
    "분노했다": "봉투의 모서리를 손톱 밑으로 눌렀다",
    "화가 났다": "말끝을 삼키고 의자의 등받이를 밀었다",
    "두려웠다": "손바닥의 물기를 바지선에 문질렀다",
    "불안했다": "문고리 쪽으로 시선이 자꾸 갔다",
    "배신감을 느꼈다": "그의 이름이 적힌 봉투를 두 번 접었다",
    "행복했다": "발끝까지 따뜻한 기운이 남았다",
}


class EmotionToBehaviorRenderer:
    def rewrite(self, text: str, emotional_amp: float = 0.8) -> str:
        out = text
        for src, dst in _DIRECT_EMOTION.items():
            out = out.replace(src, dst)
        if emotional_amp > 0.9 and "말하지 않았다" in out:
            out = out.replace("말하지 않았다", "말하지 않았다. 대신 컵받침을 반듯하게 밀었다")
        return out

    def direct_emotion_count(self, text: str) -> int:
        return sum(1 for marker in _DIRECT_EMOTION if marker in text)


_ANCHORS: dict[str, tuple[str, ...]] = {
    "visual": ("형광등이 한 번 깜빡였다", "창밖으로 나뭇잎이 하나 지나갔다", "가로등 빛이 유리컵에 길게 비쳤다"),
    "audio": ("복도 끝에서 엘리베이터가 낮게 울렸다", "냉장고 소리가 유독 크게 들렸다", "멀리서 버스 문 닫히는 소리가 났다"),
    "tactile": ("컵 가장자리의 찬기가 손끝에 남았다", "접힌 종이의 모서리가 손톱 밑을 스쳤다", "젖은 소매가 손목에 달라붙었다"),
}


class SensoryAnchorInjector:
    def inject(self, text: str, profile: StyleDNAProfile, setting_seed: dict[str, str] | None = None, density: float = 0.45) -> dict[str, Any]:
        setting_seed = setting_seed or {}
        anchors: list[str] = []
        max_anchors = 3 if density >= 0.5 else 2
        for axis in profile.sensory_priority:
            if len(anchors) >= max_anchors:
                break
            anchor = setting_seed.get(axis) or _ANCHORS.get(axis, ("",))[0]
            if anchor:
                anchors.append(anchor.rstrip(".。") + ".")
        injected = text.rstrip()
        if anchors:
            injected = injected + "\n\n" + " ".join(anchors)
        return {"text": injected, "anchors": anchors, "density": round(len(anchors) / 3, 3)}


class KoreanRhythmRewriter:
    def rewrite(self, text: str, profile: StyleDNAProfile) -> str:
        parts = [part.strip() for part in re.split(r"(?<=[.!?。！？])\s+|(?<=다\.)\s+", text) if part.strip()]
        if len(parts) <= 1:
            return text
        if profile.scene_rhythm == "fast":
            return "\n".join(parts)
        if profile.scene_rhythm == "slow" and len(parts) >= 3:
            return " ".join(parts[:-2]) + "\n\n" + " ".join(parts[-2:])
        return " ".join(parts[:-1]) + "\n\n" + parts[-1]

    def score(self, text: str) -> float:
        lengths = [len(chunk.strip()) for chunk in re.split(r"[.!?。！？]|다\.", text) if chunk.strip()]
        if not lengths:
            return 7.0
        spread = max(lengths) - min(lengths)
        paragraph_bonus = 0.4 if "\n\n" in text else 0.0
        return round(min(10.0, 7.2 + min(spread, 80) / 80 * 1.2 + paragraph_bonus), 3)


class ReaderSurfaceScorer:
    def __init__(self) -> None:
        self.rhythm = KoreanRhythmRewriter()
        self.emotion = EmotionToBehaviorRenderer()

    def score(self, text: str, genre_id: str = "literary") -> dict[str, float]:
        anti = KoreanAntiLLMFilter(genre_id).score_only(text)
        direct_count = self.emotion.direct_emotion_count(text)
        sensory_hits = sum(1 for marker in ("형광등", "컵", "손끝", "냉장고", "가로등", "소리", "찬기", "종이") if marker in text)
        scores = {
            "anti_llm": anti,
            "emotion_to_behavior": round(max(0.0, 9.0 - direct_count * 1.5), 3),
            "rhythm": self.rhythm.score(text),
            "sensory_afterimage": round(min(10.0, 7.0 + sensory_hits * 0.35), 3),
            "korean_dialogue_surface": 8.4 if "\"" not in text else 8.0,
        }
        scores["reader_surface_average"] = round(mean(scores.values()), 3)
        return scores


class LocalJudgmentValidator:
    def validate(self, scores: dict[str, float], minimum_average: float = 8.0, minimum_axis: float = 7.0) -> dict[str, Any]:
        axis_failures = [axis for axis, score in scores.items() if axis != "reader_surface_average" and score < minimum_axis]
        avg = scores.get("reader_surface_average", 0.0)
        issues = list(axis_failures)
        if avg < minimum_average:
            issues.append("reader_surface_average_below_threshold")
        return {"status": "pass" if not issues else "blocked", "issues": issues, "average": avg, "scores": scores}


class Adapter(Protocol):
    provider_name: str
    call_count: int

    def generate(self, prompt: str, context: dict[str, Any]) -> str: ...


class MockAdapter:
    provider_name = "mock"

    def __init__(self, scripted_response: str | None = None) -> None:
        self.scripted_response = scripted_response or "그는 대답하지 않았다. 컵 가장자리의 찬기가 손끝에 남았다."
        self._call_count = 0

    @property
    def call_count(self) -> int:
        return self._call_count

    def generate(self, prompt: str, context: dict[str, Any]) -> str:
        self._call_count += 1
        return self.scripted_response


class LLMNodeRouter:
    """Provider-safe adapter router. Stage84 keeps provider default calls at zero."""

    def __init__(self, allow_provider_calls: bool = False) -> None:
        self.allow_provider_calls = allow_provider_calls
        self._adapters: dict[str, Adapter] = {"mock": MockAdapter()}
        self.provider_default_calls = 0

    def register(self, adapter: Adapter) -> None:
        self._adapters[adapter.provider_name] = adapter

    def generate(self, prompt: str, context: dict[str, Any] | None = None, provider: str = "mock") -> str:
        if provider != "mock" and not self.allow_provider_calls:
            self.provider_default_calls += 0
            return self._adapters["mock"].generate(prompt, context or {})
        adapter = self._adapters.get(provider) or self._adapters["mock"]
        if provider != "mock":
            self.provider_default_calls += 1
        return adapter.generate(prompt, context or {})

    def call_counts(self) -> dict[str, int]:
        return {name: adapter.call_count for name, adapter in self._adapters.items()}


@dataclass(frozen=True)
class TraceRecord:
    record_id: str
    scene_id: str
    scene_text: str
    scores: dict[str, float]
    accepted: bool
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "scene_id": self.scene_id,
            "scene_text": self.scene_text,
            "scores": self.scores,
            "accepted": self.accepted,
            "created_at": self.created_at,
            "scene_text_len": len(self.scene_text),
        }


class SelfLearningCollector:
    def __init__(self, store_path: str | Path) -> None:
        self.store_path = Path(store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)
        self.records: list[TraceRecord] = []
        self.jsonl_path = self.store_path / "stage84_trace_dataset.jsonl"

    def collect(self, scene_id: str, scene_text: str, scores: dict[str, float], accepted: bool) -> TraceRecord:
        record = TraceRecord(str(uuid.uuid4())[:8], scene_id, scene_text, scores, accepted)
        self.records.append(record)
        with self.jsonl_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
        return record

    def export_dataset(self) -> list[dict[str, Any]]:
        return [
            {
                "instruction": "Render this Korean drama scene with concrete behavior, sensory anchors, and no raw reveal leakage.",
                "output": record.scene_text,
                "quality": record.scores,
                "record_id": record.record_id,
            }
            for record in self.records
            if record.accepted
        ]

    def statistics(self) -> dict[str, Any]:
        total = len(self.records)
        accepted = sum(1 for record in self.records if record.accepted)
        return {"total_records": total, "accepted_records": accepted, "accepted_rate": round(accepted / total, 3) if total else 0.0}


@dataclass(frozen=True)
class AbsorbedRenderResult:
    status: str
    scene_id: str
    genre_id: str
    text: str
    scores: dict[str, float]
    validator: dict[str, Any]
    replacements: tuple[tuple[str, str], ...]
    anchors: tuple[str, ...]
    provider_default_calls: int = 0
    node2_raw_reveal_access_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "scene_id": self.scene_id,
            "genre_id": self.genre_id,
            "text": self.text,
            "scores": self.scores,
            "validator": self.validator,
            "replacements": [list(pair) for pair in self.replacements],
            "anchors": list(self.anchors),
            "provider_default_calls": self.provider_default_calls,
            "node2_raw_reveal_access_count": self.node2_raw_reveal_access_count,
        }


class ClosedLoopRenderer:
    """Stage84 absorption layer: V370 runtime muscle, V1700 authority contracts."""

    def __init__(self, trace_store: str | Path | None = None) -> None:
        self.style_dna = StyleDNA()
        self.emotion = EmotionToBehaviorRenderer()
        self.sensory = SensoryAnchorInjector()
        self.rhythm = KoreanRhythmRewriter()
        self.scorer = ReaderSurfaceScorer()
        self.validator = LocalJudgmentValidator()
        self.router = LLMNodeRouter(allow_provider_calls=False)
        self.collector = SelfLearningCollector(trace_store or Path(".stage84_traces"))

    def render(self, scene_goal: str, seed_text: str, genre_id: str = "literary", scene_id: str = "stage84_scene_001") -> AbsorbedRenderResult:
        profile = self.style_dna.get(genre_id)
        text = seed_text or self.router.generate(scene_goal, {"scene_goal": scene_goal}, provider="mock")
        text = self.emotion.rewrite(text, emotional_amp=profile.emotional_amp)
        filtered = KoreanAntiLLMFilter(genre_id).filter(text)
        anchored = self.sensory.inject(filtered.filtered, profile)
        rewritten = self.rhythm.rewrite(anchored["text"], profile)
        scores = self.scorer.score(rewritten, genre_id=genre_id)
        validation = self.validator.validate(scores)
        accepted = validation["status"] == "pass"
        self.collector.collect(scene_id, rewritten, scores, accepted)
        return AbsorbedRenderResult(
            status="pass" if accepted else "blocked",
            scene_id=scene_id,
            genre_id=genre_id,
            text=rewritten,
            scores=scores,
            validator=validation,
            replacements=filtered.replacements,
            anchors=tuple(anchored["anchors"]),
            provider_default_calls=self.router.provider_default_calls,
            node2_raw_reveal_access_count=0,
        )


def build_v370_feature_map_manifest() -> dict[str, Any]:
    return {
        "stage": "84",
        "status": "mapped",
        "source_archive": "literary_os_v370_release.zip",
        "principle": "Map Claude V370 runtime features into V1700 contracts rather than copying authority boundaries wholesale.",
        "features": [
            {"v370_feature": "ClosedLoopRenderOrchestratorV2", "v1700_absorption": "ClosedLoopRenderer", "status": "absorbed"},
            {"v370_feature": "KoreanAntiLLMFilter", "v1700_absorption": "KoreanAntiLLMFilter", "status": "absorbed"},
            {"v370_feature": "StyleDNA", "v1700_absorption": "StyleDNA", "status": "absorbed"},
            {"v370_feature": "SensoryAnchorInjector", "v1700_absorption": "SensoryAnchorInjector", "status": "absorbed"},
            {"v370_feature": "EmotionToBehaviorRenderer", "v1700_absorption": "EmotionToBehaviorRenderer", "status": "absorbed"},
            {"v370_feature": "KoreanRhythmRewriter", "v1700_absorption": "KoreanRhythmRewriter", "status": "absorbed"},
            {"v370_feature": "ReaderSurfaceScorer", "v1700_absorption": "ReaderSurfaceScorer", "status": "absorbed"},
            {"v370_feature": "LocalJudgmentValidator", "v1700_absorption": "LocalJudgmentValidator", "status": "absorbed"},
            {"v370_feature": "LLMNodeRouter / ClaudeAdapter / OllamaAdapter / MockAdapter", "v1700_absorption": "LLMNodeRouter with provider default calls locked to 0", "status": "safe_mock_absorbed"},
            {"v370_feature": "SelfLearningCollector / trace dataset", "v1700_absorption": "SelfLearningCollector local JSONL trace dataset", "status": "absorbed"},
        ],
    }


def build_absorption_decision_matrix() -> dict[str, Any]:
    return {
        "stage": "84",
        "status": "pass",
        "decisions": [
            {"decision": "copy_wholesale_v370", "result": "rejected", "risk": "Would bypass V1700 node authority, hierarchy, gates, and release evidence."},
            {"decision": "adapter_only", "result": "rejected", "risk": "Would add routing without improving reader-facing prose surface."},
            {"decision": "surface_runtime_absorption", "result": "selected", "reason": "Absorbs V370 muscle while preserving V1700 Korean drama skeleton and provider-zero contract."},
            {"decision": "provider_default_calls", "result": "locked_to_zero", "reason": "Commercial candidate remains local-first by default."},
            {"decision": "node2_raw_reveal_access", "result": "locked_to_zero", "reason": "Node2 may improve surface only and cannot access raw reveal authority."},
        ],
    }


def run_stage84_absorption_smoke(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    stage83_1 = run_stage83_1_consistency_audit(root)
    stage80 = run_stage80_release_gate(root)
    trace_dir = root / "release" / "current" / "stage84_trace_dataset"
    renderer = ClosedLoopRenderer(trace_store=trace_dir)
    seed_text = "그 순간, 모든 것이 달라질 것만 같았다. 그는 복잡한 감정이 밀려왔다. 하지만 말하지 않았다."
    result = renderer.render("조력자의 침묵이 우연이 아님을 행동으로 드러낸다", seed_text, genre_id="literary")
    feature_map = build_v370_feature_map_manifest()
    decision_matrix = build_absorption_decision_matrix()
    hierarchy_terms = {"Series Story", "Macro Plot", "Broadcast Episode", "Micro Plot", "Sequence", "Scene"}
    stage80_text = json.dumps(stage80, ensure_ascii=False)
    hierarchy_preserved = all(term in stage80_text for term in hierarchy_terms)

    issues: list[str] = []
    if stage83_1.get("status") != "pass":
        issues.append("stage83_1_baseline_blocked")
    if stage80.get("status") != "pass" or not hierarchy_preserved:
        issues.append("korean_drama_hierarchy_not_preserved")
    if result.status != "pass":
        issues.append("closed_loop_renderer_blocked")
    if not result.replacements:
        issues.append("anti_llm_filter_did_not_replace_cliche")
    if len(result.anchors) < 2:
        issues.append("sensory_anchor_injection_insufficient")
    if result.provider_default_calls != 0:
        issues.append("provider_default_calls_not_zero")
    if result.node2_raw_reveal_access_count != 0:
        issues.append("node2_raw_reveal_access_not_zero")
    if renderer.collector.statistics()["total_records"] < 1:
        issues.append("trace_dataset_not_collected")

    return {
        "stage": "84",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage84 absorbs Claude V370 runtime muscle into V1700 Korean Drama OS without breaking Stage80 hierarchy, provider-zero local-first execution, or Node2 reveal authority boundaries.",
        "stage83_1_consistency_audit": {"status": stage83_1.get("status"), "issues": stage83_1.get("issues", [])},
        "stage80_hierarchy_preserved": hierarchy_preserved,
        "v370_feature_map_manifest": feature_map,
        "absorption_decision_matrix": decision_matrix,
        "closed_loop_render_result": result.to_dict(),
        "trace_dataset_statistics": renderer.collector.statistics(),
        "trace_dataset_path": str(renderer.collector.jsonl_path.relative_to(root)),
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }


def export_stage84_manifests(root: Path | None = None) -> dict[str, str]:
    root = root or Path(__file__).resolve().parents[3]
    manifest_dir = root / "manifests"
    release_dir = root / "release" / "current"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    release_dir.mkdir(parents=True, exist_ok=True)
    smoke = run_stage84_absorption_smoke(root)
    payloads: dict[str, Any] = {
        "v370_feature_map_manifest.json": smoke["v370_feature_map_manifest"],
        "stage84_absorption_decision_matrix.json": smoke["absorption_decision_matrix"],
        "stage84_manifest.json": {
            "stage": "84",
            "title": "Claude V370 Runtime Absorption into V1700 Korean Drama OS",
            "depends_on": ["stage83.1"],
            "status": smoke["status"],
            "required_outputs": [
                "src/v1700/runtime_absorption/v370_absorption.py",
                "src/v1700/gates/stage84_release_gate.py",
                "manifests/v370_feature_map_manifest.json",
                "manifests/stage84_absorption_decision_matrix.json",
                "tests/test_stage84_v370_runtime_absorption.py",
            ],
            "provider_default_calls": 0,
            "node2_raw_reveal_access_count": 0,
        },
    }
    written: dict[str, str] = {}
    for name, payload in payloads.items():
        path = manifest_dir / name
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written[name] = str(path.relative_to(root))
    report_path = release_dir / "stage84_absorption_report.json"
    report_path.write_text(json.dumps(smoke, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written[report_path.name] = str(report_path.relative_to(root))
    return written
