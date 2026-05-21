from __future__ import annotations

import json
from pathlib import Path

from v1700.ir.scene_intent import EmotionalDelta, SceneIntentIR
from v1700.ir.style_profile import StyleProfileIR

from .contracts import E2ESampleBundle


def load_sample_bundle(root: Path) -> E2ESampleBundle:
    sample = root / "samples" / "korean_drama_family_secret"
    benchmark = root / "benchmarks" / "longform_output"
    return E2ESampleBundle(
        project=_read_json(sample / "project.json"),
        characters=_read_json(sample / "characters.json"),
        world=_read_json(sample / "world.json"),
        plot_outline=_read_text(sample / "plot_outline.md"),
        scene_request=_read_json(sample / "scene_requests" / "scene_001.json"),
        benchmark_expectations=_read_json(benchmark / "expected_metrics.json"),
    )


def build_scene_intent(bundle: E2ESampleBundle) -> SceneIntentIR:
    scene_id = str(bundle.scene_request.get("scene_id", "stage141_scene_001"))
    objective = str(bundle.scene_request.get("objective", "상속 편지의 존재를 확인한다"))
    setting = str(bundle.world.get("setting", "서울의 오래된 가족 저택 응접실"))
    return SceneIntentIR(
        scene_id=scene_id,
        scene_goal=objective,
        conflict="변호사는 절차를 이유로 답을 미루고 고모는 침묵으로 압박한다",
        emotional_delta=EmotionalDelta("불안", "의심"),
        must_keep_facts=(
            "봉인된 상속 편지가 있다.",
            "가족 저택의 소유권이 흔들릴 수 있다.",
            "최종 비밀은 아직 공개되지 않는다.",
        ),
        forbidden_reveals=(
            "FINAL_SECRET_CONTENTS",
            "REAL_HEIR_IDENTITY",
        ),
        timeline_position="EP1_SCENE1",
        character_state_refs=tuple(bundle.scene_request.get("characters", [])),
        dialogue_seed="지금은 봉인을 풀 수 없어요. 하지만 아무 일도 아니라는 뜻은 아닙니다.",
        setting_seed=f"늦은 오후, {setting}. 비가 그친 뒤 젖은 정원이 창밖에 남아 있다.",
    )


def build_style_profile() -> StyleProfileIR:
    return StyleProfileIR(profile_id="stage141_prose_generation_e2e_profile")


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""
