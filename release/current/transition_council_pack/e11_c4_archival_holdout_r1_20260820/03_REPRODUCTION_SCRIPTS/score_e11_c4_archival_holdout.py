#!/usr/bin/env python3
"""Unblind and score the frozen E11-C4 archival holdout predictions."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


LEVELS = ["L0", "L1", "L2", "L3", "L4"]


GOLD_OVERRIDES = {
    ("개인의취향", 1): (
        "L2",
        "모성 기억과 묘지 고백이 초기 비밀 처리 국면을 결산하고 설계도·관계 책임 국면으로 넘긴다.",
    ),
    ("개인의취향", 4): (
        "L2",
        "숨은 접근 목적의 자백·폭로로 목표가 부모 반대 대응에서 배신과 설계 진실 결산으로 바뀐다.",
    ),
    ("난폭한로맨스", 4): (
        "L2",
        "동수 프레임의 기능이 끝나고 실제 스토커의 범죄·직접 위협 국면으로 전환된다.",
    ),
    ("난폭한로맨스", 7): (
        "L2",
        "정체 추적 국면에서 종희 실종과 수영장 시간 제한의 즉각 구조 국면으로 이동한다.",
    ),
    ("난폭한로맨스", 9): (
        "L2",
        "수색이 실패하고 은재까지 납치되면서 단일 피해자 추적이 이중 인질 위기로 바뀐다.",
    ),
    ("난폭한로맨스", 10): (
        "L2",
        "범인과 위치 규명 단계가 끝나고 수영장 구조 작전이라는 새 목적 단계로 이동한다.",
    ),
    ("도깨비", 4): (
        "L3",
        "은탁의 기억 회복과 도깨비와의 재결합으로 회차 주 carrier 질문이 답해지고 남은 결산 carrier가 필요하다.",
    ),
    ("도깨비", 5): (
        "L3",
        "청혼·기억·첫사랑 고백으로 EP15의 남은 사랑 축 전체가 종단 결산된다.",
    ),
    ("라이벌", 2): (
        "L2",
        "골프·생계 재출발 중심에서 실제 희생·사랑과 가짜 약혼 책임 국면으로 회차 목적이 바뀐다.",
    ),
    ("라이벌", 5): (
        "L2",
        "우혁 생환과 다인 재연결이 희생·사랑 확인 단계를 결산하고 출생·책임 확인 단계로 넘긴다.",
    ),
    ("로망스", 2): (
        "L2",
        "공식 관계 준비에서 저작권 함정과 회사 전쟁이 작동하는 새 병렬 국면이 열린다.",
    ),
    ("로망스", 3): (
        "L2",
        "유서 공개와 권력 균열이 회사 범죄를 가족 승인과 동등한 episode phase로 승격한다.",
    ),
    ("로망스", 6): (
        "L2",
        "부모 신뢰 확보 시도가 경찰 소환과 사업 방어 국면으로 바뀐다.",
    ),
    ("미안하다사랑한다", 3): (
        "L2",
        "은채가 무혁을 찾으면서 접근 여부 질문이 끝나고 함께 보내는 마지막 시간 실행으로 이동한다.",
    ),
    ("미안하다사랑한다", 6): (
        "L2",
        "윤이 치료를 받아들여 충격·거부 국면을 생존 선택과 진실 전달 국면으로 넘긴다.",
    ),
    ("미안하다사랑한다", 9): (
        "L2",
        "윤의 생존 선택과 무혁 메시지가 형제 진실을 수용·전달하는 다음 단계의 조건을 확정한다.",
    ),
    ("미안하다사랑한다", 11): (
        "L2",
        "은채가 복수·혈연·희생 진실을 알게 되어 사랑의 과거를 재해석하는 국면으로 이동한다.",
    ),
    ("미안하다사랑한다", 12): (
        "L3",
        "함께할지와 함께 보내는 시간이라는 주 carrier가 작별로 끝나고 사후·가족 결산 carrier만 남는다.",
    ),
}


FINAL_HOOK_NOTES = {
    ("개인의취향", 12): "박교수에게 맞서는 선택은 다음 회차 비용을 남기는 종단 거래이며 새 현 회차 carrier는 없다.",
    ("난폭한로맨스", 11): "강제 구조 선택을 여는 hook으로 현재 Sequence 거래만 끝나며 해결은 다음 회차로 이월된다.",
    ("라이벌", 7): "DNA 재검사 제안은 다음 회차 입력 hook이며 현재 회차 axis completion으로 보지 않는다.",
    ("로망스", 7): "유서를 읽은 관우의 정지는 다음 회차 선택을 여는 hook이다.",
    ("미안하다사랑한다", 14): "지영 귀환은 마지막 Sequence novelty hook이며 downstream 현 회차 계획은 없다.",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify_freeze(pre_dir: Path) -> dict:
    failures = []
    checked = []
    for line in (pre_dir / "PREUNBLIND_FREEZE_SHA256.txt").read_text(encoding="ascii").splitlines():
        if not line.strip():
            continue
        expected, name = line.split(maxsplit=1)
        actual = sha256(pre_dir / name.strip())
        checked.append(name.strip())
        if expected != actual:
            failures.append({"file": name.strip(), "expected": expected, "actual": actual})
    return {"status": "pass" if not failures else "fail", "checked": checked, "failures": failures}


def classification(rows: list[dict], field: str) -> dict:
    total = len(rows)
    correct = sum(row[field] == row["gold_scope"] for row in rows)
    ordinal = sum(abs(LEVELS.index(row[field]) - LEVELS.index(row["gold_scope"])) for row in rows)
    by_level = {}
    for level in LEVELS:
        tp = sum(row[field] == level and row["gold_scope"] == level for row in rows)
        fp = sum(row[field] == level and row["gold_scope"] != level for row in rows)
        fn = sum(row[field] != level and row["gold_scope"] == level for row in rows)
        precision = tp / (tp + fp) if tp + fp else None
        recall = tp / (tp + fn) if tp + fn else None
        f1 = None if tp + fn == 0 else (0.0 if tp == 0 else 2 * precision * recall / (precision + recall))
        by_level[level] = {"support": tp + fn, "precision": precision, "recall": recall, "f1": f1}
    mismatches = [
        {"work": row["work"], "seq": row["seq"], "pred": row[field], "gold": row["gold_scope"]}
        for row in rows
        if row[field] != row["gold_scope"]
    ]
    return {
        "correct": correct,
        "total": total,
        "accuracy": correct / total,
        "ordinal_mae": ordinal / total,
        "by_level": by_level,
        "mismatches": mismatches,
    }


def mcnemar(rows: list[dict]) -> dict:
    improved = sum(
        row["c2_scope_pred"] != row["gold_scope"] and row["c4_scope_pred"] == row["gold_scope"] for row in rows
    )
    worsened = sum(
        row["c2_scope_pred"] == row["gold_scope"] and row["c4_scope_pred"] != row["gold_scope"] for row in rows
    )
    n = improved + worsened
    if n:
        tail = sum(math.comb(n, k) for k in range(min(improved, worsened) + 1))
        p = min(1.0, 2 * tail / (2**n))
    else:
        p = 1.0
    return {"improved": improved, "worsened": worsened, "discordant": n, "two_sided_exact_p": p}


def intervention_metrics(rows: list[dict], field: str) -> dict:
    selected = [row for row in rows if row[field]]
    valid = sum(row["hindsight_valid"] is True for row in selected)
    invalid = sum(row["hindsight_valid"] is False for row in selected)
    unknown = sum(row["hindsight_valid"] is None for row in selected)
    final = sum(row["is_final_sequence"] for row in selected)
    return {
        "material_interventions_total": len(selected),
        "material_interventions_evaluable": sum(not row["is_final_sequence"] for row in selected),
        "hindsight_valid": valid,
        "hindsight_invalid": invalid,
        "hindsight_unknown": unknown,
        "activation_precision_known": valid / (valid + invalid) if valid + invalid else None,
        "final_sequence_material_rewrites": final,
    }


def render_report(result: dict) -> str:
    c2 = result["scope_metrics"]["C2"]
    c4 = result["scope_metrics"]["C4"]
    i2 = result["intervention_metrics"]["C2"]
    i4 = result["intervention_metrics"]["C4"]
    mc = result["paired_scope_change"]
    return f"""# E11-C4 Archival Holdout 검증 보고서

Date: 2026-08-20  
Status: COMPLETE_INTERNAL_ARCHIVAL_HOLDOUT  
Claim boundary: E10에서 이미 동결된 미사용 E11 작품군을 이용한 archival holdout; 새 prospective run이나 promotion evidence가 아님

## 1. 표본과 봉인

- 작품: 개인의취향, 난폭한로맨스, 도깨비, 라이벌, 로망스, 미안하다사랑한다
- 대상: EP15, 총 {c2['total']} Sequence
- 기존 E11 여섯 작품과 중복: 0
- pre-unblind freeze 검증: **{result['integrity']['preunblind_freeze']['status'].upper()}**
- holdout EpisodePlan/Arc 수: {result['integrity']['holdout_files']} files
- provider 호출: 0

기존 E10 controller 결정은 target EpisodePlan 공개 전에 이미 동결돼 있었다. 이번 실험에서는 그 결정의 completion/phase 신호를 C2 scope로 변환하고, 앞서 봉인한 A1/A2를 적용한 뒤에만 EpisodePlan을 공개했다.

## 2. 범위 분류 결과

| 지표 | C2 | C4(A1) |
|---|---:|---:|
| 정확도 | {c2['correct']}/{c2['total']} ({c2['accuracy']:.2%}) | {c4['correct']}/{c4['total']} ({c4['accuracy']:.2%}) |
| Ordinal MAE | {c2['ordinal_mae']:.4f} | {c4['ordinal_mae']:.4f} |
| L3 recall | {c2['by_level']['L3']['recall']:.2%} | {c4['by_level']['L3']['recall']:.2%} |
| L3 precision | {c2['by_level']['L3']['precision']:.2%} | {'N/A' if c4['by_level']['L3']['precision'] is None else f"{c4['by_level']['L3']['precision']:.2%}"} |

A1은 {mc['improved']}건을 고쳤지만 {mc['worsened']}건을 새로 틀렸다(McNemar p={mc['two_sided_exact_p']:.4f}). 정확도와 MAE는 소폭 개선됐지만 효과가 작고, 실제 L3를 하나도 유지하지 못했다. **A1은 H1만 통과하고 필수 안전조건 H2를 위반했으므로 채택 실패다.**

실패 원인은 의미 규칙이 아니라 표현 규칙에 묶였기 때문이다. E11 이유 문장에는 `회차/axis/carrier + 완료/전환/확정`이 있었지만 E10의 같은 의미는 `목표가 완결`, `downstream objective class가 바뀜`, `단계가 끝남`으로 기록됐다.

## 3. 개입 경제성 결과

| 지표 | C2 | C4(A2) |
|---|---:|---:|
| material interventions | {i2['material_interventions_total']} | {i4['material_interventions_total']} |
| evaluable interventions | {i2['material_interventions_evaluable']} | {i4['material_interventions_evaluable']} |
| known valid / invalid | {i2['hindsight_valid']} / {i2['hindsight_invalid']} | {i4['hindsight_valid']} / {i4['hindsight_invalid']} |
| known activation precision | {i2['activation_precision_known']:.2%} | {i4['activation_precision_known']:.2%} |
| final Sequence material rewrites | {i2['final_sequence_material_rewrites']} | {i4['final_sequence_material_rewrites']} |

E10 controller가 이미 마지막 Sequence에서 rewrite 대신 close/log만 수행했기 때문에 A2가 제거할 개입은 0건이었다. **A2는 안전하지만 incremental benefit은 이 표본에서 재차 비활성화됐다.**

## 4. 가설 판정

- H1 정확도 증가 및 MAE 감소: **PASS, 단 1행 순개선이며 p={mc['two_sided_exact_p']:.4f}**
- H2 L3 recall 저하 0.10 이내: **FAIL** ({c2['by_level']['L3']['recall']:.2%} → {c4['by_level']['L3']['recall']:.2%})
- H3 final zero-value rewrite = 0: **PASS**, 단 C2도 이미 0
- H4 C4 total interventions < C2: **FAIL / NOT ACTIVATED**
- H5 stale-carrier 비열등: **NOT EVALUABLE**, E10에는 같은 정의의 행 단위 stale-carrier ledger가 없음

## 5. 결론

이 holdout에서는 이전 재분석의 81.63%→91.84% 개선 폭이 재현되지 않았다. 정확도는 {c2['accuracy']:.2%}→{c4['accuracy']:.2%}로 1행만 순개선됐고, A1은 L3 recall을 {c2['by_level']['L3']['recall']:.2%}에서 0%로 떨어뜨렸다. 따라서 기존 A1을 controller 규칙으로 채택하면 안 된다.

다음 버전은 특정 단어를 찾는 규칙이 아니라 구조 필드로 판정해야 한다. `current carrier question answered`, `remaining sequences require a different objective class`, `final hook only`를 각각 명시적인 boolean evidence로 기록한 뒤 L3를 결정해야 한다. 이 변경은 A1을 수정하는 것이므로 새 A1-R2 실험으로 다시 봉인해야 한다.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preunblind", type=Path, required=True)
    parser.add_argument("--holdout", type=Path, required=True)
    parser.add_argument("--activation-ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    pre_dir = args.preunblind.resolve()
    holdout = args.holdout.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    freeze_check = verify_freeze(pre_dir)
    if freeze_check["status"] != "pass":
        raise RuntimeError("pre-unblind freeze verification failed")
    rows = [
        json.loads(line)
        for line in (pre_dir / "PREUNBLIND_C2_C4_PREDICTIONS.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    holdout_hashes = []
    allocation_counts = {}
    for work_dir in sorted(path for path in holdout.iterdir() if path.is_dir()):
        plan = work_dir / "episode_plan.json"
        arc = work_dir / "episodearc.json"
        plan_doc = load_json(plan)
        allocation_counts[work_dir.name] = len(plan_doc["sequence_allocation"])
        for path in (plan, arc):
            holdout_hashes.append({"path": str(path), "sha256": sha256(path), "bytes": path.stat().st_size})
    expected_counts = Counter(row["work"] for row in rows)
    if dict(expected_counts) != allocation_counts:
        raise ValueError(f"holdout allocation mismatch: {expected_counts} != {allocation_counts}")

    validity_doc = load_json(args.activation_ledger.resolve())
    validity = {
        (item["work"], int(item["checkpoint"])): (bool(item["hindsight_valid"]), item["hindsight_note"])
        for item in validity_doc["items"]
    }
    for row in rows:
        key = (row["work"], row["checkpoint"])
        if key in GOLD_OVERRIDES:
            row["gold_scope"], row["gold_basis"] = GOLD_OVERRIDES[key]
        else:
            row["gold_scope"] = "L1"
            row["gold_basis"] = FINAL_HOOK_NOTES.get(
                key, "현재 Sequence의 극적 거래가 끝나지만 episode carrier objective class는 구조적으로 유지된다."
            )
        valid_record = validity.get(key)
        if row["c2_material"] and valid_record is None:
            raise ValueError(f"material intervention lacks hindsight adjudication: {key}")
        row["hindsight_valid"] = valid_record[0] if valid_record else None
        row["hindsight_note"] = valid_record[1] if valid_record else None

    c2 = classification(rows, "c2_scope_pred")
    c4 = classification(rows, "c4_scope_pred")
    i2 = intervention_metrics(rows, "c2_material")
    i4 = intervention_metrics(rows, "c4_material")
    result = {
        "schema": "E11_C4_ARCHIVAL_HOLDOUT_RESULTS_R1",
        "date": "2026-08-20",
        "experiment_type": "archival holdout validation",
        "claim_boundary": "internal evidence; not a newly generated prospective run; no promotion claim",
        "integrity": {
            "preunblind_freeze": freeze_check,
            "holdout_files": len(holdout_hashes),
            "holdout_hashes": holdout_hashes,
            "allocation_counts": allocation_counts,
        },
        "gold_distribution": dict(sorted(Counter(row["gold_scope"] for row in rows).items())),
        "scope_metrics": {"C2": c2, "C4": c4},
        "paired_scope_change": mcnemar(rows),
        "intervention_metrics": {"C2": i2, "C4": i4},
        "hypotheses": {
            "H1": {
                "criterion": "C4 accuracy > C2 and C4 ordinal MAE < C2",
                "pass": c4["accuracy"] > c2["accuracy"] and c4["ordinal_mae"] < c2["ordinal_mae"],
            },
            "H2": {
                "criterion": "C4 L3 recall no more than 0.10 below C2",
                "pass": c4["by_level"]["L3"]["recall"] >= c2["by_level"]["L3"]["recall"] - 0.10,
            },
            "H3": {"criterion": "C4 final material rewrites = 0", "pass": i4["final_sequence_material_rewrites"] == 0},
            "H4": {"criterion": "C4 material interventions < C2", "pass": i4["material_interventions_total"] < i2["material_interventions_total"]},
            "H5": {"criterion": "C4 stale-carrier <= C2", "status": "NOT_EVALUABLE_ROW_LEDGER_ABSENT"},
        },
        "scientific_interpretation": (
            "The lexical A1 rule did not generalize across controller reason styles. A2 was already implicit in the E10 "
            "controller and therefore had no incremental activation."
        ),
    }

    ledger_path = output / "E11_C4_ARCHIVAL_HOLDOUT_ROW_LEDGER.jsonl"
    with ledger_path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    result_path = output / "E11_C4_ARCHIVAL_HOLDOUT_RESULTS.json"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path = output / "E11_C4_ARCHIVAL_HOLDOUT_REPORT_20260820.md"
    report_path.write_text(render_report(result), encoding="utf-8")
    manifest = {
        "schema": "E11_C4_ARCHIVAL_HOLDOUT_OUTPUT_MANIFEST_R1",
        "files": [
            {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in (report_path, result_path, ledger_path)
        ],
        "verification": {
            "preunblind_freeze": freeze_check["status"],
            "row_count": len(rows),
            "json_parse": "pass",
            "provider_call_count": 0,
            "runtime_generation": False,
            "raw_source_exported": False,
            "promotion_claim": False,
        },
    }
    (output / "E11_C4_ARCHIVAL_HOLDOUT_OUTPUT_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"C2": c2, "C4": c4, "paired": result["paired_scope_change"], "interventions": result["intervention_metrics"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
