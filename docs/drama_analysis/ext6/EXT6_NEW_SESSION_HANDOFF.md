# EXT6 새 세션 즉시 재개 핸드오프

Status: `ROLLING_CURRENT_READY`  
Last updated: `2026-07-30`

이 문서는 새 대화 세션이 EXT6 작업을 즉시 이어가기 위한 단일 rolling handoff다. 새 버전 파일을 만들지 않고 항상 이 경로를 갱신한다.

## 1. 반드시 읽을 권위 문서

1. `docs/drama_analysis/ext6/EXT6_SINGLE_AUTHORITY_V1_2.md`
2. `docs/drama_analysis/ext6/EXT6_EXACT_SCHEMA_REGISTRY_V1_1.json`
3. `docs/drama_analysis/ext6/SECRET_FOREST_EXT6_GOLD_ANCHOR_V1_1.md`
4. `docs/drama_analysis/ext6/EXT6_AUTHORITY_CONSOLIDATION_V1_2_FIXED_20260730.md`
5. `docs/drama_analysis/ext6/EXT6_FIXED_VERSION_CORRECTION_POLICY_20260730.md`
6. 이 문서
7. `docs/drama_analysis/ext6/CURRENT_EXT6_POINTER.json`
8. `docs/drama_analysis/ext6/EXT6_ROLLOUT_STATUS.json`
9. `docs/drama_analysis/ext6/EXT6_ROLLOUT_QUEUE.json`

## 2. 고정 권위

- 방법: `EXT6_SINGLE_AUTHORITY_V1_2`
- 스키마: `EXT6_EXACT_SCHEMA_REGISTRY_V1_1`
- gold anchor: 《비밀의숲》
- 추가 버전 상향: 금지
- 오류 처리: 같은 FIXED 계열에서 기존 문서를 수정·보강하고 supersession ledger 기록
- 기존 Stage01~04: byte-exact 동결
- 자동 CANONICAL 승격: 금지

## 3. 현재 신뢰 baseline

- 파일: `DB90_EXT6_15WORKS_WINDOWS_COMPATIBLE_FIXED_20260730.zip`
- SHA256: `53613ec114049bf1565799852c515eee3a3ab66bd4cab0adbf181884f7d08001`
- 전체 작품: 90
- EXT6 완료 작품: 15
- 파일 수: 23,883
- 기존 source hold: 《최강칠우》

## 4. 최신 완료: 《궁》

- 개별 파일: `궁_EXT6_APPEND_ONLY_EVIDENCE_FIXED_20260730.zip`
- SHA256: `5b18c547b83a24c60c6dff34d14ce4d935799e27294d04d5a2d6dbf141c4da7f`
- 24회, 1,089장면
- CastPresence 3,547
- CharacterLoad 809
- Entity 107
- RiskAudit·SelectiveAppendLedger·FunctionalHoldout 완료
- core Recall@5 1.0 유지
- supplemental Recall@5 0.0→1.0
- explicit speaker 7,925건 누락 0
- alias·비인물·schema·근거 중복·장면 밖 근거 0
- Fresh Extraction PASS
- Stage01~04 변경 0

### EP02 source-order 처리

Stage01 scene ID와 원문 물리 순서가 달라 SourceSceneAlignment JSONL을 원문 물리 offset 순서로 직렬화했다. scene_no는 재발번하지 않고 그대로 보존했다. 물리 순서 차이는 logical reheading과 manual override note로 기록했다.

이 규칙은 `EXT6_AUTHORITY_CONSOLIDATION_V1_2_FIXED_20260730.md`에 보강됐다. scene_no 오름차순을 맞추기 위해 무관한 원문에 근거를 강제 귀속하는 것은 금지한다.

## 5. 현재 작업

- 대상: 《그대웃어요》
- 상태: `PENDING_EVIDENCE_BUILD_APPEND_ONLY_V1_2_AUTHORITY`
- 시작 baseline: 위 DB90 EXT6 15작품 정본
- 다음 작품: 《그들이사는세상》

## 6. 실행 순서

```text
baseline·권위 preflight
→ 원본 hash·SceneCard ordinal 고정
→ 회차별 SourceHeadingRegistry·SourceSceneAlignment
→ CastPresence·CastCoverage
→ CharacterLoad
→ 8회 블록 강검사
→ RiskAudit·SelectiveAppendLedger
→ 독립 FunctionalHoldout
→ 최종 레코드 동결 후 감사 재계산
→ 개별 ZIP CRC
→ 통합 DB Fresh Extraction 1회
```

## 7. 실행 한도 보호

- 회차별 경검사
- 8회 블록별 강검사
- 전 시즌 최종 강검사와 전체 DB Fresh Extraction 1회
- checkpoint 저장
- 중단 시 완료된 회차·블록을 다시 생성하지 않는다.

## 8. 금지 사항

- V1.3 이상 새 방법 권위 생성
- 구조 PASS만으로 작품 완료 처리
- speaking과 PRIMARY 자동 결합
- 일반명사·행동문·장소명 Entity 생성
- 동일 evidence 복수 장면 귀속
- scene_no 오름차순을 위한 허위 source alignment
- 기존 파일 수정·삭제·재정렬
- RiskAudit·SelectiveAppend·FunctionalHoldout 생략

## 9. 새 세션 첫 행동

1. 위 문서를 순서대로 읽는다.
2. DB90 EXT6 15 baseline SHA와 로컬 존재를 확인한다.
3. pointer의 현재 작품 《그대웃어요》를 확인한다.
4. 기존 checkpoint가 있으면 마지막 완료 지점 다음부터 재개한다.
5. V1.2 전체 10개 계층이 끝나기 전 완료 처리하지 않는다.
6. 완료 후 이 문서·pointer·status·queue를 같은 고정 경로에서 갱신한다.
