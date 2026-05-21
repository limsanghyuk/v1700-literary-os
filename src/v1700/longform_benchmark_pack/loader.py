from __future__ import annotations

import json
from pathlib import Path

from v1700.ir.scene_intent import EmotionalDelta, SceneIntentIR
from v1700.ir.style_profile import StyleProfileIR

from .contracts import BenchmarkCase


def load_stage141_inputs(root: Path) -> tuple[dict, dict]:
    report_path = root / "release" / "current" / "stage141_prose_generation_e2e_report.json"
    expected_path = root / "benchmarks" / "longform_output" / "expected_metrics.json"
    report = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else {}
    expected = json.loads(expected_path.read_text(encoding="utf-8")) if expected_path.exists() else {}
    return report, expected


def build_benchmark_cases() -> tuple[BenchmarkCase, ...]:
    return (
        BenchmarkCase(
            benchmark_case_id="stage142_case_001",
            scene_id="scene_001",
            title="Inheritance Letter Reveal Pressure",
            objective="Establish the family inheritance question without revealing the final secret.",
            must_keep_facts=(
                "봉인된 상속 편지가 있다.",
                "가족 저택의 소유권이 흔들릴 수 있다.",
                "최종 비밀은 아직 공개되지 않는다.",
            ),
            forbidden_reveals=("FINAL_SECRET_CONTENTS", "REAL_HEIR_IDENTITY"),
        ),
        BenchmarkCase(
            benchmark_case_id="stage142_case_002",
            scene_id="scene_002",
            title="Legal Delay and Silent Witness",
            objective="Delay the legal answer while escalating suspicion around the sealed document.",
            must_keep_facts=(
                "변호사는 절차를 이유로 답을 미룬다.",
                "윤미라는 직접 설명하지 않고 침묵으로 압박한다.",
                "문서의 최종 내용은 아직 공개되지 않는다.",
            ),
            forbidden_reveals=("FINAL_SECRET_CONTENTS", "TRUE_DOCUMENT_OWNER"),
        ),
        BenchmarkCase(
            benchmark_case_id="stage142_case_003",
            scene_id="scene_003",
            title="House Ownership Doubt",
            objective="Make the house ownership risk feel immediate without exposing the hidden heir.",
            must_keep_facts=(
                "가족 저택의 소유권이 흔들릴 수 있다.",
                "한세라는 불안을 숨기지 못한다.",
                "진짜 상속인의 정체는 아직 밝혀지지 않는다.",
            ),
            forbidden_reveals=("REAL_HEIR_IDENTITY", "SEALED_LETTER_EXACT_TEXT"),
        ),
    )


def build_scene_intent(case: BenchmarkCase) -> SceneIntentIR:
    conflict_map = {
        "scene_001": "변호사는 절차를 이유로 답을 미루고 고모는 침묵으로 압박한다",
        "scene_002": "법적 해석은 늦어지고 가족의 눈빛은 점점 더 날카로워진다",
        "scene_003": "집의 주인이 바뀔 수 있다는 불안이 인물들의 대화를 흔든다",
    }
    setting_map = {
        "scene_001": "늦은 오후, 서울의 오래된 가족 저택 응접실",
        "scene_002": "비가 멎은 저녁, 작은 법률 사무실의 복도 앞 대기실",
        "scene_003": "밤이 깊어가는 저택 식당, 닫힌 창문에 정원 불빛이 비친다",
    }
    return SceneIntentIR(
        scene_id=case.scene_id,
        scene_goal=case.objective,
        conflict=conflict_map.get(case.scene_id, "침묵과 의심이 장면을 압박한다"),
        emotional_delta=EmotionalDelta("불안", "의심"),
        must_keep_facts=case.must_keep_facts,
        forbidden_reveals=case.forbidden_reveals,
        timeline_position=case.benchmark_case_id.upper(),
        character_state_refs=("han_sera", "kim_doyun", "yoon_mira"),
        dialogue_seed="지금 말할 수 없는 사실이 있다는 것만으로도 충분히 위험해요.",
        setting_seed=setting_map.get(case.scene_id, "서울의 오래된 실내 공간"),
    )


def build_style_profile() -> StyleProfileIR:
    return StyleProfileIR(profile_id="stage142_longform_benchmark_pack_profile")
